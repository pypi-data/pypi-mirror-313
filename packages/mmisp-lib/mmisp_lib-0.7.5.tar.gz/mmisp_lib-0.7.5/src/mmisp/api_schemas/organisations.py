from datetime import datetime
from typing import Self

from pydantic import BaseModel

from mmisp.lib.serialisation_helper import timestamp_or_empty_string


class BaseOrganisation(BaseModel):
    id: int | None = None
    name: str | None = None
    nationality: str | None = None
    sector: str | None = None
    type: str | None = None
    uuid: str | None = None


class Organisation(BaseOrganisation):
    date_created: datetime | str
    date_modified: datetime | str
    description: str | None = None
    created_by: str
    contacts: str | None = None
    local: bool
    """organisation gains access to the local instance, otherwise treated as external"""
    restricted_to_domain: str | list | None = None
    landingpage: str | None = None

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}


class GetOrganisationResponse(BaseModel):
    id: int
    name: str
    nationality: str | None = None
    sector: str | None = None
    type: str | None = None
    uuid: str | None = None
    # the fallback GENERIC_MISP_ORGANISATION doesn't have this property
    # str is needed because its returned as string
    date_created: datetime | None | str = None
    date_modified: datetime | None | str = None
    description: str | None = None
    created_by: str
    contacts: str | None = None
    local: bool
    restricted_to_domain: str | list | None = None
    landingpage: str | None = None

    def dict(self: Self, *args, **kwargs) -> dict:
        d = super().dict(*args, **kwargs)

        d["date_created"] = timestamp_or_empty_string(d["date_created"])
        d["date_modified"] = timestamp_or_empty_string(d["date_modified"])

        return d


class GetAllOrganisationsOrganisation(GetOrganisationResponse):
    user_count: int
    created_by_email: str


class GetAllOrganisationResponse(BaseModel):
    Organisation: GetAllOrganisationsOrganisation


class DeleteForceUpdateOrganisationResponse(BaseModel):
    saved: bool | None = None
    success: bool | None = None
    name: str
    message: str
    url: str

    class Config:
        orm_mode = True


class OrganisationUsersResponse(BaseModel):
    id: int
    name: str
    date_created: datetime | str | None = None
    date_modified: datetime | str | None = None
    description: str | None = None
    type: str | None = None
    nationality: str | None = None
    sector: str | None = None
    created_by: int | None = None
    uuid: str | None = None
    contacts: str | None = None
    local: bool | None = None
    restricted_to_domain: str | list | None = None
    landingpage: str | None = None


class AddOrganisation(BaseModel):
    id: int
    name: str
    description: str | None = None
    type: str
    nationality: str | None = None
    sector: str | None = None
    created_by: str
    contacts: str | None = None
    local: bool
    """organisation gains access to the local instance, otherwise treated as external"""
    restricted_to_domain: str | None = None
    landingpage: str | None = None

    class Config:
        orm_mode = True


class EditOrganisation(BaseModel):
    name: str
    description: str | None = None
    type: str
    nationality: str | None = None
    sector: str | None = None
    contacts: str | None = None
    local: bool
    """organisation gains access to the local instance, otherwise treated as external"""
    restricted_to_domain: str | None = None
    landingpage: str | None = None

    class Config:
        orm_mode = True


class ShadowAttributeOrganisation(BaseModel):
    name: str
    uuid: str
    id: int


class ServerOrganisation(BaseModel):
    id: int
    name: str
    uuid: str
    nationality: str
    sector: str
    type: str
