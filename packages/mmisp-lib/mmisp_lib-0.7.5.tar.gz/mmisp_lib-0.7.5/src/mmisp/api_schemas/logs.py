from pydantic import BaseModel


class LogsRequest(BaseModel):
    model: str | None = None
    action: str | None = None
    model_id: int | None = None
    page: int = 1
    limit: int = 50
