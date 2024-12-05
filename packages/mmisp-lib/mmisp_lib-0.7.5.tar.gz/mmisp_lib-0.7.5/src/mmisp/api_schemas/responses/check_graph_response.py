from typing import Dict, List

from pydantic import BaseModel


class IsAcyclicInfo(BaseModel):
    nodeID1: int
    nodeID2: int
    cycle: str = "Cycle"


class IsAcyclic(BaseModel):
    """
    Represents the whether graph is acyclic and details of the first detected cycle.

    - **is_acyclic**: False if the graph contains at least one cycle.
    - **cycles**: A list of entries, each containing two node IDs and a "Cycle" string.
    Conbined they result in the cycle.

    Example:
    ```json
    "is_acyclic": {
        "is_acyclic": false,
        "cycles": [
            [
                4,
                3,
                "Cycle"
            ],
            [
                3,
                4,
                "Cycle"
            ]
        ]
    }
    ```
    """

    is_acyclic: bool
    cycles: List[IsAcyclicInfo]


class MultipleOutputConnection(BaseModel):
    """
    Represents the status and details of nodes with illegal multiple output connections in a graph.

    - **has_multiple_output_connection**: True if at least one node has multiple output
      connections that are not allowed.
      For example, the 'Concurrent Task' node can have multiple output connections while the value here is `False`.
    - **edges**: A dictionary where the key is the ID of a node with multiple illegal connections,
      and the value is a list of node IDs to which these illegal connections are made.

    Example:
    ```json
    "multiple_output_connection": {
        "has_multiple_output_connection": true,
        "edges": {
            "1": [
                5,
                3
            ]
        }
    }
    ```
    """

    has_multiple_output_connection: bool
    edges: Dict[int, List[int]]


class PathWarningsInfo(BaseModel):
    source_id: int  # is a string in legacy misp
    next_node_id: int  # is a string in legacy misp
    warning: str
    blocking: bool
    module_name: str
    module_id: int


class PathWarnings(BaseModel):
    """
    Represents warnings for paths in a graph.

    - **has_path_warnings**: True if the graph contains at least one warning.
    - **edges**: A list containing all connections which are flagged as warnings.

    Example:
    ```json
    "path_warnings": {
        "has_path_warnings": true,
        "edges": [
            [
                5,
                2,
                "This path leads to a blocking node from a non-blocking context",
                true,
                "stop-execution",
                2
            ]
        ]
    }
    ```
    """

    has_path_warnings: bool
    edges: List[PathWarningsInfo]


class MiscellaneousGraphValidationError(BaseModel):
    """
    Validation errors that do no fit in the legacy MISP json response format for Graph Validation will be returned as
    errors in this format.
    """

    error_id: str
    """
    The type of error that this instance represents.
    """

    message: str
    """
    The error message of this instance.
    """


class CheckGraphResponse(BaseModel):
    """
    Response schema from the API for checking a graph.

    - **is_acyclic**: Indicates whether the graph is acyclic and provides information
      about the first detected cycle, if any.
    - **multiple_output_connection**: Indicates whether the graph has illegal multiple output connections,
    detailing the nodes involved.
    - **path_warnings**: Records warnings if a path leads to a blocking node from a
      'Concurrent Task' node, providing relevant details. Not used in Modern MISP, and will be returned empty.
    - **unsupported_modules"" List of the modules (identified with their graph_id) that are currently unsupported in
      Modern MISP (not yet implemented) causing the workflow to be invalid.
    - **misc_errors** Other miscellaneous errors indicating that the workflow graph is broken or etc. (edges registered
    at ports outside the valid range, inconsistencies between the incoming and outgoing adjacency lists etc.)

    Example JSON structure:
    ```json
    {
        "is_acyclic": {
            "is_acyclic": false,
            "cycles": [
                [4, 3, "Cycle"],
                [3, 4, "Cycle"]
            ]
        },
        "multiple_output_connection": {
            "has_multiple_output_connection": true,
            "edges": {
                "1": [5, 3]
            }
        },
        "path_warnings": {
            "has_path_warnings": true,
            "edges": [
                [5, 2, "This path leads to a blocking node from a non-blocking context", true, "stop-execution", 2]
            ]
        }
    }
    ```
    """

    is_acyclic: IsAcyclic
    multiple_output_connection: MultipleOutputConnection
    path_warnings: PathWarnings
    unsupported_modules: List[int]
    misc_errors: List[MiscellaneousGraphValidationError]
