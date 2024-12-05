from typing import Any, Dict, Type

from pydantic import BaseModel, Field, validator


class FeedUpdateBody(BaseModel):
    name: str | None = None
    provider: str | None = None
    url: str | None = None
    rules: str | None = None
    enabled: bool | None = None
    distribution: str | None = None
    sharing_group_id: int | None = None
    tag_id: int | None = None
    default: bool | None = None
    source_format: str | None = None
    fixed_event: bool | None = None
    delta_merge: bool | None = None
    event_id: int | None = None
    publish: bool | None = None
    override_ids: bool | None = None
    settings: str | None = None
    input_source: str | None = None
    delete_local_file: bool | None = None
    lookup_visible: bool | None = None
    headers: str | None = None
    caching_enabled: bool | None = None
    force_to_ids: bool | None = None
    orgc_id: int | None = None

    class Config:
        orm_mode = True


class FeedToggleBody(BaseModel):
    enable: bool

    class Config:
        orm_mode = True


class FeedAttributesResponse(BaseModel):
    id: int
    name: str
    provider: str
    url: str
    rules: str | None = None
    enabled: bool | None = None
    distribution: str
    sharing_group_id: int | None = None
    tag_id: int
    default: bool | None = None
    source_format: str | None = None
    fixed_event: bool
    delta_merge: bool
    event_id: int
    publish: bool
    override_ids: bool
    settings: str | None = None
    input_source: str
    delete_local_file: bool | None = None
    lookup_visible: bool | None = None
    headers: str | None = None
    caching_enabled: bool
    force_to_ids: bool
    orgc_id: int

    @validator("sharing_group_id", always=True)
    @classmethod
    def check_sharing_group_id(cls: Type["FeedAttributesResponse"], value: Any, values: Dict[str, Any]) -> int | None:
        """
        If distribution equals 4, sharing_group_id will be shown.
        """
        distribution = values.get("distribution", None)
        if distribution == "4" and value is not None:
            return value
        return None


class FeedResponse(BaseModel):
    Feed: FeedAttributesResponse

    class Config:
        orm_mode = True


class FeedFetchResponse(BaseModel):
    result: str

    class Config:
        orm_mode = True


class FeedEnableDisableResponse(BaseModel):
    name: str
    message: str
    url: str

    class Config:
        orm_mode = True


class FeedCreateBody(BaseModel):
    name: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    url: str = Field(min_length=1)
    rules: str | None = None
    enabled: bool | None = None
    distribution: str | None = None
    sharing_group_id: str | None = None
    tag_id: int | None = None
    default: bool | None = None
    source_format: str | None = None
    fixed_event: bool | None = None
    delta_merge: bool | None = None
    event_id: int | None = None
    publish: bool | None = None
    override_ids: bool | None = None
    settings: str | None = None
    input_source: str | None = None
    delete_local_file: bool | None = None
    lookup_visible: bool | None = None
    headers: str | None = None
    caching_enabled: bool | None = None
    force_to_ids: bool | None = None
    orgc_id: int | None = None

    class Config:
        orm_mode = True


class FeedCacheResponse(BaseModel):
    name: str
    message: str
    url: str
    saved: bool
    success: bool

    class Config:
        orm_mode = True
