from datetime import datetime
from typing import Any, Type

from pydantic import BaseModel, PositiveInt, conint, validator

from mmisp.api_schemas.organisations import Organisation
from mmisp.lib.distribution import DistributionLevels


class GetAllEventsGalaxyClusterGalaxy(BaseModel):
    id: int
    uuid: str
    name: str
    type: str
    description: str
    version: str
    icon: str
    namespace: str
    enabled: bool
    local_only: bool
    kill_chain_order: str | None = None
    created: datetime | str
    modified: datetime | str
    org_id: int
    orgc_id: int
    default: bool
    distribution: DistributionLevels


class AddEditGetEventGalaxyClusterMeta(BaseModel):
    external_id: int | None = None
    refs: list[str] | None = None
    kill_chain: str | None = None


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
    comment: str | None = None
    value: str
    original_value: str
    to_ids: str
    type: str
    category: str
    distribution: str

    class Config:
        orm_mode = True


class AddAttributeViaFreeTextImportEventAttributes(BaseModel):
    value: str


class AddAttributeViaFreeTextImportEventBody(BaseModel):
    Attribute: AddAttributeViaFreeTextImportEventAttributes

    class Config:
        orm_mode = True


class GetAllEventsGalaxyCluster(BaseModel):
    id: int
    uuid: str
    collection_uuid: str
    type: str
    value: str
    tag_name: str
    description: str
    galaxy_id: int
    source: str
    authors: list[str]
    version: str
    distribution: str | None = None
    sharing_group_id: int | None = None
    org_id: int
    orgc_id: int
    default: str | None = None
    locked: bool | None = None
    extends_uuid: str
    extends_version: str
    published: bool | None = None
    deleted: bool | None = None
    Galaxy: GetAllEventsGalaxyClusterGalaxy
    meta: AddEditGetEventGalaxyClusterMeta | None = None
    tag_id: int
    local: bool | None = None
    relationship_type: bool | str | None = None


class AddEditGetEventGalaxyClusterRelationTag(BaseModel):
    id: int
    name: str
    colour: str
    exportable: bool
    org_id: int
    user_id: int
    hide_tag: bool
    numerical_value: str
    is_galaxy: bool
    is_custom_galaxy: bool
    local_only: bool


class AddEditGetEventGalaxyClusterRelation(BaseModel):
    id: int
    galaxy_cluster_id: int
    referenced_galaxy_cluster_id: int
    referenced_galaxy_cluster_uuid: str
    referenced_galaxy_cluster_type: str
    galaxy_cluster_uuid: str
    distribution: str
    sharing_group_id: int | None = None
    default: bool
    Tag: list[AddEditGetEventGalaxyClusterRelationTag] = []


class AddEditGetEventGalaxyCluster(BaseModel):
    id: int
    uuid: str
    collection_uuid: str
    type: str
    value: str
    tag_name: str
    description: str
    galaxy_id: int
    source: str
    authors: list[str]
    version: str
    distribution: str | None = None
    sharing_group_id: int | None = None
    org_id: int
    orgc_id: int
    default: bool | None = None
    locked: bool | None = None
    extends_uuid: str | None = None
    extends_version: str | None = None
    published: bool | None = None
    deleted: bool | None = None
    GalaxyClusterRelation: list[AddEditGetEventGalaxyClusterRelation] = []
    Org: Organisation | None = None
    Orgc: Organisation | None = None
    meta: AddEditGetEventGalaxyClusterMeta | None = None
    tag_id: int
    attribute_tag_id: int | None = None
    event_tag_id: int | None = None
    local: bool | None = None
    relationship_type: bool | str = ""


class AddEditGetEventGalaxy(BaseModel):
    id: int
    uuid: str
    name: str
    type: str
    description: str
    version: str
    icon: str
    namespace: str
    enabled: bool
    local_only: bool
    kill_chain_order: str | None = None
    created: datetime | str
    modified: datetime | str
    org_id: int
    orgc_id: int
    default: bool
    distribution: DistributionLevels
    GalaxyCluster: list[AddEditGetEventGalaxyCluster] = []


class AddEditGetEventOrg(BaseModel):
    id: int
    name: str
    uuid: str | None = None
    local: bool | None = None


class AddEditGetEventTag(BaseModel):
    id: int
    name: str
    colour: str
    exportable: bool
    user_id: int
    hide_tag: bool
    numerical_value: int | None = None
    is_galaxy: bool
    is_custom_galaxy: bool
    local_only: bool
    local: bool
    relationship_type: bool | str | None = None


class AddEditGetEventAttribute(BaseModel):
    id: int
    event_id: int
    object_id: int
    object_relation: str | None = None
    category: str
    type: str
    value: str
    to_ids: bool
    uuid: str
    timestamp: str
    distribution: str
    sharing_group_id: int
    comment: str | None = None
    deleted: bool
    disable_correlation: bool
    first_seen: str | None = None
    last_seen: str | None = None
    Galaxy: list[AddEditGetEventGalaxy] = []
    ShadowAttribute: list[str] = []
    Tag: list[AddEditGetEventTag] = []


