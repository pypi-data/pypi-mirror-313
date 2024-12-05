"""
This package contains the data-structure representing the workflow graph
and the modules in it.

The sub-packages are specialisations, in this package the basic graph representation
is implemented.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict, Iterable, List, Optional, Self, Tuple, Union
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from ..db.database import Base
    from .input import Filter, RoamingData, WorkflowInput
    from .modules import ModuleConfiguration, Overhead

NodeConnection = Tuple[int, Union["Module", "Trigger"]]


@dataclass
class Apperance:
    """
    Value object with attributes that are only used in the visual editor.
    """

    pos: Tuple[float, float]
    """
    Tuple with x/y coordinates in the canvas where the current node is displayed.
    """

    typenode: bool
    """
    Unclear what exactly that is. Hardcoded to `False` for now since it's like this everywhere.
    """

    cssClass: str
    """
    CSS classes that the current node has in the visual editor.
    """

    nodeUid: str | None
    """
    Unique ID in the DOM set by the visual editor. Sometimes it's apparently `None` for
    unknown reasons.
    """


class GraphError(ABC):
    """
    Abstract base-class for validation errors in the graph structure. The idea is to
    display error kinds via

    ```python
    match error:
        case CyclicGraphError(path):
            pass
        case MultipleEdgesPerOutput(affected):
            pass
        # ...
    ```
    """


@dataclass
class CyclicGraphError(GraphError):
    """
    If a cycle was found in the graph it is invalid. This class represents that error.
    """

    cycle_path: List[Tuple["Node", int, "Node", int]]
    """
    List of edges (from, output_port, to, input_port) that create a cycle.
    """


@dataclass
class MultipleEdgesPerOutput(GraphError):
    """
    A [`Node`][mmisp.workflows.graph.Node] has multiple inputs and outputs. Unless
    explicitly allowed, each output may only have a single connection to another node.
    An example for that is [`ModuleConcurrentTask`][mmisp.workflows.modules.ModuleConcurrentTask].

    This class represents the error if that's not allowed.
    """

    affected: Tuple["Node", int]
    """
    All edges affected by the problem: first component of the tuple
    is the node with too many connections per output, the second
    component is the ID of the affected output.
    """


class MissingTrigger(GraphError):
    """
    Each workflow that isn't a blueprint must have a trigger as starting node.
    A violation of that is described with this class.

    !!! note
        Incidentally, in legacy MISP this isn't part of `checkGraph`, but
        only used in the validation rules of the `Workflow` model.

        In MMISP, both validations are unified.
    """


@dataclass
class UnsupportedWorkflow(GraphError):
    """
    Not all modules are implemented in modern MISP. All of them exist though
    to allow reading any workflow JSON here.

    If a workflow relies on unsupported modules, this error class is used.
    """

    module_graph_id: int
    """
    ID of the unsupported module
    """


@dataclass
class ConfigurationError(GraphError):
    """
    Generic "configuration error" class. Useful to e.g. reject wrong parameters
    from the visual editor.
    """

    node: "Node"
    """
    Reference to the misconfigured node.
    """

    context: str
    """
    Error message.
    """


@dataclass
class InconsistentEdgeBetweenAdjacencyLists(GraphError):
    """
    In MISP the standard for storing the graph is in duplicated form, the graph is stored once as an adjacency list of
    outgoing edges and in parallel a second time as an adjacency list of incoming edges.
    In case there is an edge from node A to node B, that is registered as outgoing from node A to node B and not as
    incoming from node A to node B or vica-versa, this is an inconsistency error that will be returned with an instance
    of this class.
    """

    from_: "Node"
    """
    The starting node of the inconsistent edge.
    """

    output_port_id: int
    "The output port of the inconsistent edge."

    to: "Node"
    """
    The ending node of the inconsistent edge.
    """

    input_port_id: int
    """
    The input port of the inconsistent edge.
    """


@dataclass
class GraphValidationResult:
    """
    Accumulator for all validation results. The idea is to run graph-level checks such
    as cycle-detection in [`Graph.check`][mmisp.workflows.graph.Graph.check] and then run node-level
    checks in [`Node.check`][mmisp.workflows.graph.Node.check]. Whenever an error is encountered, it's
    added into this class.
    """

    errors: List[GraphError]
    """
    Fatal errors in the workflow graph. The graph is unusable like this.
    """

    def add_result(self: Self, other: Self) -> None:
        """
        Merges another validation result into this accumulator object.

        Arguments:
            other: Another validation result added in here.
        """
        self.errors += other.errors

    def is_valid(self: Self) -> bool:
        """
        If neither errors nor warnings are added, the graph is valid.
        """
        return self.errors == []


@dataclass(kw_only=True)
class Node(ABC):
    """
    A single node in a graph. Can be a trigger - something that caused the workflow run -
    or a module - a behavioral component in the workflow graph.

    Inputs & outputs can be thought of like a layer 4 address where the node is the
    address and the input/output is the port number. So an edge doesn't just connect
    two nodes together, but tuples of `(output number, input)` and
    `(input number, output)`. This is needed because

    * The concurrent execution requires just a single output, but with multiple edges
      to other modules from it.
    * An If/Else module has two outputs: one node to execute if the condition is
      true and one if it isn't.

    It might've been possible to infer outputs by the order of the connections, but this
    would've lead to ambiguity because

    * If >1 module is connected to this module, it's not clear whether there are multiple
      connections leaving the same output (as in the concurrency module) or if each module
      has its own meaning (as in the if/else module).
    * It's valid to produce an if/else module with only else connecting to another node.
      In that case the first output in the list should actually be encoded as
      second list element since the first is empty.

    Because of that, infering inputs/outputs from the order seemed too error-prone
    and the legacy MISP structure was reused here.
    """

    inputs: Dict[int, List[NodeConnection]]
    """
    References to [`Node`][mmisp.workflows.graph.Node] objects connecting to this
    node. Grouped by the ID of the input.
    """

    outputs: Dict[int, List[NodeConnection]]
    """
    References to [`Node`][mmisp.workflows.graph.Node] objects that are connected to
    this node. Grouped by the ID of the output.

    The data-structure is recursive here (basically a doubly-linked list)
    using references to make walking the graph as easy as possible.
    """

    graph_id: int
    """
    The id with which this node was identified in the json data, that was used to initialize its parent graph.
    """

    n_inputs: int = 1
    """
    Number of _allowed_ inputs. If `inputs` exceeds this, the
    [`Node.check`][mmisp.workflows.graph.Node.check] method will return an error for this.
    """

    n_outputs: int = 1
    """
    Number of _allowed_ outputs. If `outputs` exceeds this, the
    [`Node.check`][mmisp.workflows.graph.Node.check] method will return an error for this.
    """

    enable_multiple_edges_per_output: bool = False
    """
    Whether it's OK to have multiple edges going from a single output.
    See [`Node`][mmisp.workflows.graph.Node] for more context. Used by e.g. the concurrent
    tasks module.
    """

    supported: bool = True
    """
    Indicator whether the module / trigger is supported. All items from legacy MISP
    exist here to allow loading any workflow, but not all are actually supported by
    the application.
    """

    def __eq__(self: Self, other: object) -> bool:
        """
        Custom comparison if two instances are equal, needed for our special hash function so that the statement
        __eq__(a, b) = True => __hash__(a) == __hash__(b) is valid for every pair of nodes a nd b, which guaranties that
        the Dict (HashMap) will not malfunction.

        Arguments:
            other: A reference to the other object to be compared.
        """
        return self is other

    def __hash__(self: Self) -> int:
        """
        Our custom node hash function which allows to store nodes in a Dict (HashMap).
        """
        return id(self)

    def check(self: Self) -> GraphValidationResult:
        """
        Checks if the module is correctly configured. At Node level 3 conditions are checked (and errors returned if not
        fulfilled):
        1(2). The registered input(output) ports are in the range from 1 to
        ['n_inputs'][mmisp.workflows.graph.Node.n_inputs](['n_outputs'][mmisp.workflows.graph.Node.n_outputs]) incl.
        It is allowed to have less registered input(output) ports than the specified maximum amount.
        3. In case ['enable_multiple_edges_per_output'][mmisp.workflows.graph.Node.enable_multiple_edges_per_output] has
        a value of false, each outgoing port has maximum 1 outgoing edge. (It is allowed for an outgoing port to have no
        outgoing edges.)
        """
        result = GraphValidationResult([])
        for input_id in self.inputs.keys():
            if input_id < 1 or input_id > self.n_inputs:
                result.errors.append(
                    ConfigurationError(
                        self,
                        "There is an input port registered for this node outside of the valid range of [1, "
                        + str(self.n_inputs)
                        + "].",
                    )
                )
        for output_id in self.outputs.keys():
            if output_id < 1 or output_id > self.n_outputs:
                result.errors.append(
                    ConfigurationError(
                        self,
                        "There is an output port registered for this node outside of the valid range of [1, "
                        + str(self.n_outputs)
                        + "].",
                    )
                )
        if not self.enable_multiple_edges_per_output:
            for key, value in self.outputs.items():
                if len(value) > 1:
                    result.errors.append(MultipleEdgesPerOutput((self, key)))

        return result


@dataclass(kw_only=True, eq=False)
class WorkflowNode(Node):
    """
    Dataclass with shared properties for both modules & triggers,
    but not relevant for the abstract Node type.
    """

    id: str
    """
    Unique identifier of the module/trigger. To be declared in the
    subclass implementing a concrete module/trigger.
    """

    name: str
    """
    Human-readable identifier of the module/trigger. To be declared in the
    subclass implementing a concrete module/trigger.
    """

    blocking: bool
    """
    If the workflow of a blocking trigger fails, the actual
    operation won't be carried out. For instance, if the
    "event before save"-trigger fails, the event will not
    besaved.

    For modules, blocking and failing modules will terminate
    the workflow execution.
    """

    version: str = "0.1"
    """
    Current version of the module. To be declared in the
    subclass implementing a concrete module.
    """

    apperance: Apperance
    """
    Value object with miscellaneous settings for the visual editor.
    """

    def check(self: Self) -> GraphValidationResult:
        results = super().check()
        if not self.supported:
            results.errors.append(UnsupportedWorkflow(self.graph_id))
        return results


@dataclass(kw_only=True, eq=False)
class Module(WorkflowNode):
    """
    A module is a workflow node that is either

    * an action, i.e. performs an operation with an observable effect
    * a logic module, i.e. forwards to a different module based on
      a condition
    * a filter, i.e. manipulates the
      [`WorkflowInput`][mmisp.workflows.input.WorkflowInput].

    A module implementation can be provided by writing a subclass that
    assigns values to at least `id`, `version`, `name`.
    """

    configuration: "ModuleConfiguration"
    """
    Values for the params required by this module.
    """

    template_params: List[str] = field(default_factory=lambda: [])
    """
    List containing all params that are jinja2 templates.
    """

    on_demand_filter: Optional["Filter"]
    """
    Some modules allow filtering of data internally without modifying
    [`WorkflowInput`][mmisp.workflows.input.WorkflowInput]. The filter
    used for that is defined by this attribute.
    """

    previous_version: str = "?"
    """
    Previously used version of the module.
    """

    html_template: str = ""
    """
    HTML template provided by the visual editor to use.
    To be declared in the subclass implementing a concrete module.
    """

    on_demand_filtering_enabled: bool = False
    """
    Whether internal filtering is enabled.
    """

    blocking: bool = False
    """
    Whether or not the module is blocking, i.e. can abort the
    workflow if it fails. If it's not blocking and fails,
    execution continues.
    """

    description: str = ""
    """
    Human-readable description of the node.
    Must be here because Modules and triggers have a description.
    """

    icon: str = "envelope"
    """
    Frontend icon.
    Must be here because Modules and triggers have a description.
    """

    params: None | dict = None

    async def initialize_for_visual_editor(self: Self, db: AsyncSession) -> None:
        """
        Initializes the parameters for a module. Done in a method
        since that may involve further DB operations.

        Only needed for the visual editor, not the execution since it
        defines which params are expected and which values are accepted
        (e.g. all attributes stored in the database).

        Arguments:
            db: SQLAlchemy session
        """
        self.params = {}

    def is_initialized_for_visual_editor(self: Self) -> bool:
        """
        Checks if the module was initialized for the visual editor
        which happens by calling
        [`Module.initialize`][mmisp.workflows.modules.Module.initialize].
        It's expected that the attribute
        `params` will be set by this method.
        """
        return hasattr(self, "params") and isinstance(self.params, dict)

    async def exec(self: Self, payload: "WorkflowInput", db: AsyncSession) -> Tuple[bool, Union["Module", None]]:
        """
        Executes the module using the specific payload given by the workflow that calls
        the execution of the module.
        Execution strongly depends on the type of the module that is executed.

        The first component of the tuple indicates whether execution was successful.
        The second component of the tuple is the next node to be executed.

        Since this library allows arbitrarily many inputs & outputs, we cannot infer
        the next module from the success of the execution of this module (relevant for
        e.g. if/else).

        The default implementation assumes exactly one output and returns it on success.

        Arguments:
            payload: The workflows input for the specific module execution.
            db: Database handle for write operations.
        """
        assert self.n_outputs == 1, """
                Module.exec() assumes exactly one output. If that's not the case,
                override the method.
            """
        assert not self.enable_multiple_edges_per_output, """
                Module.exec() assumes each output allows only a single edge.
                if that's not the case, override the method.
            """

        result = await self._exec(payload, db)
        # execution failed, no more things to do.
        if not result:
            return (False, None)

        default_output = next(iter(self.outputs.values()))
        if default_output == []:
            return (result, None)

        next_step = default_output[0][1]
        assert not isinstance(next_step, Trigger)
        return (result, next_step)

    async def _exec(self: Self, payload: "WorkflowInput", db: AsyncSession) -> bool:
        return False

    def check(self: Self) -> GraphValidationResult:
        results = super().check()
        assert self.is_initialized_for_visual_editor()
        # Ignore the type error here, mypy doesn't realize that is_initialized_for_visual_editor
        # checks for that already.
        errors = self.configuration.validate(self.params)  # type:ignore[arg-type]
        if errors != []:
            for e in errors:
                results.errors.append(ConfigurationError(self, e))
        return results


VerbatimWorkflowInput = Union["RoamingData", "Base"]


@dataclass(kw_only=True, eq=False)
class Trigger(WorkflowNode):
    """
    A trigger represents the starting point of a workflow.
    It can have only one output and no inputs. Each trigger
    is represented by this class, the attributes are loaded
    from the DB.

    Legacy MISP provides subclasses for each triggers, but
    since the properties were saved into the database anyways
    and no behavior was added to those classes, the idea was
    dropped entirely in MMISP.
    """

    scope: str
    """
    Scope the trigger operates on. E.g. `event` or `attribute`.
    """

    description: str = ""
    """
    Human-readable description of when the trigger gets executed.
    """

    overhead: "Overhead"
    """
    Indicates the expensiveness/overhead of the trigger
    as indicated by the [`Overhead`][mmisp.workflows.modules.Overhead] enum.
    """

    overhead_message: str = ""
    """
    Explanatory message describing why the overhead level was chosen
    for this trigger.
    """

    icon: str = "envelope"
    """
    Frontend icon.
    """

    disabled: bool = False
    """
    Whether or not the trigger is disabled, i.e. ignored when triggered.
    """

    n_inputs: int = 0

    async def normalize_data(self: Self, db: AsyncSession, input: VerbatimWorkflowInput) -> "RoamingData":
        """
        Allows triggers to perform custom "normalization" operations
        before handing over to the actual modules.

        Workflow input can be an arbitrary JSON already, but it can also be
        a SQLAlchemy model. In the latter case it's this method's responsibility
        to transform it into MISP compliant data.

        Arguments:
            db:     DB handle to load more entities from the database.
            input:  Workflow input to modify.
        """

        # if a different model is provided here, you need
        # a custom implementation.
        assert isinstance(input, dict), (
            "No dict was passed to default normalize_data implementation of a trigger. "
            f"Override your trigger if other inputs shall be accepted. Got: {type(input)}"
        )

        return input


@dataclass
class Frame:
    """
    Value object representing a frame in the visual editor. Only for visualization.
    """

    text: str
    """
    Title of the frame
    """

    uuid: UUID
    """
    Unique identifier of the frame. Used by the visual editor.
    """

    clazz: str
    """
    Additional CSS classes for the frame. `class` is a reserved keyword.
    """

    nodes: List[Node]
    """
    List of (references) to nodes that are visually encapsulated in the frame
    in the visual editor.
    """


@dataclass
class Graph(ABC):
    """
    A representation of a workflow graph. Consists of
    """

    nodes: Dict[int, Trigger | Module]
    """
    A list of all nodes inside the graph. Edges are represented by nodes
    having references to other nodes in their
    `inputs`/`outputs`.
    """

    root: Trigger | Module
    """
    Reference to the root of the graph.
    """

    frames: Iterable[Frame]
    """
    List of frame objects in the visual editor.
    """

    def __check_nodes(self: Self, storage: GraphValidationResult) -> None:
        for node_id, node in self.nodes.items():
            storage.add_result(node.check())

    def __check_input_adjacency_list_correspond_to_output_one(self: Self, storage: GraphValidationResult) -> None:
        for node_id, node in self.nodes.items():
            for input_port_id, connections in node.inputs.items():
                for connection in connections:
                    list_outgoing = connection[1].outputs.get(connection[0])
                    if list_outgoing is None:
                        storage.errors.append(
                            InconsistentEdgeBetweenAdjacencyLists(connection[1], connection[0], node, input_port_id)
                        )
                    elif (input_port_id, node) not in list_outgoing:
                        storage.errors.append(
                            InconsistentEdgeBetweenAdjacencyLists(connection[1], connection[0], node, input_port_id)
                        )

            for output_port_id, connections in node.outputs.items():
                for connection in connections:
                    list_incoming = connection[1].inputs.get(connection[0])
                    if list_incoming is None:
                        storage.errors.append(
                            InconsistentEdgeBetweenAdjacencyLists(node, output_port_id, connection[1], connection[0])
                        )
                    elif (output_port_id, node) not in list_incoming:
                        storage.errors.append(
                            InconsistentEdgeBetweenAdjacencyLists(node, output_port_id, connection[1], connection[0])
                        )

    def __acyclic_check_dfs(self: Self, current: Node, storage: GraphValidationResult) -> None:
        for output_id, connections in current.outputs.items():
            for connection in connections:
                next_node_state = self.__visited.get(connection[1])
                if next_node_state is None:
                    self.__visited[connection[1]] = False
                    self.__parent[connection[1]] = (current, output_id, connection[0])
                    self.__acyclic_check_dfs(connection[1], storage)
                elif not next_node_state:
                    error = CyclicGraphError([])
                    error.cycle_path.append((current, output_id, connection[1], connection[0]))
                    current_node_loop = current
                    while current_node_loop is not connection[1]:
                        parent_node = self.__parent.get(current_node_loop)
                        assert parent_node is not None
                        error.cycle_path.append((parent_node[0], parent_node[1], current_node_loop, parent_node[2]))
                        current_node_loop = parent_node[0]
                    storage.errors.append(error)
        self.__visited[current] = True

    def __check_is_graph_acyclic(self: Self, storage: GraphValidationResult) -> None:
        self.__visited: Dict[Node, bool] = {}
        self.__parent: Dict[Node, Tuple[Node, int, int]] = {}
        for node_id, node in self.nodes.items():
            if self.__visited.get(node) is None:
                self.__visited[node] = False
                self.__acyclic_check_dfs(node, storage)

    @abstractmethod
    def check(self: Self) -> GraphValidationResult:
        """
        Checks if the graph's structure is valid. Works as described in
        [`GraphValidationResult`][mmisp.workflows.graph.GraphValidationResult].
        """
        storage = GraphValidationResult([])
        self.__check_is_graph_acyclic(storage)
        self.__check_input_adjacency_list_correspond_to_output_one(storage)
        self.__check_nodes(storage)
        return storage

    async def initialize_graph_modules(self: Self, db: AsyncSession) -> None:
        """
        This method is declared in `mmisp.workflows.modules`, but
        is a method of is part of [`Graph`][mmisp.workflows.graph.Graph].
        It injects `db` into each module. This is done to avoid
        circular import situations.

        !!! note
            For now, this is necessary since modules may require other
            objects from the database. E.g. the
            [`ModuleOrganisationIf`][mmisp.workflows.modules.ModuleOrganisationIf]
            loads the names of all organisations.

            There are a few ways forward:

            * Implement a more sophisticated SQLAlchemy type that
              allows to query other entities while placing the JSON
              into the [`Graph`][mmisp.workflows.graph.Graph] structure.

            * Factor the :attribute:`mmisp.workflows.modules.Module.params`
              structure out and inject it into the workflow editor on its own.

            For modernizing legacy MISP's workflows and retaining backwards
            compatibility, just injecting the DB into each node at the
            beginning is the simplest solution though.

        Arguments:
            db: SQLAlchemy DB session.
        """
        for node in self.nodes.values():
            if isinstance(node, Module):
                await node.initialize_for_visual_editor(db)
                assert node.is_initialized_for_visual_editor()


class WorkflowGraph(Graph):
    """
    This graph represents a workflow. That means that it MUST have a trigger as starting
    node and no trigger anywhere else.
    """

    def check(self: Self) -> GraphValidationResult:
        result = super().check()
        if not isinstance(self.root, Trigger):
            result.errors.append(MissingTrigger())
        for node_id, node in self.nodes.items():
            if (node is not self.root) and isinstance(node, Trigger):
                result.errors.append(
                    ConfigurationError(
                        node,
                        "This node is a trigger and not the root node. Only the"
                        + " root is allowed (and must be) a trigger in a workflow.",
                    )
                )
        return result


class BlueprintGraph(Graph):
    """
    This graph represents a blueprint. Blueprints are reusable parts of a
    workflow graph and MUST NOT have a trigger.

    Whether that's the case can be enforced with the
    [`BlueprintGraph.check`][mmisp.workflows.graph.BlueprintGraph.check] method.
    """

    def check(self: Self) -> GraphValidationResult:
        """
        Custom check method for blueprint graph.
        """
        result = super().check()
        for node_id, node in self.nodes.items():
            if isinstance(node, Trigger):
                result.errors.append(ConfigurationError(node, "Trigger nodes are not allowed in blueprints."))
        return result
