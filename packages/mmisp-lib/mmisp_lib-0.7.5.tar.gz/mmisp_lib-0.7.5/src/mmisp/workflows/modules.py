"""
This module contains subclasses for different node-types,
i.e. triggers and modules and implementations for modules
that were bundled with legacy MISP.
"""

from dataclasses import dataclass, field
from enum import Enum
from json import dumps
from typing import Any, Dict, List, Self, Tuple, Type, Union, cast

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models.attribute import Attribute
from ..db.models.event import Event, EventTag
from ..db.models.tag import Tag
from ..db.models.user import User
from ..lib.actions import action_publish_event
from .graph import Module, Trigger, VerbatimWorkflowInput
from .input import Filter, Operator, RoamingData, WorkflowInput, evaluate_condition, extract_path, get_path
from .misp_core_format import (
    attribute_to_misp_core_format,
    event_after_save_new_to_core_format,
    event_to_misp_core_format,
    org_from_id,
    tags_for_event_in_core_format,
)


class ModuleParamType(Enum):
    """
    This enum provides supported form fields in the visual editor to
    configure a parameter represented by
    [`ModuleParam`][mmisp.workflows.modules.ModuleParam] for a
    module.
    """

    INPUT = "input"
    HASHPATH = "hashpath"
    TEXTAREA = "textarea"
    SELECT = "select"
    PICKER = "picker"
    CHECKBOX = "checkbox"


class Overhead(Enum):
    """
    Represents overhead of a module. That means e.g. how often it will be
    executed on a typical MISP installation.
    """

    LOW = 1
    MEDIUM = 2
    HIGH = 3

    @classmethod
    def from_int(cls: Type[Self], input: int) -> Self:
        """
        Returns a member of this enum given the int
        representation of the overhead.

        Arguments:
            input: numeric representation of the overhead.
        """
        return cls(input)


@dataclass
class ModuleParam:
    """
    Each module can be configured in the visual editor, e.g. an
    if/else module needs an operator, a value to check against and
    an attribute-path to a the value to check against. All of these
    values are configurable.

    This class represents a single parameter passed to a module.
    """

    id: str
    """
    Identifier for the parameter. Must be unique in the context
    of a single module.
    """

    label: str
    """
    Human-readable label in the visual editor for this parameter.
    """

    kind: ModuleParamType
    """
    Which type of input is expected. Denoted by
    [`ModuleParamType`][mmisp.workflows.modules.ModuleParamType].
    """

    options: Dict[str, Any]
    """
    Additional options passed to the visual editor. The other
    options are useful for e.g. validation of actual workflow
    inputs. All the other parameters (e.g. placeholder) are
    passed into this dictionary.
    """

    jinja_supported: bool = False
    """
    If `True`, the input from the visual editor for this parameter
    is a jinja2 template. A template gets the
    [`WorkflowInput`][mmisp.workflows.input.WorkflowInput] data
    as input.
    """


ModuleParams = Dict[str, ModuleParam]


@dataclass
class ModuleConfiguration:
    """
    Parameters for a module. If a module defines a textarea with ID
    `foobar` as param, this class expects a dictionary

    ```python
    {
        "foobar": "mytext"
    }
    ```

    These params are defined in the visual editor and thus saved
    together with the module.
    """

    data: Dict[str, List[str] | str | bool]
    """
    The dictionary containing values for the parameters a module
    needs.
    """

    def validate(self: Self, structure: ModuleParams) -> List[str]:
        """
        Check if the parameters specified here are correct. For e.g. a
        `select`-param with id "foobar", it will be checked if
        `data["foobar"]` is among the options provided by the select.

        Arguments:
            structure: The module param definitions to validate the
                configuration against.
        """

        errors = []
        extraneous = set(self.data.keys()) - set(structure.keys())
        if len(extraneous) > 0:
            errors += [f"Unspecified keys found in configuration: {extraneous}"]

        for key, config in structure.items():
            # Values can be optional or mutually exclusive with other values.
            # Let modules figure out what to do if some keys are missing.
            # As long as the stuff that's actually set is fine, we're good.
            if not (value := self.data.get(key)):
                continue

            if config.kind == ModuleParamType.SELECT and value not in config.options.get("options", {}).keys():
                errors += [f"Param {key} has an invalid value"]

            if config.kind == ModuleParamType.CHECKBOX and not isinstance(value, bool):
                errors += [f"Param {key} is expected to be a boolean"]

        return errors


class ModuleAction(Module):
    """
    Marker class representing an action module. Not relevant for the behavior,
    but for the HTTP responses to determine which kind of module this is.
    """


class ModuleLogic(Module):
    """
    Marker class representing a logic module. Not relevant for the behavior,
    but for the HTTP responses to determine which kind of module this is.
    """


