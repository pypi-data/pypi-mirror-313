from calendar import timegm
from time import gmtime

from sqlalchemy.ext.asyncio import AsyncSession

from mmisp.db.models.event import Event


async def action_publish_event(db: AsyncSession, event: Event) -> None:
    setattr(event, "published", True)
    setattr(event, "publish_timestamp", timegm(gmtime()))
