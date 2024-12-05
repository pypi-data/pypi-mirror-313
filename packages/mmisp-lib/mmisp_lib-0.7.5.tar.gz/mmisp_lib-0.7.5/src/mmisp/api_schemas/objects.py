from typing import Any, Dict, Optional, Type

from pydantic import BaseModel, Field, validator

from mmisp.api_schemas.attributes import AddAttributeBody, GetAllAttributesResponse
from mmisp.api_schemas.events import ObjectEventResponse


class ObjectSearchBody(BaseModel):
    object_name: str | None = None
    object_template_uuid: str | None = None
    object_template_version: str | None = None
    event_id: int | None = None
    category: str | None = None
    comment: str | None = None
    first_seen: str | None = None
    last_seen: str | None = None
    quick_filter: str | None = None
    timestamp: str | None = None
    event_info: str | None = None
    from_: str | None = None  # 'from' is a reserved word in Python, so an underscore is added
    to: str | None = None
    date: str | None = None
    last: str | None = None
    event_timestamp: str | None = None
    org_id: int | None = None
    uuid: str | None = None
    value1: str | None = None
    value2: str | None = None
    type: str | None = None
    object_relation: str | None = None
    attribute_timestamp: str | None = None
    to_ids: bool | None = None
    published: bool | None = None
    deleted: bool | None = None
    return_format: str | None = "json"
    limit: str | None = "25"

    @validator("limit", allow_reuse=True)
    @classmethod
    def check_limit(cls: Type["ObjectSearchBody"], value: Any) -> str:  # noqa: ANN101
        if value:
            try:
                limit_int = int(value)
            except ValueError:
                raise ValueError("'limit' must be a valid integer")

            if not 1 <= limit_int <= 500:
                raise ValueError("'limit' must be between 1 and 500")
        return value

    class Config:
        orm_mode = True


class ObjectWithAttributesResponse(BaseModel):
    id: int
    uuid: str
    name: str
    meta_category: str | None = None
    description: str | None = None
    template_uuid: str | None = None
    template_version: str | None = None
    event_id: int | None = None
    timestamp: str | None = None
    distribution: str | None = None
    sharing_group_id: int | None = None  # is none if distribution is not 4, see validator
    comment: str | None = None
    deleted: bool | None = None
    first_seen: str | None = None
    last_seen: str | None = None
    attributes: list[GetAllAttributesResponse] | None = Field(alias="Attribute", default=None)
    Event: ObjectEventResponse | None = None

    @validator("sharing_group_id", always=True)
    @classmethod
    def check_sharing_group_id(
        cls: Type["ObjectWithAttributesResponse"], value: Any, values: Dict[str, Any]
    ) -> Optional[int]:  # noqa: ANN101
        """
        If distribution equals 4, sharing_group_id will be shown.
        """
        distribution = values.get("distribution", None)
        if distribution == "4" and value is not None:
            return value
        return None

    class Config:
        allow_population_by_field_name = True


class ObjectResponse(BaseModel):
    Object: ObjectWithAttributesResponse


class ObjectSearchResponse(BaseModel):
    response: list[ObjectResponse]


class ObjectCreateBody(BaseModel):
    name: str = Field(min_length=1)
    meta_category: str | None = None
    description: str | None = None
    distribution: str | None = None
    sharing_group_id: int
    comment: str = Field(min_length=1)
    deleted: bool | None = None
    first_seen: str | None = None
    last_seen: str | None = None
    Attribute: list[AddAttributeBody] | None = None
