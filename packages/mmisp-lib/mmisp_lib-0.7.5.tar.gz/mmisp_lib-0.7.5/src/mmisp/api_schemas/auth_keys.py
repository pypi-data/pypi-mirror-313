from typing import List, Self, Union

from pydantic import BaseModel, PositiveInt, conint, validator


class SearchGetAuthKeysResponseItemUser(BaseModel):
    id: int
    email: str


class ViewAuthKeyResponseWrapper(BaseModel):
    id: int
    uuid: str
    authkey_start: str
    authkey_end: str
    created: str
    expiration: int
    read_only: bool
    user_id: int
    comment: str
    allowed_ips: list[str] | None = None
    unique_ips: list[str] | None = []


class ViewAuthKeysResponse(BaseModel):
    AuthKey: ViewAuthKeyResponseWrapper
    User: SearchGetAuthKeysResponseItemUser


class SearchGetAuthKeysResponseItemAuthKey(BaseModel):
    id: int
    uuid: str
    authkey_start: str
    authkey_end: str
    created: str
    expiration: str
    read_only: bool
    user_id: int
    comment: str | None
    allowed_ips: list[str] | None = None
    unique_ips: list[str] | None = []


class SearchGetAuthKeysResponseAuthKey(BaseModel):
    id: int
    uuid: str
    authkey_start: str
    authkey_end: str
    created: str
    expiration: str
    read_only: bool
    user_id: str
    comment: str | None
    allowed_ips: list[str] | None = None
    unique_ips: list[str] | None = []
    last_used: str | None = None


class SearchGetAuthKeysResponseItem(BaseModel):
    AuthKey: SearchGetAuthKeysResponseItemAuthKey
    User: SearchGetAuthKeysResponseItemUser

    class Config:
        orm_mode = True


class SearchGetAuthKeysResponse(BaseModel):
    AuthKey: SearchGetAuthKeysResponseAuthKey
    User: SearchGetAuthKeysResponseItemUser

    class Config:
        orm_mode = True


class SearchAuthKeyBody(BaseModel):
    page: PositiveInt = 1
    limit: conint(gt=0, lt=500) = 25  # type: ignore
    id: int | None = None
    uuid: str | None = None
    authkey_start: str | None = None
    authkey_end: str | None = None
    created: str | None = None
    expiration: str | None = None
    read_only: bool | None = None
    user_id: int | None = None
    comment: str | None = None
    allowed_ips: str | list[str] | None = None
    last_used: str | None = None  # deprecated


class EditAuthKeyResponseAuthKey(BaseModel):
    id: int
    uuid: str
    authkey_start: str
    authkey_end: str
    created: str
    expiration: str
    read_only: bool
    user_id: int
    comment: str
    allowed_ips: str | None = None


class EditAuthKeyResponseCompleteAuthKey(BaseModel):
    id: int
    uuid: str
    authkey_start: str
    authkey_end: str
    created: str
    expiration: str
    read_only: bool
    user_id: str
    comment: str
    allowed_ips: str | None = None
    unique_ips: list[str] | None = None


class EditAuthKeyResponseUser(BaseModel):
    id: int
    org_id: int


class EditAuthKeyResponse(BaseModel):
    AuthKey: EditAuthKeyResponseAuthKey
    User: EditAuthKeyResponseUser


class EditAuthKeyResponseCompl(BaseModel):
    AuthKey: EditAuthKeyResponseCompleteAuthKey
    User: EditAuthKeyResponseUser


class EditAuthKeyBody(BaseModel):
    read_only: bool | None = None
    comment: str | None = None
    allowed_ips: Union[str, List[str]] | None = None
    expiration: str | None = None

    @validator("allowed_ips", pre=True)
    def ensure_list(cls: Self, v: str | List[str]) -> List[str]:
        if isinstance(v, str):
            return [v]
        return v


class AddAuthKeyResponseAuthKey(BaseModel):
    id: int
    uuid: str
    authkey_start: str
    authkey_end: str
    created: str
    expiration: str | None = "0"
    read_only: bool
    user_id: int
    comment: str | None = None
    allowed_ips: list[str] | None = None
    unique_ips: list[str]
    authkey_raw: str


class AddAuthKeyResponse(BaseModel):
    AuthKey: AddAuthKeyResponseAuthKey


class AddAuthKeyBody(BaseModel):
    uuid: str | None = None
    read_only: bool | None = None
    user_id: int | None = None
    comment: str | None = None
    allowed_ips: list[str] | None = None
    expiration: int | str | None = 0
