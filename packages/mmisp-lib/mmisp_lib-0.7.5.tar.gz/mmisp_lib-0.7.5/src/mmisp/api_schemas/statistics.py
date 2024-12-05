from pydantic import BaseModel


class UsageDataResponseModel(BaseModel):
    events: int
    attributes: int
    eventAttributes: int
    users: int
    usersWithGPGKeys: int
    organisations: int
    localOrganisations: int
    eventCreatorOrgs: int
    averageUsersPerOrg: float


class OrgDataResponseModel(BaseModel):
    users: int
    events: int
    attributes: int