class NodeRegistry:
    def __init__(self: Self) -> None:
        self.triggers: Dict[str, Type[Trigger]] = {}
        self.modules: Dict[str, Type[Module]] = {}

    def add(self: Self, name: str, node: Type[Module | Trigger]) -> None:
        if issubclass(node, Module):
            self.modules[name] = node
        elif issubclass(node, Trigger):
            self.triggers[name] = node
        else:
            raise Exception("Node must be an instance of Module or Trigger!")

    def all(self: Self) -> Dict[str, Type[Module | Trigger]]:
        return self.triggers | self.modules


NODE_REGISTRY = NodeRegistry()


def workflow_node(cls: Type[Module | Trigger]) -> Type[Module | Trigger]:
    """
    Annotation that registers the annotated class in the
    [`NodeRegistry`][mmisp.workflows.modules.NodeRegistry].
    That way modules & triggers are registered
    in the workflow application.
    """

    NODE_REGISTRY.add(cls.id, cls)
    return cls


@workflow_node
@dataclass(kw_only=True, eq=False)
class TriggerAttributeAfterSave(Trigger):
    id: str = "attribute-after-save"
    name: str = "Attribute After Save"
    scope: str = "attribute"
    icon: str = "cube"
    description: str = "This trigger is called after an Attribute has been saved in the database"
    blocking: bool = False
    overhead: Overhead = Overhead.HIGH

    async def normalize_data(self: Self, db: AsyncSession, input: VerbatimWorkflowInput) -> RoamingData:
        assert isinstance(input, Attribute)
        return await attribute_to_misp_core_format(db, input)


@workflow_node
@dataclass(kw_only=True, eq=False)
class TriggerEnrichmentBeforeQuery(Trigger):
    id: str = "enrichment-before-query"
    scope: str = "others"
    name: str = "Enrichment Before Query"
    description: str = "This trigger is called just before a query against the enrichment service is done"
    icon: str = "asterisk"
    overhead: Overhead = Overhead.LOW
    blocking: bool = True
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class TriggerEventAfterSaveNewFromPull(Trigger):
    id: str = "event-after-save-new-from-pull"
    scope: str = "event"
    name: str = "Event After Save New From Pull"
    description: str = (
        "This trigger is called after a new Event has been saved in the database "
        "from a PULL operation. This trigger executes in place of `event-after-save-new`"
    )
    icon: str = "envelope"
    blocking: bool = False
    overhead: Overhead = Overhead.LOW

    async def normalize_data(self: Self, db: AsyncSession, input: VerbatimWorkflowInput) -> RoamingData:
        assert isinstance(input, Event)
        return await event_after_save_new_to_core_format(db, input)


@workflow_node
@dataclass(kw_only=True, eq=False)
class TriggerEventAfterSaveNew(Trigger):
    id: str = "event-after-save-new"
    scope: str = "event"
    name: str = "Event After Save New"
    description: str = "This trigger is called after a new Event has been saved in the database"
    icon: str = "envelope"
    blocking: bool = False
    overhead: Overhead = Overhead.LOW

    async def normalize_data(self: Self, db: AsyncSession, input: VerbatimWorkflowInput) -> RoamingData:
        assert isinstance(input, Event)
        return await event_after_save_new_to_core_format(db, input)


@workflow_node
@dataclass(kw_only=True, eq=False)
class TriggerEventAfterSave(Trigger):
    id: str = "event-after-save"
    scope: str = "event"
    name: str = "Event After Save"
    description: str = "This trigger is called after an Event or any of its elements has been saved in the database"
    icon: str = "envelope"
    blocking: bool = False
    overhead: Overhead = Overhead.HIGH

    async def normalize_data(self: Self, db: AsyncSession, input: VerbatimWorkflowInput) -> RoamingData:
        assert isinstance(input, Event)

        result = await event_to_misp_core_format(db, input)
        result["Event"]["Tag"] = await tags_for_event_in_core_format(db, input.id)
        result["Event"]["Orgc"] = (await org_from_id(db, input.orgc_id))["Orgc"]
        result["_AttributeFlattened"] = []

        return result


@workflow_node
@dataclass(kw_only=True, eq=False)
class TriggerEventBeforeSave(Trigger):
    id: str = "event-before-save"
    scope: str = "event"
    name: str = "Event Before Save"
    description: str = (
        "This trigger is called before an Event or any of its elements is about to be saved in the database"
    )
    icon: str = "envelope"
    blocking: bool = True
    overhead: Overhead = Overhead.HIGH

    async def normalize_data(self: Self, db: AsyncSession, input: VerbatimWorkflowInput) -> RoamingData:
        assert isinstance(input, Event)
        return await event_to_misp_core_format(db, input)


@workflow_node
@dataclass(kw_only=True, eq=False)
class TriggerEventPublish(Trigger):
    id: str = "event-publish"
    scope: str = "event"
    name: str = "Event Publish"
    description: str = "This trigger is called just before a MISP Event starts the publishing process"
    icon: str = "upload"
    blocking: bool = True
    overhead: Overhead = Overhead.LOW

    async def normalize_data(self: Self, db: AsyncSession, input: VerbatimWorkflowInput) -> RoamingData:
        assert isinstance(input, Event)
        return await event_to_misp_core_format(db, input)


