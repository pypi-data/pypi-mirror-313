from mmisp.db.models.object import Object


def generate_object() -> Object:
    """
    Generate an object.
    :return: An object.
    """
    return Object(
        name="test",
        template_uuid=None,
        template_version=1,
        timestamp="1",
        distribution=1,
        comment="test",
        deleted=False,
    )
