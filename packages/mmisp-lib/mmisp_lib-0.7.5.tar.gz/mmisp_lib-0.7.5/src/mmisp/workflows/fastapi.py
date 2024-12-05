"""
API schemas for workflows. No classes here, just transformers.

Intended use for incoming JSON is

```python
async def update_workflow(
    workflow: Annotated[Workflow, Depends(json_dict_to_workflow_entity)]
):
    pass
```

and for returning a JSON representation for a workflow:
```python
async def get_workflow(
    ...
) -> Annotated[Workflow, Depends(workflow_entity_to_json_dict)]:
    pass
```
"""

from json import dumps
from typing import Any, Dict

from fastapi import HTTPException

from mmisp.db.models.log import Log
from mmisp.workflows.graph import Node
from mmisp.workflows.modules import Module, Trigger

from ..db.models.workflow import Workflow
from ..workflows.legacy import GraphFactory


def json_dict_to_workflow_entity(input: Dict[str, Dict[str, Any]]) -> Workflow:
    if "Workflow" not in input:
        raise HTTPException(status_code=400, detail="JSON body must contain a 'Workflow' key!")

    workflow_data = input["Workflow"]
    try:
        return Workflow(
            id=workflow_data["id"],
            uuid=workflow_data["uuid"],
            name=workflow_data["name"],
            description=workflow_data["description"],
            timestamp=workflow_data["timestamp"],
            enabled=workflow_data["enabled"],
            counter=workflow_data["counter"],
            trigger_id=workflow_data["trigger_id"],
            debug_enabled=workflow_data["debug_enabled"],
            data=GraphFactory.jsondict2graph(workflow_data["data"]),
        )
    except KeyError as ke:
        raise HTTPException(status_code=400, detail=f"Missing attribute {ke} in workflow JSON body")


def workflow_entity_to_json_dict(workflow: Workflow) -> Dict[str, Dict[str, Any]]:
    graph_json = GraphFactory.graph2jsondict(workflow.data)  # type:ignore [arg-type]
    return {
        "Workflow": {
            "id": str(workflow.id),
            "uuid": workflow.uuid,
            "name": workflow.name,
            "description": workflow.description,
            "timestamp": workflow.timestamp,
            "enabled": workflow.enabled,
            "counter": workflow.counter,
            "trigger_id": workflow.trigger_id,
            "debug_enabled": workflow.debug_enabled,
            "data": graph_json,
            "listening_triggers": [graph_json[next(iter(graph_json))]["data"]],
        }
    }


def module_entity_to_json_dict(module: Module | Trigger) -> Dict[str, Any]:
    if isinstance(module, Module):
        assert module.is_initialized_for_visual_editor()
    return {
        "version": module.version,
        "blocking": module.blocking,
        "id": module.id,
        "name": module.name,
        "description": module.description,
        "icon": module.icon,
        "inputs": module.n_inputs,
        "outputs": module.n_outputs,
        "support_filters": __get_support_filters(module),
        "expect_misp_core_format": False,
        # ignoring the type error here: we already made sure that the
        # module is initialized and thus params is a dict.
        "params": list(module.params.values()) if hasattr(module, "params") else [],  # type:ignore[union-attr]
        "is_misp_module": False,
        "is_custom": False,
        "icon_class": "",
        "multiple_output_connection": module.enable_multiple_edges_per_output,
        "saved_filters": [],  # FIXME: idk what that is :(
        "module_type": "action",
        "disabled": False,  # FIXME: not implemented!
    }


def trigger_entity_to_json_dict(trigger: Trigger, workflow: Dict[str, Any], disabled: bool) -> Dict[str, Any]:
    return {
        "id": trigger.id,
        "scope": trigger.scope,
        "name": trigger.name,
        "description": trigger.description,
        "icon": trigger.icon,
        "inputs": trigger.n_inputs,
        "outputs": trigger.n_outputs,
        "blocking": trigger.blocking,
        "misp_core_format": False,
        "trigger_overhead": trigger.overhead,
        "trigger_overhead_message": trigger.overhead_message,
        "is_misp_module": False,
        "is_custom": False,
        "expect_misp_core_format": False,
        "version": trigger.version,
        "icon_class": "",
        "multiple_output_connection": trigger.enable_multiple_edges_per_output,
        "support_filters": __get_support_filters(trigger),
        "saved_filters": [],
        "params": __get_config(trigger),
        "module_type": "trigger",
        "html_template": "trigger",
        "disabled": disabled,
        "Workflow": workflow,
    }


def __get_config(node: Node) -> str:
    config = "[]"  # FIXME: is list
    if hasattr(node, "configuration"):
        config = dumps(node.configuration.data)
    return config


def __get_support_filters(node: Node) -> bool:
    support_filters = False
    if hasattr(node, "on_demand_filtering_enabled"):
        support_filters = node.on_demand_filtering_enabled
    return support_filters


def log_to_json_dict(log: Log) -> Dict[str, Any]:
    return {
        "Log": {
            "id": str(log.id),
            "title": log.title,
            "created": log.created,
            "model": log.model,
            "model_id": str(log.model_id),
            "action": log.action,
            "user_id": str(log.user_id),
            "change": log.change,
            "email": log.email,
            "org": log.org,
            "description": log.description,
            "ip": log.ip,
        }
    }