@workflow_node
@dataclass(kw_only=True, eq=False)
class TriggerLogAfterSave(Trigger):
    id: str = "log-after-save"
    scope: str = "log"
    name: str = "Log After Save"
    description: str = "This trigger is called after a Log event has been saved in the database"
    icon: str = "file"
    blocking: bool = False
    overhead: Overhead = Overhead.HIGH
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class TriggerObjectAfterSave(Trigger):
    id: str = "object-after-save"
    scope: str = "object"
    name: str = "Object After Save"
    description: str = "This trigger is called after an Object has been saved in the database"
    icon: str = "cubes"
    blocking: bool = False
    overhead: Overhead = Overhead.HIGH
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class TriggerPostAfterSave(Trigger):
    id: str = "post-after-save"
    scope: str = "post"
    name: str = "Post After Save"
    description: str = "This trigger is called after a Post has been saved in the database"
    icon: str = "comment"
    blocking: bool = False
    overhead: Overhead = Overhead.LOW
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class TriggerShadowAttributeBeforeSave(Trigger):
    id: str = "shadow-attribute-before-save"
    scope: str = "shadow-attribute"
    name: str = "Shadow Attribute Before Save"
    description: str = "This trigger is called just before a Shadow Attribute is saved in the database"
    icon: str = "comment"
    blocking: bool = True
    overhead: Overhead = Overhead.MEDIUM
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class TriggerSightingAfterSave(Trigger):
    id: str = "sighting-after-save"
    scope: str = "sighting"
    name: str = "Sighting After Save"
    description: str = "This trigger is called when a sighting has been saved"
    icon: str = "eye"
    blocking: bool = False
    overhead: Overhead = Overhead.MEDIUM

    async def normalize_data(self: Self, db: AsyncSession, input: VerbatimWorkflowInput) -> RoamingData:
        assert isinstance(input, Attribute)
        # Apparently, this only has associated attribute w/o sightings in the payload?
        return await attribute_to_misp_core_format(db, input, with_sightings=False)


def _normalize_user(input: VerbatimWorkflowInput) -> RoamingData:
    assert isinstance(input, User)
    return {
        "id": input.id,
        "last_login": input.last_login,
        "date_modified": input.date_modified,
        "role_id": input.role_id,
        "invited_by": input.invited_by,
        "disabled": input.disabled,
        "current_login": input.current_login,
        "email": input.email,
        "org_id": input.org_id,
        "date_created": input.date_created,
    }


@workflow_node
@dataclass(kw_only=True, eq=False)
class TriggerUserAfterSave(Trigger):
    id: str = "user-after-save"
    scope: str = "user"
    name: str = "User After Save"
    description: str = "This trigger is called after a user has been saved in the database"
    icon: str = "user-edit"
    blocking: bool = False
    overhead: Overhead = Overhead.LOW

    async def normalize_data(self: Self, _: AsyncSession, input: VerbatimWorkflowInput) -> RoamingData:
        return _normalize_user(input)


@workflow_node
@dataclass(kw_only=True, eq=False)
class TriggerUserBeforeSave(Trigger):
    id: str = "user-before-save"
    scope: str = "user"
    name: str = "User Before Save"
    description: str = "This trigger is called just before a user is save in the database"
    icon: str = "user-plus"
    blocking: bool = True
    overhead: Overhead = Overhead.LOW

    async def normalize_data(self: Self, _: AsyncSession, input: VerbatimWorkflowInput) -> RoamingData:
        return _normalize_user(input)


