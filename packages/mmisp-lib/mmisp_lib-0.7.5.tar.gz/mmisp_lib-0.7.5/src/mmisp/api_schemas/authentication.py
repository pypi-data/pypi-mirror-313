from enum import Enum

from pydantic import BaseModel, SecretStr


class TokenResponse(BaseModel):
    token: str


class ChangeLoginInfoResponse(BaseModel):
    successful: bool


class IdentityProviderBody(BaseModel):
    name: str
    org_id: int
    active: bool
    base_url: str
    client_id: str
    client_secret: SecretStr
    scope: str | None = None


class IdentityProviderCallbackBody(BaseModel):
    code: str
    redirect_uri: str


class IdentityProviderEditBody(BaseModel):
    name: str | None = None
    org_id: int | None = None
    active: bool | None = None
    base_url: str | None = None
    client_id: str | None = None
    client_secret: SecretStr | None = None
    scope: str | None = None


class GetIdentityProviderResponse(BaseModel):
    id: int
    name: str
    org_id: int
    active: bool
    base_url: str
    client_id: str
    scope: str | None = None


class IdentityProviderInfo(BaseModel):
    id: int
    name: str
    url: str | None = None

    class Config:
        orm_mode = True


class LoginType(Enum):
    PASSWORD = "password"
    IDENTITY_PROVIDER = "idp"


class StartLoginBody(BaseModel):
    email: str


class PasswordLoginBody(BaseModel):
    email: str
    password: SecretStr


class SetPasswordBody(BaseModel):
    password: SecretStr


class ChangePasswordBody(BaseModel):
    email: str
    password: SecretStr
    oldPassword: SecretStr | None = None


class ExchangeTokenLoginBody(BaseModel):
    exchangeToken: str


class StartLoginResponse(BaseModel):
    loginType: LoginType
    identityProviders: list[IdentityProviderInfo] = []
