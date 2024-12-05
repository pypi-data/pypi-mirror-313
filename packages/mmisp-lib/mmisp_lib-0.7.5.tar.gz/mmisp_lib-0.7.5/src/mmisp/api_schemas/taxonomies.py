from pydantic import BaseModel

from mmisp.api_schemas.common import TagAttributesResponse


class TaxonomyEntrySchema(BaseModel):
    tag: str
    expanded: str
    exclusive_predicate: bool
    description: str
    existing_tag: bool | TagAttributesResponse


class TaxonomyTagEntrySchema(BaseModel):
    tag: str
    expanded: str
    exclusive_predicate: bool
    description: str
    existing_tag: bool | TagAttributesResponse
    events: int
    attributes: int


class GetTagTaxonomyResponse(BaseModel):
    id: int
    namespace: str
    description: str
    version: str
    enabled: bool
    exclusive: bool
    required: bool
    highlighted: bool
    entries: list[TaxonomyTagEntrySchema]

    class Config:
        orm_mode = True


class TaxonomyView(BaseModel):
    id: int
    namespace: str
    description: str
    version: str
    enabled: bool
    exclusive: bool
    required: bool
    highlighted: bool


class ViewTaxonomyResponse(BaseModel):
    Taxonomy: TaxonomyView
    total_count: int
    current_count: int

    class Config:
        orm_mode = True


class GetIdTaxonomyResponse(BaseModel):
    id: int
    namespace: str
    description: str
    version: str
    enabled: bool
    exclusive: bool
    required: bool
    highlighted: bool
    entries: list[TaxonomyEntrySchema]

    class Config:
        orm_mode = True


class GetIdTaxonomyResponseWrapper(BaseModel):
    Taxonomy: GetIdTaxonomyResponse


class ExportTaxonomyEntry(BaseModel):
    value: str
    expanded: str
    description: str


class TaxonomyValueSchema(BaseModel):
    predicate: str
    entry: list[ExportTaxonomyEntry]


class TaxonomyPredicateSchema(BaseModel):
    value: str
    expanded: str
    description: str


class ExportTaxonomyResponse(BaseModel):
    namespace: str
    description: str
    version: int
    exclusive: bool
    predicates: list[TaxonomyPredicateSchema]
    values: list[TaxonomyValueSchema]

    class Config:
        orm_mode = True
