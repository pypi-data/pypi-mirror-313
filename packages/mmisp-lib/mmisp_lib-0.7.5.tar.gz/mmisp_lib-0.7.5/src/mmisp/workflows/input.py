"""
Data structure for the payload passed to the workflow and
filtering mechanism associated with it.
"""

import copy
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Self, Type

if TYPE_CHECKING:
    from ..db.models.user import User
    from ..db.models.workflow import Workflow

RoamingData = Dict[str, Any]


class Operator(Enum):
    """
    Enum representing possible filter operations.
    """

    IN = "in"
    NOT_IN = "not_in"
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    ANY_VALUE = "any_value"
    IN_OR = "in_or"
    NOT_IN_OR = "not_in_or"
    IN_AND = "in_and"
    NOT_IN_AND = "not_in_and"

    @classmethod
    def from_str(cls: Type[Self], input: str) -> Self:
        """
        Returns a member of this enum given the string
        representation of the operator.

        Arguments:
            input: string representation of the operator.
        """
        return cls(input)


class EvaluateImplementation(Enum):
    """
    Enum representing all EvaluateCondition implementations in Legacy MISP.
    """

    LEGACY_IF_ELSE = 1
    LEGACY_FILTER = 2


class FilterError(Exception):
    """
    Abstract class representing possible invalid Filter inputs
    """


@dataclass
class InvalidSelectionError(FilterError):
    """
    If the selection passed to the filter is invalid this error is returned.
    Examples for invalid selections are datatypes other from String, hashpahts,
    that dont lead to a list or empty strings
    """

    message: str


@dataclass
class InvalidPathError(FilterError):
    """
    If the path passed to the filter is invalid this error is returned.
    e.g.: empty String
    """

    message: str


@dataclass
class InvalidOperationError(FilterError):
    """
    If the operation passed to the filter is invalid this error is returned.
    e.g.: Operation.to_str fails to return a valid operation.
    """

    message: str


@dataclass
class InvalidValueError(FilterError):
    """
    If the value passed to the filter is invalid this error is returned.
    e.g.: input not of type str or List[str]
    """

    message: str


def extract_path(path: List[str], data: Any) -> List[Any]:
    """
    A utility method providing the Hash::extract functionality in CakePHP.

    Arguments:
        path: The hash path to extract data from.
        data: The container to extract data from.
    Returns:
        A list of the extracted data, if data matching the hash path was found, an empty List otherwise.
    """
    if path == []:
        return [data]

    if path[0] == "{n}" and isinstance(data, list):
        results = []
        for el in data:
            extracted = extract_path(path[1:], el)
            if extracted:
                results.extend(extracted)
        return results

    if isinstance(data, dict) and path[0] in data:
        return extract_path(path[1:], data[path[0]])

    return []


def get_path(path: List[str], data: Any) -> Any:
    """
    A utility method providing the Hash::get functionality in CakePHP.

    Arguments:
        path: The hash path to extract data from.
        data: The container to extract data from.
    Returns:
        The extracted data, if data matching the hash path was found, a None pointer otherwise.
    """
    if path == []:
        return data
    if isinstance(data, dict) and path[0] in data:
        return get_path(path[1:], data[path[0]])
    return None


