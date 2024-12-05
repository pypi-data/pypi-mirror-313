from typing import Any, Optional

from pydantic import BaseModel


class GraphRequest(BaseModel):
    workflow_graph: dict


class WorkflowEditRequest(BaseModel):
    # workflow_name: str
    # workflow_description: str
    # workflow_graph: dict
    data: Any


class ModuleIndexRequest(BaseModel):
    enabled: Optional[bool] = None
    type: str = "action"
    actiontype: str = "all"
    limit: int = 50
    page: int = 1


class TriggerRequest(BaseModel):
    scope: Optional[str] = None
    enabled: Optional[bool] = None
    blocking: Optional[bool] = None
    limit: int = 50
    page: int = 1
