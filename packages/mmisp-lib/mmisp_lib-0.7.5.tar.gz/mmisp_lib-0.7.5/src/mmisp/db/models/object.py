from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from mmisp.db.database import Base
from mmisp.db.mixins import DictMixin
from mmisp.db.mypy import Mapped, mapped_column
from mmisp.lib.uuid import uuid


class Object(Base, DictMixin):
    __tablename__ = "objects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    uuid: Mapped[str] = mapped_column(String(255), unique=True, default=uuid, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    meta_category: Mapped[str] = mapped_column("meta-category", String(255), index=True, key="meta_category")
    description: Mapped[str] = mapped_column(String(255))
    template_uuid: Mapped[str] = mapped_column(String(255), index=True, default=None)
    template_version: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id"), index=True, nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer, index=True, nullable=False, default=0)
    distribution: Mapped[int] = mapped_column(Integer, index=True, nullable=False, default=0)
    sharing_group_id: Mapped[int] = mapped_column(Integer, ForeignKey("sharing_groups.id"), index=True)
    comment: Mapped[str] = mapped_column(String(255), nullable=False)
    deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    first_seen: Mapped[int] = mapped_column(Integer, index=True, default=None)
    last_seen: Mapped[int] = mapped_column(Integer, index=True, default=None)

    attributes = relationship(
        "Attribute",
        primaryjoin="Object.id == Attribute.object_id",
        back_populates="mispobject",
        lazy="raise_on_sql",
        foreign_keys="Attribute.object_id",
    )  # type:ignore[var-annotated]
    event = relationship(
        "Event",
        back_populates="mispobjects",
        lazy="raise_on_sql",
    )  # type:ignore[var-annotated]


class ObjectTemplate(Base, DictMixin):
    __tablename__ = "object_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    uuid: Mapped[str] = mapped_column(String(255), unique=True, default=uuid, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    org_id: Mapped[int] = mapped_column(Integer, ForeignKey("organisations.id"), index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255))
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    requirements: Mapped[str] = mapped_column(String(255))
    fixed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
