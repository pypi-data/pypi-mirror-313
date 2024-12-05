from mmisp.api_schemas.attributes import GetAttributeAttributes, GetAttributeTag


class AttributeTagWithRelationshipType(GetAttributeTag):
    """
    Encapsulates a MISP Attribute Tag with the relationship type to its attribute.
    """

    relationship_local: bool
    """Whether the relationship is only local or not."""
    relationship_type: str
    """The relationship type between the attribute and tag."""


class AttributeWithTagRelationship(GetAttributeAttributes):
    """
    Encapsulates a full MISP Attribute with all it's tags and tag relationships.
    """

    Tag: list[AttributeTagWithRelationshipType] | None = None