class ModuleIf(ModuleLogic):
    """
    The class on which all if/else module implementations will be based.
    """

    async def exec(self: Self, payload: "WorkflowInput", db: AsyncSession) -> Tuple[bool, Union["Module", None]]:
        success, condition_true = await self._exec(payload, db)
        if not success:
            return False, None
        connections = cast(dict, self.outputs.get(1 if condition_true else 2))
        if not connections:
            return True, None
        return True, connections[0][1]

    async def _exec(self: Self, payload: "WorkflowInput", db: AsyncSession) -> Tuple[bool, bool]:  # type:ignore[override]
        """
        The implementation of the if/else execution. The first return value indicates whether the execution was
        successful, the second the decision whether to go to the yes or to the no next node.
        """
        return False, False


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleIfGeneric(ModuleIf):
    id: str = "generic-if"
    n_outputs: int = 2
    name: str = "IF :: Generic"
    version: str = "0.2"
    description: str = (
        "Generic IF / ELSE condition block. The `then` output will be used "
        "if the encoded conditions is satisfied, otherwise the `else` output will be used."
    )
    icon: str = "code-branch"
    html_template: str = "if"

    async def initialize_for_visual_editor(self: Self, db: AsyncSession) -> None:
        self.configuration.data["operator"] = "in"
        self.params = {
            "value": ModuleParam(
                id="value",
                label="Value",
                kind=ModuleParamType.INPUT,
                options={
                    "placeholder": "tlp:red",
                    "display_on": {"operator": ["in", "not_in", "equals", "not_equals"]},
                },
            ),
            "value_list": ModuleParam(
                id="value_list",
                label="Value+list",
                kind=ModuleParamType.PICKER,
                options={
                    "picker_create_new": True,
                    "placeholder": "['ip-src',+'ip-dst']",
                    "display_on": {"operator": "in_or"},
                },
            ),
            "operator": ModuleParam(
                id="operator",
                label="Operator",
                kind=ModuleParamType.SELECT,
                options={
                    "options": {
                        "in": "In",
                        "not_in": "Not+in",
                        "equals": "Equals",
                        "not_equals": "Not+equals",
                        "any_value": "Any+value",
                        "in_or": "Any+value+from",
                    },
                },
            ),
            "hash_path": ModuleParam(
                id="hash_path",
                label="Hash+path",
                kind=ModuleParamType.HASHPATH,
                options={"placeholder": "Attribute.{n}.Tag"},
            ),
        }

    async def _exec(self: Self, payload: WorkflowInput, db: AsyncSession) -> Tuple[bool, bool]:  # type:ignore[override]
        operator = Operator.from_str(cast(str, self.configuration.data["operator"]))
        hash_path = cast(str, self.configuration.data["hash_path"]).split(".")

        if operator == Operator.IN_OR:
            value = self.configuration.data["value_list"]
        else:
            value = self.configuration.data["value"]

        if operator == Operator.EQUALS or operator == Operator.NOT_EQUALS:
            extracted_data = get_path(hash_path, payload.data)
        else:
            extracted_data = extract_path(hash_path, payload.data)

        if extracted_data is False:
            extracted_data = []

        decision = evaluate_condition(value, operator, extracted_data)
        return True, decision


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleEnrichEvent(ModuleAction):
    id: str = "enrich-event"
    name: str = "Enrich Event"
    version: str = "0.2"
    description: str = "Enrich all Attributes contained in the Event with the provided module."
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleAttributeCommentOperation(ModuleAction):
    id: str = "Module_attribute_comment_operation"
    version: str = "0.1"
    name: str = "Attribute comment operation"
    description: str = "Set the Attribute's comment to the selected value"
    icon: str = "edit"
    on_demand_filtering_enabled: bool = True
    supported: bool = False
    template_params: List[str] = field(default_factory=lambda: ["comment"])


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleTagIf(ModuleIf):
    id: str = "tag-if"
    n_outputs: int = 2
    name: str = "IF :: Tag"
    version: str = "0.4"
    description: str = (
        "Tag IF / ELSE condition block. The `then` output will be used if "
        "the encoded conditions is satisfied, otherwise the `else` output will be used."
    )
    icon: str = "code-branch"
    html_template: str = "if"

    async def initialize_for_visual_editor(self: Self, db: AsyncSession) -> None:
        self.configuration.data.setdefault("scope", "event")
        self.configuration.data.setdefault("condition", "in_or")

        tags_and_clusters = (await db.execute(select(Tag.name, Tag.is_galaxy))).all()
        tags = [name for name, is_galaxy in tags_and_clusters if not is_galaxy]
        galaxies = [name for name, is_galaxy in tags_and_clusters if is_galaxy]

        self.params = {
            "scope": ModuleParam(
                id="scope",
                label="Scope",
                kind=ModuleParamType.SELECT,
                options={
                    "options": {"event": "Event", "attribute": "Attribute", "event_attribute": "Inherited Attribute"}
                },
            ),
            "condition": ModuleParam(
                id="condition",
                label="Condition",
                kind=ModuleParamType.SELECT,
                options={
                    "options": {
                        "in_or": "Is tagged with any (OR)",
                        "in_and": "Is tagged with all (AND)",
                        "not_in_or": "Is not tagged with any (OR)",
                        "not_in_and": "Is not tagged with all (AND)",
                    }
                },
            ),
            "tags": ModuleParam(
                id="tags",
                label="Tags",
                kind=ModuleParamType.PICKER,
                options={
                    "multiple": True,
                    "options": tags,
                    "placeholder": "Pick a tag",
                },
            ),
            "clusters": ModuleParam(
                id="clusters",
                label="Galaxy Clusters",
                kind=ModuleParamType.PICKER,
                options={
                    "multiple": True,
                    "options": galaxies,
                    "placeholder": "Pick a Galaxy Cluster",
                },
            ),
        }

    def __get_tags_from_scope(self: Self, payload: WorkflowInput, scope: str) -> List[Any]:
        match scope:
            case "attribute":
                hash_path = ["Event", "_AttributeFlattened", "{n}", "Tag", "{n}", "name"]
            case "event_attribute":
                hash_path = ["Event", "_AttributeFlattened", "{n}", "_allTags", "{n}", "name"]
            case "event":
                hash_path = ["Event", "Tag", "{n}", "name"]
        return extract_path(hash_path, payload.data)

    async def _exec(self: Self, payload: WorkflowInput, db: AsyncSession) -> Tuple[bool, bool]:  # type:ignore[override]
        selected_tags = cast(list, self.configuration.data.get("tags", []))
        selected_clusters = cast(list, self.configuration.data.get("clusters", []))
        return True, evaluate_condition(
            selected_tags + selected_clusters,
            Operator.from_str(cast(str, self.configuration.data.get("condition"))),
            self.__get_tags_from_scope(payload, cast(str, self.configuration.data.get("scope"))),
        )


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleStopExecution(ModuleAction):
    id: str = "stop-execution"
    n_outputs: int = 0
    template_params: List[str] = field(default_factory=lambda: ["message"])
    name: str = "Stop execution"
    version: str = "0.2"
    description: str = "Essentially stops the execution for blocking workflows. Do nothing for non-blocking ones"
    icon: str = "ban"

    async def initialize_for_visual_editor(self: Self, db: AsyncSession) -> None:
        self.configuration.data.setdefault("message", "Execution+stopped")
        self.params = {
            "message": ModuleParam(
                id="message",
                label="Stop+message",
                kind=ModuleParamType.INPUT,
                options={"placeholder": "Execution+stopped"},
                jinja_supported=True,
            )
        }

    async def exec(self: Self, payload: WorkflowInput, db: AsyncSession) -> Tuple[bool, Union["Module", None]]:
        payload.user_messages.append(cast(str, self.configuration.data.get("message", "Execution stopped")))
        return False, None


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleAttachWarninglist(ModuleAction):
    id: str = "attach-warninglist"
    name: str = "Add to warninglist"
    description: str = "Append attributes to an active custom warninglist."
    icon: str = "exclamation-triangle"
    on_demand_filtering_enabled: bool = True
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleConcurrentTask(ModuleLogic):
    """
    Accepts multiple connecting nodes and executes all of them
    concurrently.
    """

    id: str = "concurrent-task"
    name: str = "Concurrent Task"
    description: str = (
        "Allow breaking the execution process and running concurrent tasks."
        "You can connect multiple nodes the `concurrent` output."
    )
    icon: str = "random"
    enable_multiple_edges_per_output: bool = True
    html_template: str = "concurrent"


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleCountIf(ModuleIf):
    id: str = "count-if"
    name: str = "IF :: Count"
    description: str = (
        "Count IF / ELSE condition block. It counts the amount of entry "
        "selected by the provided hashpath. The `then` output will be used "
        "if the encoded conditions is satisfied, otherwise the `else` "
        "output will be used."
    )
    icon: str = "code-branch"
    html_template: str = "if"

    async def initialize_for_visual_editor(self: Self, db: AsyncSession) -> None:
        self.configuration.data.setdefault("operator", "equals")
        self.params = {
            "selector": ModuleParam(
                id="selector",
                label="Data selector to count",
                kind=ModuleParamType.HASHPATH,
                options={"placeholder": "Event.Tag.{n}.name", "hashpath": {"is_sub_selector": False}},
            ),
            "operator": ModuleParam(
                id="operator",
                label="Condition",
                kind=ModuleParamType.SELECT,
                options={
                    "options": {
                        "equals": "Equals to",
                        "not_equals": "Not Equals to",
                        "greater": "Greater than",
                        "greater_equals": "Greater or equals than",
                        "less": "Less than",
                        "less_equals": "Less or equals than",
                    }
                },
            ),
            "value": ModuleParam(id="value", label="Value", kind=ModuleParamType.INPUT, options={"placeholder": "50"}),
        }

    def __evaluate_count(self: Self, amount: int, operator: str, value: int) -> bool:
        match operator:
            case "equals":
                return amount == value
            case "not_equals":
                return amount != value
            case "greater":
                return amount > value
            case "greater_equals":
                return amount >= value
            case "less":
                return amount < value
            case "less_equals":
                return amount <= value
        return False

    async def _exec(self: Self, payload: WorkflowInput, db: AsyncSession) -> Tuple[bool, bool]:  # type:ignore[override]
        amount = len(extract_path(cast(str, self.configuration.data["selector"]).split("."), payload.data))
        operator = cast(str, self.configuration.data["operator"])
        try:
            value = int(cast(str, self.configuration.data["value"]))
        except ValueError:
            return False, False
        return True, self.__evaluate_count(amount, operator, value)


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleDistributionIf(ModuleIf):
    id: str = "distribution-if"
    name: str = "IF :: Distribution"
    version: str = "0.3"
    description: str = (
        "Distribution IF / ELSE condition block. The `then` output will "
        "be used if the encoded conditions is satisfied, otherwise the `else` "
        "output will be used."
    )
    icon: str = "code-branch"
    n_outputs: int = 2
    html_template: str = "if"
    supported: bool = False