def evaluate_condition(
    left: Any | List[Any],
    operator: Operator,
    right: Any | List[Any],
    impl: EvaluateImplementation = EvaluateImplementation.LEGACY_IF_ELSE,
) -> bool:
    """
    A utility method for performing comparisons between the specified data.

    Arguments:
        left: The first operand.
        operator: The operator to be used in the comparison.
        right: The second operand.
        impl: Which legacy MISP implementation of evaluate condition to be used: the if/else or the filter.
    Returns:
        Whether the comparison holds or not.
    """
    match operator:
        case Operator.ANY_VALUE:
            return right is not None and right != []
        case Operator.IN:
            return isinstance(right, list) and left in right
        case Operator.NOT_IN:
            return isinstance(right, list) and left not in right
        case Operator.EQUALS:
            match impl:
                case EvaluateImplementation.LEGACY_IF_ELSE:
                    return not isinstance(right, list) and left == right
                case EvaluateImplementation.LEGACY_FILTER:
                    return left == str(right)
        case Operator.NOT_EQUALS:
            match impl:
                case EvaluateImplementation.LEGACY_IF_ELSE:
                    return not isinstance(right, list) and left != right
                case EvaluateImplementation.LEGACY_FILTER:
                    return left != str(right)
        case _:
            if not isinstance(left, list) or not isinstance(right, list):
                return False
            match operator:
                case Operator.IN_OR:
                    for to_be_searched in left:
                        if to_be_searched in right:
                            return True
                    return False
                case Operator.NOT_IN_OR:
                    for to_be_searched in left:
                        if to_be_searched in right:
                            return False
                    return True
                case Operator.IN_AND:
                    for to_be_searched in left:
                        if to_be_searched not in right:
                            return False
                    return True
                case Operator.NOT_IN_AND:
                    for to_be_searched in left:
                        if to_be_searched not in right:
                            return True
                    return False
    return False


@dataclass
class Filter:
    """
    The data passed to a workflow can be filtered on-demand.
    That means, all entries from the dict may be removed that
    don't match a condition.

    The condition that needs to match is represented by
    this object.

    There are two ways these filters can be applied:

    * via the
      [`ModuleGenericFilterData`][mmisp.workflows.modules.ModuleGenericFilterData]
      in place. Can be undone by adding
      [`ModuleGenericFilterReset`][mmisp.workflows.modules.ModuleGenericFilterReset]
      later on.

    * via a module with `on_demand_filtering_enabled` set to
      `True`. The filtering must be called by the module itself
      in that case.
    """

    selector: str
    """
    Attribute path pointing to a list inside the
    [`WorkflowInput`][mmisp.workflows.input.WorkflowInput].
    In this list, each element below attribute-path `path`
    will be checked against `value` using operation
    `operator`.

    For instance given the structure

    ```python
    {
        "foo": [
            {
                "bar": "lololo"
            },
            {
                "bar": "lalala"
            },
        ]
    }
    ```

    a filter with `selector` being `foo`, `path` being `bar`,
    `value` being `lololo` and `operator` being
    `not_equal` would result in

    ```python
    {
        "foo": [
            {
                "bar": "lalala"
            }
        ]
    }
    ```

    Path must be a
    [CakePHP hash path](https://book.cakephp.org/3/en/core-libraries/hash.html)
    since existing legacy MISP filters are using that format
    as well.

    !!! note
        MMSIP filter currently only support limited hash path functionality.

        Supported features are the dot-separated paths consisting of keys and
        '{n}' indicating iterating over a list or a dictionary with numeric keys.

        Additional hash path functionality such as Matchers could be added to MMISP later.
    """

    path: str
    """
    Attribute path in the list where each item will be
    checked against `value` using operation `operator`.
    """

    operator: Operator
    """
    [`Operator`][mmisp.workflows.input.Operator] to compare
    the item below `path` against `value`.
    """

    value: str | List[str]
    """
    Value to compare against. Can be a list for operations
    `in`/`not_in` or a string value for `equals`/etc..
    """

    def match_value(self: Self, value: Any) -> bool:
        """
        Check if a value matches a filter.

        Arguments:
            value: The value to check.
            filter: The filter to match against.

        Returns:
            True if the value matches the filter, False otherwise.
        """
        return evaluate_condition(self.value, self.operator, value, EvaluateImplementation.LEGACY_FILTER)

    def apply(self: Self, data: RoamingData | List[RoamingData]) -> None:
        selector = self.selector.split(".")

        self.__deep_insert(data, selector, self.__get_matching_items(extract_path(selector, data)))

    def __deep_insert(
        self: Self, target: RoamingData | List[RoamingData], path: List[Any], data: List[Any] | Literal[False]
    ) -> None:
        token = path.pop(0)
        if token == "{n}":
            # When having a "wildcard" for each list key, the stuff below
            # is inserted into each list element.
            assert isinstance(target, list) and isinstance(data, list)
            for i, _ in enumerate(target):
                self.__deep_insert(target, [i] + path, data)
        elif path == []:
            if data is False:
                # If the extraction failed, we insert the key as done in
                # legacy MISP, but set it to False.
                assert isinstance(token, str)
                target[token] = False  # type:ignore[call-overload]
            elif isinstance(data, list):
                # Here it gets a little hairy:
                # this section will be reached if
                # * the extraction of `selection` worked, but
                #   `__get_matching_items` found no matches, i.e. `data`
                #   is [].
                # * the final portion of the hashpath is not `{n}` (e.g.
                #   `Event._AttributeFlattened.{n}.Tag`): then, the "final"
                #   `data` is always the value below `Tag` here.
                target[token] = data[0] if data != [] else []
            else:
                target[token] = data
        elif path == ["{n}"]:
            # Reassigning variables in Python isn't equal to a pointer
            # assignment. Hence, we cannot do `target = data` in the next
            # step and assign the list to the dictionary key here already.
            assert data is not False
            target[token] = data
        else:
            self.__deep_insert(target[token], path, data)

    def __get_matching_items(self: Self, data: List[Any] | Literal[False]) -> List[Any] | Literal[False]:
        if not data:
            return False

        result = []
        for item in data:
            to_check = extract_path(self.path.split("."), item)
            if any(self.match_value(elem) for elem in to_check):
                result.append(item)

        return result

    def validate(self: Self) -> None:
        # check selection

        if self.selector == "":
            raise InvalidSelectionError("empty selection")

        # check path
        if self.path == "":
            raise InvalidPathError("empty path")

        # check operator
        if not isinstance(self.operator, Operator):
            raise InvalidOperationError("invalid operator")

        # check value
        if self.operator == Operator.IN_OR and not isinstance(self.value, list):
            raise InvalidValueError("incorrect type")

        elif self.operator == Operator.ANY_VALUE:
            if self.value != "":
                raise InvalidValueError("any value operator does not accept a value")

        return None


