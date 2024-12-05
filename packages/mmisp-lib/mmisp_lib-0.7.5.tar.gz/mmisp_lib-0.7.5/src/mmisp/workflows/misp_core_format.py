from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..db.models.attribute import Attribute
from ..db.models.event import Event, EventTag
from ..db.models.organisation import Organisation
from ..db.models.sighting import Sighting
from ..db.models.tag import Tag
from ..db.models.user import User


async def attribute_to_misp_core_format(db: AsyncSession, attribute: Attribute, with_sightings: bool = True) -> dict:
    event = (await db.execute(select(Event).filter(Event.id == attribute.event_id))).scalars().first()
    assert event is not None
    event_data = (await event_to_misp_core_format(db, event))["Event"]
    sightings = (
        await db.execute(
            select(Sighting, Organisation)
            .join(Attribute)
            .join(Organisation)
            .filter(Attribute.id == Sighting.attribute_id)
            .filter(Attribute.id == attribute.id)
            .filter(Organisation.id == Sighting.org_id)
        )
    ).all()

    attribute_data = {
        "id": str(attribute.id),
        "event_id": str(attribute.event_id),
        "object_id": str(attribute.object_id),
        "object_relation": attribute.object_relation,
        "category": attribute.category,
        "type": attribute.type,
        "to_ids": attribute.to_ids,
        "uuid": attribute.uuid,
        "timestamp": str(attribute.timestamp),  # yes, this is actually a string
        "distribution": str(attribute.distribution),
        "sharing_group_id": str(attribute.sharing_group_id),
        "comment": attribute.comment,
        "deleted": attribute.deleted,
        "disable_correlation": attribute.disable_correlation,
        "first_seen": attribute.first_seen,
        "last_seen": attribute.last_seen,
        "value": attribute.value,
    }

    if with_sightings:
        attribute_data["Sighting"] = [
            {
                "id": sighting.id,
                "attribute_id": sighting.attribute_id,
                "event_id": sighting.event_id,
                "org_id": sighting.org_id,
                "date_sighting": str(sighting.date_sighting),
                "uuid": sighting.uuid,
                "source": sighting.source,
                "type": str(sighting.type),
                "attribute_uuid": attribute.uuid,
                "Organisation": {
                    "id": organisation.id,
                    "uuid": organisation.uuid,
                    "name": organisation.name,
                },
            }
            for sighting, organisation in sightings
        ]

    result = {
        "Event": event_data,
    }

    result["Event"]["Attribute"] = [attribute_data]
    result["Event"]["_AttributeFlattened"] = [attribute_data]

    return result


async def tags_for_event_in_core_format(db: AsyncSession, event_id: int) -> list:
    tags: Sequence[Tag] = (
        (
            await db.execute(
                select(Tag).join(EventTag).filter(EventTag.tag_id == Tag.id).filter(EventTag.event_id == event_id)
            )
        )
        .scalars()
        .all()
    )

    return [
        {
            "id": tag.id,
            "name": tag.name,
            "colour": tag.colour,
            "exportable": tag.exportable,
        }
        for tag in tags
    ]


async def event_after_save_new_to_core_format(db: AsyncSession, event: Event) -> dict:
    user_email = (await db.execute(select(User.email).filter(User.id == event.user_id))).scalars().first()
    event_dict = await event_to_misp_core_format(db, event)

    event_data = event_dict["Event"]
    event_data["Attribute"] = []
    event_data["ShadowAttribute"] = []
    event_data["Object"] = []
    event_data["EventTag"] = []
    event_data["EventReport"] = []
    event_data["CryptographicKey"] = []
    event_data["Galaxy"] = []
    event_data["Orgc"] = await org_from_id(db, event.orgc_id)
    event_data["Org"] = await org_from_id(db, event.org_id)
    event_data["RelatedEvent"] = []
    event_data["Sighting"] = []
    event_data["User"] = {"email": user_email}

    return event_dict


async def event_to_misp_core_format(db: AsyncSession, event: Event) -> dict:
    return {
        "Event": {
            "id": str(event.id),
            "org_id": str(event.org_id),
            "distribution": event.distribution,
            "info": event.info,
            "orgc_id": event.orgc_id,
            "uuid": event.uuid,
            # this actually is a datetime.date when querying from SQLAlchemy,
            # no idea why mypy doesn't get it 🙄
            "date": event.date if isinstance(event.date, str) else event.date.isoformat(),  # type:ignore[attr-defined]
            "published": event.published,
            "analysis": event.analysis,
            "attribute_count": event.attribute_count,
            "timestamp": event.timestamp,
            "sharing_group_id": event.sharing_group_id,
            "proposal_email_lock": event.proposal_email_lock,
            "locked": event.locked,
            "threat_level_id": event.threat_level_id,
            "publish_timestamp": event.publish_timestamp,
            "sighting_timestamp": event.sighting_timestamp,
            "disable_correlation": event.disable_correlation,
            "extends_uuid": event.extends_uuid,
            # "event_creator_email": event.event_creator_email,
        }
    }


async def org_from_id(db: AsyncSession, org: int) -> dict:
    orgc = await db.get(Organisation, org)
    return {
        "Orgc": {
            "id": str(orgc.id),
            "uuid": str(orgc.uuid),
            "name": orgc.name,
            "local": orgc.local,
        }
        if orgc is not None
        else None,
    }
