from pydantic import BaseModel


class Position(BaseModel):
    x: str
    y: str
    width: str
    height: str


class Value(BaseModel):
    widget: str
    position: Position


class ViewUserSettingResponseUserSetting(BaseModel):
    id: int
    setting: str
    value: dict | list
    user_id: int
    timestamp: str


class ViewUserSettingResponse(BaseModel):
    UserSetting: ViewUserSettingResponseUserSetting


class SetUserSettingResponseUserSetting(BaseModel):
    id: int
    setting: str
    value: dict | list
    user_id: int
    timestamp: str


class SetUserSettingResponse(BaseModel):
    UserSetting: SetUserSettingResponseUserSetting


class SetUserSettingBody(BaseModel):
    value: dict | list


class SearchUserSettingResponse(BaseModel):
    id: int
    setting: str
    value: Value
    user_id: int
    timestamp: str


class SearchUserSettingBody(BaseModel):
    id: int | None = None
    setting: str | None = None
    user_id: int | None = None


class UserSettingSchema(BaseModel):
    id: int
    setting: str
    value: dict | list
    user_id: int
    timestamp: str


class UserSettingResponse(BaseModel):
    UserSetting: UserSettingSchema


class GetUserSettingResponse(BaseModel):
    id: int
    setting: str
    value: str
    user_id: int
    timestamp: str
