from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel


class NoticelistAttributes(BaseModel):
    id: int
    name: str
    expanded_name: str
    ref: list[str]
    geographical_area: list[str]
    version: str
    enabled: bool


class Data(BaseModel):
    scope: str | list[str] | None
    field: str | list[str] | None
    value: str | list[str] | None
    tags: str | list[str] | None
    message: str | Any


class NoticelistEntryResponse(BaseModel):
    id: int
    noticelist_id: int
    data: Data


class NoticelistAttributesResponse(NoticelistAttributes):
    NoticelistEntry: Sequence[NoticelistEntryResponse]


class GetAllNoticelists(BaseModel):
    Noticelist: NoticelistAttributes

    class Config:
        orm_mode = True


class NoticelistResponse(BaseModel):
    Noticelist: NoticelistAttributesResponse

    class Config:
        orm_mode = True
