from datetime import datetime

from pydantic import BaseModel

from mmisp.api_schemas.organisations import Organisation, OrganisationUsersResponse
from mmisp.api_schemas.roles import Role, RoleUsersResponse


class User(BaseModel):
    id: int
    org_id: int
    email: str
    autoalert: bool
    invited_by: int
    gpgkey: str | None = None
    certif_public: str | None = None
    termsaccepted: bool
    role_id: int
    change_pw: bool
    contactalert: bool
    disabled: bool
    expiration: datetime | int | None = None
    current_login: int
    """time in seconds"""
    last_login: int
    """time in seconds"""
    force_logout: bool
    date_created: int
    """time in seconds"""
    date_modified: int
    """time in seconds"""
    external_auth_required: bool
    external_auth_key: str | None = None
    last_api_access: int
    """time in seconds"""
    notification_daily: bool
    notification_weekly: bool
    notification_monthly: bool
    totp: str | None = None
    hotp_counter: int | None = None
    last_pw_change: int | None = None
    """time in seconds"""


class Config:
    orm_mode = True


class UserAttributesBody(BaseModel):
    org_id: int | None = None
    authkey: str | None = None
    email: str | None = None
    autoalert: bool | None = None
    gpgkey: str | None = None
    certif_public: str | None = None
    termsaccepted: bool | None = None
    role_id: str | None = None
    change_pw: bool | None = None
    contactalert: bool | None = None
    disabled: bool | None = None
    expiration: datetime | str | None = None
    force_logout: bool | None = None
    external_auth_required: bool | None = None
    external_auth_key: str | None = None
    notification_daily: bool | None = None
    notification_weekly: bool | None = None
    notification_monthly: bool | None = None
    totp: str | None = None
    hotp_counter: str | None = None
    name: str | None = None
    nids_sid: int | None = None


class AddUserBody(BaseModel):
    authkey: str
    contactalert: bool
    nids_sid: int
    org_id: int
    email: str
    termsaccepted: bool
    disabled: bool
    notification_daily: bool
    notification_weekly: bool
    notification_monthly: bool
    password: str
    name: str
    """role_id newly added"""
    role_id: str


class AddUserResponseData(BaseModel):
    id: int
    org_id: int
    server_id: int
    email: str
    autoalert: bool
    authkey: str
    invited_by: int
    gpgkey: str | None = None
    certif_public: str | None = None
    nids_sid: int
    termsaccepted: bool
    newsread: int | None = None
    role_id: int
    change_pw: bool
    contactalert: bool
    disabled: bool
    expiration: int | None = None
    current_login: int
    force_logout: bool
    date_created: int
    date_modified: int
    sub: str | None = None
    external_auth_required: bool
    external_auth_key: str | None = None
    last_api_access: int
    notification_daily: bool
    notification_weekly: bool
    notification_monthly: bool
    totp: str | None = None
    hotp_counter: int | None = None
    last_pw_change: int | None = None


class AddUserResponse(BaseModel):
    User: AddUserResponseData


class GetUsersUser(BaseModel):
    id: int
    org_id: int
    server_id: int = 0
    email: str
    autoalert: bool
    auth_key: str | None
    invited_by: int
    gpg_key: str | None
    certif_public: str | None
    nids_sid: int
    termsaccepted: bool
    newsread: int | None
    role_id: int
    change_pw: bool
    contactalert: bool
    disabled: bool
    expiration: int | None
    current_login: int | None
    last_login: int | None
    last_api_access: int | None
    force_logout: bool
    date_created: int | None
    date_modified: int | None
    last_pw_change: int | None
    totp: str | None
    """detailed information bellow"""
    hotp_counter: int | None
    notification_daily: bool | None
    notification_weekly: bool | None
    notification_monthly: bool | None
    external_auth_required: bool | None
    external_auth_key: str | None
    sub: str | None
    """new contents bellow"""  # not in the database, all 3 fields to none now, so no error will be raised
    name: str | None
    contact: bool | None
    notification: bool | None


class GetUsersElement(BaseModel):
    User: GetUsersUser
    Role: RoleUsersResponse
    Organisation: OrganisationUsersResponse
    UserSetting: dict | None = None


class GetAllUsersResponse(BaseModel):
    users: list[GetUsersElement]


class UserWithName(BaseModel):
    user: User
    name: str


class UsersViewMeResponse(BaseModel):
    User: User
    Role: Role
    UserSetting: list = []
    Organisation: Organisation


class ServerUser(BaseModel):
    id: int
    org_id: int
    email: str
    server_id: int
