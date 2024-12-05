from pydantic import BaseModel


class StandartResponse(BaseModel):
    name: str
    message: str
    url: str


class StandardStatusResponse(StandartResponse):
    saved: bool
    success: bool


class StandardStatusIdentifiedResponse(StandardStatusResponse):
    id: int
