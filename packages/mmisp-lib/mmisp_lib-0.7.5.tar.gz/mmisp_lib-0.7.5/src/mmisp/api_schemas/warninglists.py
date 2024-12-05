from enum import StrEnum

from pydantic import BaseModel, Field

from mmisp.lib.attributes import literal_valid_attribute_types


class WarninglistCategory(StrEnum):
    FALSE_POSITIVE = "False positive"
    KNOWN_IDENTIFIER = "Known identifier"


class WarninglistListType(StrEnum):
    CIDR = "cidr"
    HOSTNAME = "hostname"
    STRING = "string"
    SUBSTRING = "substring"
    REGEX = "regex"


class WarninglistTypeResponse(BaseModel):
    id: int
    type: str
    warninglist_id: int


class WarninglistEntryResponse(BaseModel):
    id: int
    value: str = Field(max_length=65535)
    warninglist_id: int
    comment: str | None = None


class WarninglistBaseResponse(BaseModel):
    id: int
    name: str = Field(max_length=255)
    type: str
    description: str = Field(max_length=65535)
    version: str
    enabled: bool
    default: bool
    category: str


class WarninglistAttributesResponse(WarninglistBaseResponse):
    WarninglistEntry: list[WarninglistEntryResponse] | None = None
    WarninglistType: list[WarninglistTypeResponse] | None = None


class WarninglistResponse(BaseModel):
    Warninglist: WarninglistAttributesResponse

    class Config:
        orm_mode = True


class WarninglistAttributes(WarninglistBaseResponse):
    warninglist_entry_count: str
    valid_attributes: str


class ToggleEnableWarninglistsResponse(BaseModel):
    saved: bool
    success: str | None = None
    errors: str | None = None

    class Config:
        orm_mode = True


class ToggleEnableWarninglistsBody(BaseModel):
    id: int | list[int]
    name: str | list[str]
    enabled: bool

    class Config:
        orm_mode = True


class GetSelectedWarninglistsBody(BaseModel):
    value: str | None = None
    enabled: bool | None = None

    class Config:
        orm_mode = True


class WarninglistsResponse(BaseModel):
    Warninglist: WarninglistAttributes


class GetSelectedAllWarninglistsResponse(BaseModel):
    Warninglists: list[WarninglistsResponse]

    class Config:
        orm_mode = True


class DeleteWarninglistResponse(BaseModel):
    saved: bool
    success: bool
    id: int
    name: str
    message: str
    url: str

    class Config:
        orm_mode = True


class CreateWarninglistBody(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    type: WarninglistListType
    description: str = Field(min_length=1, max_length=65535)
    enabled: bool
    default: bool
    category: WarninglistCategory
    valid_attributes: list[literal_valid_attribute_types]  # type:ignore[valid-type]
    values: str = Field(min_length=1, max_length=65535)

    class Config:
        orm_mode = True


class NameWarninglist(BaseModel):
    id: int
    name: str
    matched: str


class CheckValueResponse(BaseModel):
    value: list[NameWarninglist]

    class Config:
        orm_mode = True


class CheckValueWarninglistsBody(BaseModel):
    value: str

    class Config:
        orm_mode = True
