from typing import Any, Type

from pydantic import BaseModel, validator


class SightingFiltersBody(BaseModel):
    value1: str | None = None
    value2: str | None = None
    type: str | None = None
    category: str | None = None
    from_: str | None = None  # 'from' is a reserved word in Python, so an underscore is added
    to: str | None = None
    last: str | None = None
    timestamp: str | None = None
    event_id: int | None = None
    uuid: str | None = None
    attribute_timestamp: str | None = None
    to_ids: bool | None = None
    deleted: bool | None = None
    event_timestamp: str | None = None
    eventinfo: str | None = None
    sharinggroup: list[str] | None = None
    first_seen: str | None = None
    last_seen: str | None = None
    requested_attributes: list[str] | None = None
    returnFormat: str | None = "json"
    limit: str | None = "25"

    @validator("limit")
    @classmethod
    def check_limit(cls: Type["SightingFiltersBody"], value: Any) -> str:  # noqa: ANN101
        if value is not None:
            try:
                limit_int = int(value)
            except ValueError:
                raise ValueError("limit must be a valid integer")

            if not 1 <= limit_int <= 500:
                raise ValueError("limit must be between 1 and 500")
        return value


class SightingOrganisationResponse(BaseModel):
    id: int
    uuid: str
    name: str


class SightingAttributesResponse(BaseModel):
    id: int
    uuid: str
    attribute_id: int
    attribute_uuid: str
    event_id: int | None = None
    org_id: int | None = None
    date_sighting: str | None = None
    source: str | None = None
    type: str | None = None
    Organisation: SightingOrganisationResponse | None = None


class SightingsGetResponse(BaseModel):
    sightings: list[SightingAttributesResponse]

    class Config:
        orm_mode = True


class SightingCreateBody(BaseModel):
    values: list[str]
    source: str | None = None
    timestamp: str | None = None
    filters: SightingFiltersBody | None = None

    class Config:
        orm_mode = True