class AddEditGetEventShadowAttribute(BaseModel):
    value: str
    to_ids: bool
    type: str
    category: str


class AddEditGetEventEventReport(BaseModel):
    id: int
    uuid: str
    event_id: int
    name: str
    content: str
    distribution: str
    sharing_group_id: int
    timestamp: str
    deleted: bool


class AddEditGetEventObject(BaseModel):
    id: int
    name: str
    meta_category: str
    description: str
    template_uuid: str
    template_version: str
    event_id: int
    uuid: str
    timestamp: str
    distribution: str
    sharing_group_id: int
    comment: str
    deleted: bool
    first_seen: str | None = None
    last_seen: str | None = None
    ObjectReference: list[str] = []
    Attribute: list[AddEditGetEventAttribute] = []


class AddEditGetEventRelatedEventAttributesOrg(BaseModel):
    id: int
    name: str
    uuid: str


class AddEditGetEventRelatedEventAttributes(BaseModel):
    id: int
    date: str
    threat_level_id: int
    info: str
    published: str
    uuid: str
    analysis: str
    timestamp: str
    distribution: str
    org_id: int
    orgc_id: int
    Org: AddEditGetEventRelatedEventAttributesOrg
    Orgc: AddEditGetEventRelatedEventAttributesOrg


class AddEditGetEventRelatedEvent(BaseModel):
    Event: AddEditGetEventRelatedEventAttributes
    RelationshipInbound: list


class AddEditGetEventDetails(BaseModel):
    id: int
    orgc_id: int
    org_id: int
    date: str
    threat_level_id: int
    info: str
    published: bool
    uuid: str
    attribute_count: str
    analysis: str
    timestamp: str
    distribution: int
    proposal_email_lock: bool
    locked: bool
    publish_timestamp: str
    sharing_group_id: int | None = None
    disable_correlation: bool
    extends_uuid: str
    protected: bool | None = None
    event_creator_email: str
    Org: AddEditGetEventOrg
    Orgc: AddEditGetEventOrg
    Attribute: list[AddEditGetEventAttribute] = []
    ShadowAttribute: list[AddEditGetEventShadowAttribute] = []
    RelatedEvent: list[AddEditGetEventRelatedEvent] = []
    Galaxy: list[AddEditGetEventGalaxy] = []
    Object: list[AddEditGetEventObject] = []
    EventReport: list[AddEditGetEventEventReport] = []
    CryptographicKey: list[str] = []
    Tag: list[AddEditGetEventTag] = []

    #    @validator("uuid", "extends_uuid", pre=True)
    #    @classmethod
    #    def uuid_empty_str(cls: Type["AddEditGetEventDetails"], value: Any) -> Any:  # noqa: ANN102
    #        """
    #        Method to convert an empty string or None to a UUID filled with zeros for the UUID fields.
    #
    #        :param value: the value to check and possibly convert
    #        :type value: Any
    #        :return: returns a UUID object containing zeros if the input is an empty string,zero or None
    #         otherwise the input value
    #        :rtype: Any
    #        """
    #        if value == "" or value is None or value == "0":
    #            return "00000000-0000-0000-0000-000000000000"
    #
    #        return value

    @validator("sharing_group_id", pre=True)
    @classmethod
    def zero_sharing_group_id_to_none(cls: Type["AddEditGetEventDetails"], value: Any) -> Any:  # noqa: ANN102
        if value is not None and value == 0:
            return None
        return value


class AddEditGetEventResponse(BaseModel):
    Event: AddEditGetEventDetails

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}


class GetAllEventsOrg(BaseModel):
    id: int
    name: str
    uuid: str | None = None


class UnpublishEventResponse(BaseModel):
    saved: bool | None = None
    success: bool | None = None
    name: str
    message: str
    url: str
    id: int | None = None

    class Config:
        orm_mode = True


class SearchEventsResponse(BaseModel):
    response: list[AddEditGetEventResponse]

    class Config:
        orm_mode = True


class SearchEventsBody(BaseModel):
    returnFormat: str
    page: int | None = None
    limit: int | None = None
    value: str | None = None
    type: str | None = None
    category: str | None = None
    org: str | None = None
    tags: list[str] | None = None
    event_tags: list[str] | None = None
    searchall: str | None = None
    from_: str | None = None
    to: str | None = None
    last: int | None = None
    eventid: int | None = None
    withAttachments: bool | None = None
    sharinggroup: list[str] | None = None
    metadata: bool | None = None
    uuid: str | None = None
    publish_timestamp: str | None = None
    timestamp: str | None = None
    published: bool | None = None
    enforceWarninglist: bool | None = None
    sgReferenceOnly: bool | None = None
    requested_attributes: list[str] | None = None
    includeContext: bool | None = None
    headerless: bool | None = None
    includeWarninglistHits: bool | None = None
    attackGalaxy: str | None = None
    to_ids: bool | None = None
    deleted: bool | None = None
    excludeLocalTags: bool | None = None
    date: str | None = None
    includeSightingdb: bool | None = None
    tag: str | None = None
    object_relation: str | None = None
    threat_level_id: int | None = None

    class Config:
        orm_mode = True


