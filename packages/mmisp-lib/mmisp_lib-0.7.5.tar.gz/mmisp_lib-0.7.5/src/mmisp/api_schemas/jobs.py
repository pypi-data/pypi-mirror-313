from pydantic import BaseModel


class FreeTextProcessID(BaseModel):
    id: str


class FreeTextImportWorkerData(BaseModel):
    data: str


class FreeTextImportWorkerUser(BaseModel):
    user_id: int


class FreeTextImportWorkerBody(BaseModel):
    user: FreeTextImportWorkerUser
    data: FreeTextImportWorkerData

    class Config:
        orm_mode = True


class AddAttributeViaFreeTextImportEventResponse(BaseModel):
    event_id: str
    value: str
    original_value: str
    to_ids: str
    type: str
    category: str
    distribution: str

    class Config:
        orm_mode = True


class AddAttributeViaFreeTextImportEventBody(BaseModel):
    value: str
    returnMetaAttributes: bool

    class Config:
        orm_mode = True


class AttributeType(BaseModel):
    types: list[str]
    default_type: str
    value: str


class ProcessFreeTextResponse(BaseModel):
    attributes: list[AttributeType]
