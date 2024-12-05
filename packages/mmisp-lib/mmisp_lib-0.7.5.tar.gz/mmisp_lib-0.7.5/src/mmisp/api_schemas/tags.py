from pydantic import BaseModel, Field

import mmisp.api_schemas.taxonomies
from mmisp.api_schemas.common import TagAttributesResponse


class TagUpdateBody(BaseModel):
    name: str | None = None
    colour: str | None = None
    exportable: bool | None = None
    org_id: int | None = None
    user_id: int | None = None
    hide_tag: bool | None = None
    numerical_value: str | None = None
    local_only: bool | None = None

    class Config:
        orm_mode = True


class TaxonomyPredicateResponse(mmisp.api_schemas.taxonomies.TaxonomyPredicateSchema):
    id: int
    taxonomy_id: int
    colour: str
    exclusive: bool
    numerical_value: int


class TagCombinedModel(BaseModel):
    Tag: TagAttributesResponse
    Taxonomy: mmisp.api_schemas.taxonomies.TaxonomyView
    TaxonomyPredicate: TaxonomyPredicateResponse


class TagSearchResponse(BaseModel):
    response: list[TagCombinedModel]

    class Config:
        orm_mode = True


class TagGetResponse(BaseModel):
    Tag: list[TagAttributesResponse]

    class Config:
        orm_mode = True


class TagResponse(BaseModel):
    Tag: TagAttributesResponse


class TagViewResponse(TagAttributesResponse):
    count: int
    attribute_count: int


class TagDeleteResponse(BaseModel):
    name: str
    message: str
    url: str

    class Config:
        orm_mode = True


class TagCreateBody(BaseModel):
    name: str = Field(min_length=1)
    colour: str = Field(min_length=7, max_length=7)
    exportable: bool
    org_id: int | None = None
    user_id: int | None = None
    hide_tag: bool | None = None
    numerical_value: str | None = None
    local_only: bool | None = None

    class Config:
        orm_mode = True