class ModuleFilter(ModuleLogic):
    labels = ["A", "B", "C", "D", "E", "F"]

    def _filtering_labels(self: Self) -> Dict[str, str]:
        labels = {k: f"Label {k}" for k in self.labels}
        return labels


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleGenericFilterData(ModuleFilter):
    """
    Configure a filter on the workflow payload. Every
    subsequent module will only see the filtered version
    unless the effect gets reversed with
    [ModuleGenericFilterReset][mmisp.workflows.modules.ModuleGenericFilterReset].
    """

    id: str = "generic-filter-data"
    name: str = "Filter :: Generic"
    version: str = "0.2"
    description: str = (
        "Generic data filtering block. The module filters incoming data and forward the matching data to its output."
    )
    icon: str = "filter"

    async def initialize_for_visual_editor(self: Self, db: AsyncSession) -> None:
        self.params = {
            "filtering-label": ModuleParam(
                id="filtering-label",
                label="Filtering label",
                kind=ModuleParamType.SELECT,
                options={"options": self._filtering_labels(), "default": self.labels[0]},
            ),
            "selector": ModuleParam(
                id="selector",
                label="Data selector",
                kind=ModuleParamType.HASHPATH,
                options={"placeholder": "Event._AttributeFlattened.{n}", "hashpath": {"is_sub_selector": False}},
            ),
            "value": ModuleParam(
                id="value",
                label="Value",
                kind=ModuleParamType.INPUT,
                options={
                    "placeholder": "tlp:red",
                    "display_on": {
                        "operator": ["in", "not_in", "equals", "not_equals"],
                    },
                },
            ),
            "value_list": ModuleParam(
                id="value_list",
                label="Value list",
                kind=ModuleParamType.PICKER,
                options={
                    "picker_create_new": True,
                    "placeholder": dumps(["ip-src", "ip-dst"]),
                    "display_on": {"operator": ["in_or"]},
                },
            ),
            "operator": ModuleParam(
                id="operator",
                label="Operator",
                kind=ModuleParamType.SELECT,
                options={"default": Operator.IN.value, "options": {k.value: k.value for k in Operator}},
            ),
            "hash_path": ModuleParam(
                id="hash_path",
                label="Hash path",
                kind=ModuleParamType.HASHPATH,
                options={"placeholder": "Tag.name", "hashpath": {"is_sub_selector": False}},
            ),
        }

    async def _exec(self: Self, payload: WorkflowInput, db: AsyncSession) -> bool:
        config = self.configuration.data

        operator = Operator.from_str(str(config["operator"]))
        if operator == Operator.IN_OR:
            value = self.configuration.data["value_list"]
            assert isinstance(value, list)
        else:
            value = self.configuration.data["value"]
            assert isinstance(value, str)

        payload.add_filter(
            str(config["filtering-label"]),
            Filter(
                selector=str(config["selector"]),
                path=str(config["hash_path"]),
                value=value,
                operator=operator,
            ),
        )

        return True


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleGenericFilterReset(ModuleFilter):
    """
    Resets all filters declared for the workflow payload.
    """

    id: str = "generic-filter-reset"
    name: str = "Filter :: Remove filter"
    description: str = "Reset filtering"
    icon: str = "redo-alt"

    async def initialize_for_visual_editor(self: Self, db: AsyncSession) -> None:
        labels = self._filtering_labels()
        labels["all"] = "All filters"
        self.params = {
            "filtering-label": ModuleParam(
                id="filtering-label",
                kind=ModuleParamType.SELECT,
                options={"options": labels},
                jinja_supported=False,
                label="Filtering Label to remove",
            )
        }

    async def _exec(self: Self, payload: WorkflowInput, db: AsyncSession) -> bool:
        if (label := self.configuration.data["filtering-label"]) == "all":
            payload.reset_filters()
        else:
            assert isinstance(label, str)
            payload.reset_single_filter(label)
        return True


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleOrganisationIf(ModuleIf):
    """
    Module allowing to check if the organistaion property
    of the payload matches a condition.
    """

    id: str = "organisation-if"
    name: str = "IF :: Organisation"
    description: str = (
        "Organisation IF / ELSE condition block. The `then` output "
        "will be used if the encoded conditions is satisfied, otherwise "
        "the `else` output will be used."
    )
    icon: str = "code-branch"
    n_outputs: int = 2
    html_template: str = "if"
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModulePublishedIf(ModuleIf):
    id: str = "published-if"
    name: str = "IF :: Published"
    description: str = (
        "Published IF / ELSE condition block. The `then` output "
        "will be used if the encoded conditions is satisfied, otherwise "
        "the `else` output will be used."
    )
    icon: str = "code-branch"
    n_outputs: int = 2
    html_template: str = "if"

    async def initialize_for_visual_editor(self: Self, db: AsyncSession) -> None:
        self.configuration.data.setdefault("condition", "equals")
        self.params = {
            "condition": ModuleParam(
                id="condition",
                label="Condition",
                kind=ModuleParamType.SELECT,
                options={
                    "options": {
                        "equals": "Event is published",
                        "not_equals": "Event is not published",
                    }
                },
            )
        }

    async def _exec(self: Self, payload: WorkflowInput, db: AsyncSession) -> Tuple[bool, bool]:  # type:ignore[override]
        return True, evaluate_condition(
            get_path(["Event", "published"], payload.data),
            Operator.from_str(cast(str, self.configuration.data["condition"])),
            True,
        )


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleThreatLevelIf(ModuleIf):
    id: str = "threat-level-if"
    html_template: str = "if"
    n_outputs: int = 2
    name: str = "IF :: Threat Level"
    version: str = "0.1"
    description: str = (
        "Threat Level IF / ELSE condition block. The `then` output "
        "will be used if the encoded conditions is satisfied, otherwise "
        "the`else` output will be used."
    )
    icon: str = "code-branch"
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleAddEventblocklistEntry(ModuleAction):
    id: str = "add_eventblocklist_entry"
    version: str = "0.1"
    name: str = "Add Event Blocklist entry"
    description: str = "Create a new entry in the Event blocklist table"
    icon: str = "ban"


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleAssignCountryFromEnrichment(ModuleAction):
    id: str = "assign_country"
    name: str = "IF :: Threat Level"
    version: str = "0.1"
    description: str = (
        "Threat Level IF / ELSE condition block. The `then` output will be used if the "
        "encoded conditions is satisfied, otherwise the `else` output will be used."
    )
    icon: str = "code-branch"
    n_outputs: int = 2
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleAttachEnrichment(ModuleAction):
    id: str = "attach-enrichment"
    name: str = "Attach enrichment"
    version: str = "0.3"
    description: str = "Attach selected enrichment result to Attributes."
    icon: str = "asterisk"
    on_demand_filtering_enabled: bool = True
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleAttributeEditionOperation(ModuleAction):
    id: str = "attribute_edition_operation"
    name: str = "Attribute edition operation"
    description: str = "Base module allowing to modify attribute"
    icon: str = "edit"
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleAttributeIdsFlagOperation(ModuleAction):
    id: str = "attribute_ids_flag_operation"
    name: str = "Attribute IDS Flag operation"
    description: str = "Toggle or remove the IDS flag on selected attributes."
    icon: str = "edit"
    on_demand_filtering_enabled: bool = True
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleEventDistributionOperation(ModuleAction):
    id: str = "Module_event_distribution_operation"
    name: str = "Event distribution operation"
    description: str = "Set the Event's distribution to the selected level"
    icon: str = "edit"
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleMsTeamsWebhook(ModuleAction):
    id: str = "ms-teams-webhook"
    name: str = "MS Teams Webhook"
    version: str = "0.5"
    description: str = 'Perform callbacks to the MS Teams webhook provided by the "Incoming Webhook" connector'
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModulePublishEvent(ModuleAction):
    id: str = "publish-event"
    name: str = "Publish Event"
    version: str = "0.1"
    description: str = "Publish an Event in the context of the workflow"
    icon: str = "upload"

    async def initialize_for_visual_editor(self: Self, db: AsyncSession) -> None:
        self.params = {}

    async def _exec(self: Self, payload: "WorkflowInput", db: AsyncSession) -> bool:
        try:
            event_id = str(payload.data["Event"]["id"])  # type: ignore
        except KeyError or TypeError:  # type: ignore[truthy-function]
            return False

        if not event_id or not event_id.isdigit():
            return False

        event = await db.get(Event, event_id)

        if not event:
            return False

        await action_publish_event(db, event)

        return True


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModulePushZMQ(ModuleAction):
    id: str = "push-zmq"
    name: str = "Push to ZMQ"
    version: str = "0.2"
    description: str = "Push to the ZMQ channel"
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleSendLogMail(ModuleAction):
    id: str = "send-log-mail"
    name: str = "Send Log Mail"
    description: str = (
        "Allow to send a Mail to a list or recipients, based on a Log trigger."
        " Requires functional misp-modules to be functional."
    )
    icon: str = "envelope"
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleSendMail(ModuleAction):
    id: str = "send-mail"
    name: str = "Send Mail"
    description: str = (
        "Allow to send a Mail to a list or recipients. Requires functional misp-modules to be functional."
    )
    icon: str = "envelope"
    supported: bool = False
    template_params: List[str] = field(default_factory=lambda: ["mail_template_subject", "mail_template_body"])


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleSplunkHecExport(ModuleAction):
    id: str = "splunk-hec-export"
    name: str = "Splunk HEC export"
    version: str = "0.2"
    description: str = (
        "Export Event Data to Splunk HTTP Event Collector. Due to the potential high amount "
        "of requests, it's recommanded to put this module after a `concurrent_task` logic module."
    )
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleTagOperation(ModuleAction):
    id: str = "tag_operation"
    name: str = "Tag operation"
    description: str = "Add or remove tags on Event or Attributes."
    icon: str = "tags"
    on_demand_filtering_enabled: bool = True
    version: str = "0.2"
    # supported: bool = False

    async def initialize_for_visual_editor(self: Self, db: AsyncSession) -> None:
        self.configuration.data.setdefault("scope", "event")
        self.configuration.data.setdefault("action", "add_tag")
        self.configuration.data.setdefault("tag_locality", "local")

        tags = (await db.execute(select(Tag.name))).scalars().all()

        tag_dict = {tag: tag for tag in tags}

        self.params = {
            "scope": ModuleParam(
                id="scope",
                label="Scope",
                kind=ModuleParamType.SELECT,
                options={
                    "options": {
                        "event": "Event",
                        "attribute": "Attribute",
                    }  # currently tags can only be added to events.
                },
            ),
            "action": ModuleParam(
                id="action",
                label="Action",
                kind=ModuleParamType.SELECT,
                options={"options": {"add": "Add Tag", "remove": "Remove Tag"}},
            ),
            "tag_locality": ModuleParam(
                id="tag_locality",
                label="Tag Locality",
                kind=ModuleParamType.SELECT,
                options={"options": {"local": "Local", "global": "Global", "any": "Any"}},
            ),
            "tags": ModuleParam(
                id="tags",
                label="Tags",
                kind=ModuleParamType.PICKER,
                options={
                    "multiple": True,
                    "picker_create_new": True,
                    "placeholder": "Select some Options",
                    "options": tag_dict,
                },
            ),
            "relationship_type": ModuleParam(
                id="relationship_type",
                label="Relationship Type",
                kind=ModuleParamType.INPUT,
                options={"placeholder": "Relationship Type", "display_on": {"action": "add"}},
            ),
        }

    async def _add_tag(
        self: Self, payload: WorkflowInput, db: AsyncSession, scope: str, tag_name: str, tag_locality: str
    ) -> bool:
        try:
            event_id = str(payload.data["Event"]["id"])  # type: ignore
        except KeyError or TypeError:  # type: ignore[truthy-function]
            return False

        local = tag_locality == "local"
        tag_id = (await db.execute(select(Tag.id).where(Tag.name == tag_name))).scalar()

        if tag_id is None:
            return False

        if scope == "event":
            event_tag = EventTag(event_id=event_id, tag_id=tag_id, local=local)

            db.add(event_tag)
            await db.flush()
            return True

        elif scope == "attribute":
            return False

        return False

    async def _remove_tag(
        self: Self, payload: WorkflowInput, db: AsyncSession, scope: str, tag_name: str, tag_locality: str
    ) -> bool:
        try:
            event_id = str(payload.data["Event"]["id"])  # type: ignore
        except KeyError or TypeError:  # type: ignore[truthy-function]
            return False

        tag_id = (await db.execute(select(Tag.id).where(Tag.name == tag_name))).scalar()

        if tag_id is None:
            return True

        event_tag = (
            await db.execute(select(EventTag).where(and_(EventTag.event_id == event_id, EventTag.tag_id == tag_id)))
        ).scalar()

        if event_tag is None:
            return True

        if scope == "event":
            await db.delete(event_tag)
            await db.commit()
            return True

        return False

    async def _exec(self: Self, payload: WorkflowInput, db: AsyncSession) -> bool:
        scope = cast(str, self.configuration.data["scope"])
        action = cast(str, self.configuration.data["action"])
        tag_name = cast(str, self.configuration.data["tags"])
        tag_locality = cast(str, self.configuration.data["tag_locality"])

        if scope == "attribute":
            return False

        if action == "add":
            return await self._add_tag(payload, db, scope, tag_name, tag_locality)
        elif action == "remove":
            return await self._remove_tag(payload, db, scope, tag_name, tag_locality)

        return False


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleTagReplacementGeneric(ModuleAction):
    id: str = "tag_replacement_generic"
    name: str = "Tag Replacement Generic"
    description: str = "Attach a tag, or substitue a tag by another"
    icon: str = "tags"
    on_demand_filtering_enabled: bool = True
    version: str = "0.1"
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleTagReplacementPap(ModuleAction):
    id: str = "tag_replacement_pap"
    name: str = "Tag Replacement - PAP"
    description: str = "Attach a tag (or substitue) a tag by another for the PAP taxonomy"
    icon: str = "tags"
    on_demand_filtering_enabled: bool = True
    version: str = "0.1"
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleTagReplacementTlp(ModuleAction):
    id: str = "tag_replacement_tlp"
    name: str = "Tag Replacement - TLP"
    version: str = "0.1"
    description: str = "Attach a tag (or substitue) a tag by another for the TLP taxonomy"
    icon: str = "tags"
    on_demand_filtering_enabled: bool = True
    supported: bool = False


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleTelegramSendAlert(ModuleAction):
    id: str = "telegram-send-alert"
    name: str = "Telegram Send Alert"
    version: str = "0.1"
    description: str = "Send a message alert to a Telegram channel"
    supported: bool = False
    template_params: List[str] = field(default_factory=lambda: ["message_body_template"])


@workflow_node
@dataclass(kw_only=True, eq=False)
class ModuleWebhook(ModuleAction):
    id: str = "webhook"
    name: str = "Webhook"
    version: str = "0.7"
    description: str = "Allow to perform custom callbacks to the provided URL"
    supported: bool = False
    template_params: List[str] = field(default_factory=lambda: ["url", "payload", "headers"])
