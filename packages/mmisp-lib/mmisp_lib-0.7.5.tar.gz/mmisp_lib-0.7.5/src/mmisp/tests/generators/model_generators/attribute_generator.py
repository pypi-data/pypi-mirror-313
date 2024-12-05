from mmisp.db.models.attribute import Attribute
from mmisp.lib.attributes import AttributeCategories


def generate_attribute(event_id) -> Attribute:
    return Attribute(value="1.2.3.4", value1="1.2.3.4", type="ip-src", category="Network activity", event_id=event_id)


def generate_text_attribute(event_id, value: str) -> Attribute:
    return Attribute(
        value=value, type="text", category=AttributeCategories.OTHER.value, event_id=event_id, sharing_group_id=0
    )


def generate_domain_attribute(event_id, value: str) -> Attribute:
    return Attribute(value=value, type="domain", category=AttributeCategories.NETWORK_ACTIVITY.value, event_id=event_id)