class WorkflowInput:
    """
    When a workflow gets executed, it gets input data. For
    instance, the "after event save"-workflow gets a dictionary
    containing the event that was saved.

    Additionally, filters can be added by modules. That way,
    subsequent modules will only see a filtered subset
    of the workflow data. This operation can be undone.

    Filters are expressed using [`Filter`][mmisp.workflows.input.Filter]
    class.
    """

    def __init__(self: Self, data: RoamingData, user: "User", workflow: "Workflow") -> None:
        self.__unfiltered_data = data
        self.__filtered_data: RoamingData | List[RoamingData] | None = None
        self.user = user
        self.workflow = workflow
        self.filters: Dict[str, Filter] = {}
        self.user_messages: List[str] = []

    @property
    def data(self: Self) -> RoamingData | List[RoamingData] | None:
        """
        Returns either all of the data given to the workflow input
        OR a list with filter results if a filter was added
        using [`WorkflowInput.add_filter`][mmisp.workflows.input.WorkflowInput.add_filter].
        """

        if self.filters == {}:
            return self.__unfiltered_data

        if self.__filtered_data is None:
            self.filter()

        return self.__filtered_data

    def filter(self: Self) -> None:
        result = copy.deepcopy(self.__unfiltered_data)
        for filter in self.filters.values():
            filter.apply(result)

        self.__filtered_data = result

    def add_filter(self: Self, label: str, filter: Filter) -> None:
        """
        Adds another [`Filter`][mmisp.workflows.input.Filter]
        to the workflow input.

        Arguments:
            filter: Filter to be added.
        """

        filter.validate()

        self.filters[label] = filter
        self.__filtered_data = None

    def reset_single_filter(self: Self, label: str) -> None:
        del self.filters[label]
        self.filtered_data = None

    def reset_filters(self: Self) -> None:
        """
        Removes all filters from the workflow input.
        [`WorkflowInput.data`][mmisp.workflows.input.WorkflowInput.data]
        will contain all of the data it has instead of a
        filtered portion now.
        """
        self.filters = {}
        self.filtered_data = None
