import random
from datetime import datetime

from mmisp.api_schemas.attributes import AddAttributeBody, GetAttributeAttributes
from mmisp.lib.attributes import AttributeCategories, mapper_val_safe_clsname
from mmisp.lib.uuid import uuid
from mmisp.plugins.models.attribute import AttributeTagWithRelationshipType, AttributeWithTagRelationship
from mmisp.tests.generators.feed_generator import generate_number_as_str
from mmisp.tests.generators.object_generator import generate_ids_as_str, generate_random_date_str, generate_random_str
from mmisp.tests.generators.tag_generator import generate_get_attribute_tag_response


def generate_valid_random_create_attribute_data() -> AddAttributeBody:
    return AddAttributeBody(
        type="other",
        value=generate_random_str(),
        value1=generate_random_str(),
        value2=generate_random_str(),
        event_id=generate_ids_as_str(),
        category=random.choice(list(AttributeCategories)),
        to_ids=bool(random.getrandbits(1)),
        uuid=uuid(),
        timestamp=generate_random_date_str(),
        distribution=generate_number_as_str(),
        sharing_group_id=generate_ids_as_str(),
        comment=generate_random_str(),
        deleted=False,
        disable_correlation=bool(random.getrandbits(1)),
        first_seen=datetime.now().isoformat(),
        last_seen=datetime.now().isoformat(),
    )


def generate_get_attribute_attributes_response() -> GetAttributeAttributes:
    return GetAttributeAttributes(
        id=generate_ids_as_str(),
        event_id=generate_ids_as_str(),
        object_id=generate_ids_as_str(),
        object_relation=generate_random_str(),
        category=generate_random_str(),
        type=random.choice(list(mapper_val_safe_clsname.keys())),
        value=generate_random_str(),
        to_ids=False,
        uuid=uuid(),
        timestamp=generate_random_date_str(),
        distribution=generate_number_as_str(),
        sharing_group_id=generate_ids_as_str(),
        comment=generate_random_str(),
        deleted=bool(random.getrandbits),
        disable_correlation=bool(random.getrandbits),
        first_seen=generate_random_date_str(),
        last_seen=generate_random_date_str(),
        event_uuid=uuid(),
        data=generate_random_str(),
        Tag=[generate_get_attribute_tag_response()],
    )


def generate_attribute_with_tag_relationship() -> AttributeWithTagRelationship:
    attribute: GetAttributeAttributes = generate_get_attribute_attributes_response()
    tags: list[AttributeTagWithRelationshipType] = []
    for tag in attribute.Tag or []:
        tags.append(
            AttributeTagWithRelationshipType(
                **tag.dict(), relationship_local=bool(random.getrandbits), relationship_type=generate_random_str()
            )
        )

    return AttributeWithTagRelationship(
        id=attribute.id,
        event_id=attribute.event_id,
        object_id=attribute.object_id,
        object_relation=attribute.object_relation,
        category=attribute.category,
        type=attribute.type,
        value=attribute.value,
        to_ids=attribute.to_ids,
        uuid=attribute.uuid,
        timestamp=attribute.timestamp,
        distribution=attribute.distribution,
        sharing_group_id=attribute.sharing_group_id,
        comment=attribute.comment,
        deleted=attribute.deleted,
        disable_correlation=attribute.disable_correlation,
        first_seen=attribute.first_seen,
        last_seen=attribute.last_seen,
        event_uuid=attribute.event_uuid,
        data=attribute.data,
        Tag=tags,
    )
