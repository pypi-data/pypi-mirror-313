from datetime import datetime
from typing import Self

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from mmisp.db.mypy import Mapped, mapped_column
from mmisp.lib.uuid import uuid

from ..database import Base
from .organisation import Organisation
from .tag import Tag
from .user import User


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    uuid: Mapped[str] = mapped_column(String(40), unique=True, default=uuid, nullable=False, index=True)
    org_id: Mapped[int] = mapped_column(Integer, ForeignKey(Organisation.id), nullable=False, index=True)
    date: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    info: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    analysis: Mapped[int] = mapped_column(Integer, nullable=False)
    attribute_count: Mapped[int] = mapped_column(Integer, default=0)
    orgc_id: Mapped[int] = mapped_column(Integer, ForeignKey(Organisation.id), nullable=False, index=True)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    distribution: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sharing_group_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, default=0)
    proposal_email_lock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    locked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    threat_level_id: Mapped[int] = mapped_column(Integer, nullable=False)
    publish_timestamp: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sighting_timestamp: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    disable_correlation: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    extends_uuid: Mapped[str] = mapped_column(String(40), default="", index=True)
    protected: Mapped[bool] = mapped_column(Boolean)

    attributes = relationship("Attribute", back_populates="event")  # type:ignore[assignment,var-annotated]
    mispobjects = relationship("Object", back_populates="event")  # type:ignore[assignment,var-annotated]
    org = relationship(
        "Organisation", primaryjoin="Event.org_id == Organisation.id", back_populates="events", lazy="raise_on_sql"
    )  # type:ignore[assignment,var-annotated]
    orgc = relationship(
        "Organisation",
        primaryjoin="Event.orgc_id == Organisation.id",
        back_populates="events_created",
        lazy="raise_on_sql",
    )  # type:ignore[assignment,var-annotated]
    creator = relationship("User", primaryjoin="Event.user_id == User.id", lazy="selectin")
    tags = relationship("Tag", secondary="event_tags", lazy="raise_on_sql", viewonly=True)
    eventtags = relationship(
        "EventTag", primaryjoin="Event.id == EventTag.event_id", lazy="raise_on_sql", viewonly=True
    )
    eventtags_galaxy = relationship(
        "EventTag",
        primaryjoin="and_(Event.id == EventTag.event_id, Tag.is_galaxy)",
        secondary="join(EventTag, Tag, EventTag.tag_id == Tag.id)",
        secondaryjoin="EventTag.tag_id == Tag.id",
        lazy="raise_on_sql",
        viewonly=True,
    )
    galaxy_tags = relationship(
        "Tag",
        secondary="event_tags",
        secondaryjoin="and_(EventTag.tag_id == Tag.id, Tag.is_galaxy)",
        lazy="raise_on_sql",
        overlaps="tags, events",
        viewonly=True,
    )

    async def add_tag(
        self: Self, db: AsyncSession, tag: Tag, local: bool = False, relationship_type: str | None = None
    ) -> "EventTag":
        if tag.local_only:
            local = True
        event_tag: EventTag = EventTag(
            event=self, tag=tag, local=local, event_id=self.id, tag_id=tag.id, relationship_type=relationship_type
        )
        db.add(event_tag)
        await db.flush()
        await db.refresh(event_tag)
        return event_tag


class EventReport(Base):
    __tablename__ = "event_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    uuid: Mapped[str] = mapped_column(String(40), unique=True, nullable=False, default=uuid)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey(Event.id), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text)
    distribution: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sharing_group_id: Mapped[int] = mapped_column(Integer)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)
    deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class EventTag(Base):
    __tablename__ = "event_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey(Event.id, ondelete="CASCADE"), nullable=False, index=True)
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey(Tag.id, ondelete="CASCADE"), nullable=False, index=True)
    local: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    relationship_type: Mapped[str] = mapped_column(String(191), nullable=True)

    event = relationship("Event", back_populates="eventtags", lazy="raise_on_sql", viewonly=True)
    tag = relationship("Tag", back_populates="eventtags", lazy="raise_on_sql", viewonly=True)