class PublishEventResponse(BaseModel):
    saved: bool | None = None
    success: bool | None = None
    name: str
    message: str
    url: str
    id: int | None = None

    class Config:
        orm_mode = True


class GetAllEventsEventTagTag(BaseModel):
    id: int
    name: str
    colour: str
    is_galaxy: bool


class IndexEventsEventTag(BaseModel):
    id: int
    event_id: int
    tag_id: int
    local: bool
    Tag: GetAllEventsEventTagTag


class IndexEventsAttributes(BaseModel):
    id: int
    org_id: int
    date: str
    info: str
    uuid: str
    published: bool
    analysis: str
    attribute_count: str
    orgc_id: int
    timestamp: str
    distribution: str
    sharing_group_id: int
    proposal_email_lock: bool
    locked: bool
    threat_level_id: int
    publish_timestamp: str
    sighting_timestamp: str
    disable_correlation: bool
    extends_uuid: str
    protected: bool | None = None
    Org: GetAllEventsOrg
    Orgc: GetAllEventsOrg
    GalaxyCluster: list[GetAllEventsGalaxyCluster] = []
    EventTag: list[IndexEventsEventTag] = []

    class Config:
        orm_mode = True


class IndexEventsBody(BaseModel):
    page: PositiveInt | None = None
    limit: conint(gt=0, lt=500) | None = None  # type: ignore
    sort: int | None = None
    direction: int | None = None
    minimal: bool | None = None
    attribute: str | None = None
    eventid: int | None = None
    datefrom: str | None = None
    dateuntil: str | None = None
    org: str | None = None
    eventinfo: str | None = None
    tag: str | None = None
    tags: list[str] | None = None
    distribution: str | None = None
    sharinggroup: str | None = None
    analysis: str | None = None
    threatlevel: str | None = None
    email: str | None = None
    hasproposal: str | None = None
    timestamp: str | None = None
    publish_timestamp: str | None = None
    searchDatefrom: str | None = None
    searchDateuntil: str | None = None

    class Config:
        orm_mode = True


class ObjectEventResponse(BaseModel):
    id: int
    info: str
    org_id: int | None = None
    orgc_id: int | None = None


class GetAllEventsEventTag(BaseModel):
    id: int
    event_id: int
    tag_id: int
    local: bool
    relationship_type: bool | str | None = None
    Tag: GetAllEventsEventTagTag | None = None


class GetAllEventsResponse(BaseModel):
    id: int
    org_id: int  # owner org
    distribution: str
    info: str
    orgc_id: int  # creator org
    uuid: str
    date: str
    published: bool
    analysis: str
    attribute_count: str
    timestamp: str
    sharing_group_id: int
    proposal_email_lock: bool
    locked: bool
    threat_level_id: int
    publish_timestamp: str
    sighting_timestamp: str
    disable_correlation: bool
    extends_uuid: str
    event_creator_email: str | None = None  # omitted
    protected: str | None = None
    Org: GetAllEventsOrg
    Orgc: GetAllEventsOrg
    GalaxyCluster: list[GetAllEventsGalaxyCluster]
    EventTag: list[GetAllEventsEventTag]

    class Config:
        orm_mode = True


class EditEventBody(BaseModel):
    info: str | None = None
    org_id: int | None = None
    distribution: str | None = None
    orgc_id: int | None = None
    uuid: str | None = None
    date: str | None = None
    published: bool | None = None
    analysis: str | None = None
    attribute_count: str | None = None
    timestamp: str | None = None
    sharing_group_id: int | None = None
    proposal_email_lock: bool | None = None
    locked: bool | None = None
    threat_level_id: int | None = None
    publish_timestamp: str | None = None
    sighting_timestamp: str | None = None
    disable_correlation: bool | None = None
    extends_uuid: str | None = None
    event_creator_email: str | None = None
    protected: str | None = None
    cryptographic_key: str | None = None

    class Config:
        orm_mode = True


class DeleteEventResponse(BaseModel):
    saved: bool
    success: bool | None = None
    name: str
    message: str
    url: str
    id: int
    errors: str | None = None

    class Config:
        orm_mode = True


class AddRemoveTagEventsResponse(BaseModel):
    saved: bool
    success: str | None = None
    check_publish: bool | None = None
    errors: str | None = None

    class Config:
        orm_mode = True


class AddEventBody(BaseModel):
    info: str
    org_id: int | None = None
    distribution: str | None = None
    orgc_id: int | None = None
    uuid: str | None = None
    date: str | None = None
    published: bool | None = None
    analysis: str | None = None
    attribute_count: str | None = None
    timestamp: str | None = None
    sharing_group_id: int | None = None
    proposal_email_lock: bool | None = None
    locked: bool | None = None
    threat_level_id: int | None = None
    publish_timestamp: str | None = None
    sighting_timestamp: str | None = None
    disable_correlation: bool | None = None
    extends_uuid: str | None = None
    protected: str | None = None

    class Config:
        orm_mode = True


class AddEventTag(BaseModel):
    name: str
