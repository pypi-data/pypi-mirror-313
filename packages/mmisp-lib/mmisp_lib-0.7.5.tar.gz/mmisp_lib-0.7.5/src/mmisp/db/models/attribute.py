import typing
from typing import Self, Type

from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, String, Text, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.hybrid import Comparator, hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm.decl_api import DeclarativeMeta

from mmisp.db.mixins import DictMixin
from mmisp.db.mypy import Mapped, mapped_column
from mmisp.lib.attributes import categories, default_category, mapper_safe_clsname_val, to_ids
from mmisp.lib.uuid import uuid

from ..database import Base
from .event import Event
from .tag import Tag

if typing.TYPE_CHECKING:
    from sqlalchemy import ColumnExpressionArgument
else:
    ColumnExpressionArgument = typing.Any


class AttributeComparator(Comparator):
    def __init__(self: Self, cls: typing.Any) -> None:
        self.cls = cls

    def __eq__(self: Self, other: typing.Any) -> ColumnExpressionArgument:
        # Overriding equality to check if the value matches either value1 or value1 + "|" + value2
        return or_(self.cls.value1 == other, self.cls.value1 + "|" + self.cls.value2 == other)


class Attribute(Base, DictMixin):
    __tablename__ = "attributes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    uuid: Mapped[str] = mapped_column(String(40), unique=True, default=uuid, index=True)
    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True
    )
    object_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    object_relation: Mapped[str] = mapped_column(String(255), index=True)
    category: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    value1: Mapped[str] = mapped_column(Text, nullable=False)
    value2: Mapped[str] = mapped_column(Text, nullable=False, default="")
    to_ids: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    distribution: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sharing_group_id: Mapped[int] = mapped_column(Integer, index=True, default=0)
    comment: Mapped[str] = mapped_column(Text)
    deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    disable_correlation: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    first_seen: Mapped[int] = mapped_column(BigInteger, index=True)
    last_seen: Mapped[int] = mapped_column(BigInteger, index=True)

    event = relationship("Event", back_populates="attributes", lazy="joined")  # type:ignore[var-annotated]
    mispobject = relationship(
        "Object",
        primaryjoin="Attribute.object_id == Object.id",
        back_populates="attributes",
        lazy="joined",
        foreign_keys="Attribute.object_id",
    )  # type:ignore[var-annotated]
    tags = relationship("Tag", secondary="attribute_tags", lazy="raise_on_sql", viewonly=True)
    attributetags = relationship(
        "AttributeTag",
        primaryjoin="Attribute.id == AttributeTag.attribute_id",
        back_populates="attribute",
        lazy="raise_on_sql",
        viewonly=True,
    )
    attributetags_galaxy = relationship(
        "AttributeTag",
        primaryjoin="and_(Attribute.id == AttributeTag.attribute_id, Tag.is_galaxy)",
        secondary="join(AttributeTag, Tag, AttributeTag.tag_id == Tag.id)",
        secondaryjoin="AttributeTag.tag_id == Tag.id",
        lazy="raise_on_sql",
        viewonly=True,
    )

    galaxy_tags = relationship(
        "Tag",
        secondary="attribute_tags",
        secondaryjoin="and_(AttributeTag.tag_id == Tag.id, Tag.is_galaxy)",
        lazy="raise_on_sql",
        overlaps="tags, events",
        viewonly=True,
    )
    local_tags = relationship(
        "Tag",
        secondary="attribute_tags",
        secondaryjoin="and_(AttributeTag.tag_id == Tag.id, AttributeTag.local)",
        lazy="raise_on_sql",
        viewonly=True,
    )
    nonlocal_tags = relationship(
        "Tag",
        secondary="attribute_tags",
        secondaryjoin="and_(AttributeTag.tag_id == Tag.id, not_(AttributeTag.local))",
        lazy="raise_on_sql",
        viewonly=True,
    )

    __mapper_args__ = {"polymorphic_on": "type"}

    def __init__(self: Self, *arg, **kwargs) -> None:
        if "value" in kwargs:
            split_val = kwargs["value"].split("|", 1)
            kwargs["value1"] = split_val[0]
            if len(split_val) == 2:
                kwargs["value2"] = split_val[1]

        super().__init__(*arg, **kwargs)

    async def add_tag(self: Self, db: AsyncSession, tag: "Tag", local: bool = False) -> "AttributeTag":
        if tag.local_only:
            local = True
        attribute_tag = AttributeTag(attribute=self, tag=tag, event_id=self.event_id, local=local)
        db.add(attribute_tag)
        await db.commit()
        await db.refresh(attribute_tag)
        return attribute_tag

    @property
    def event_uuid(self: "Attribute") -> str:
        return self.event.uuid

    @hybrid_property
    def value(self: Self) -> str:
        if self.value2 == "":
            return self.value1
        return f"{self.value1}|{self.value2}"

    @value.setter  # type: ignore[no-redef]
    def value(self: Self, value: str) -> None:
        split = value.split("|", 1)
        self.value1 = split[0]
        if len(split) == 2:
            self.value2 = split[1]

    @value.comparator
    def value(cls: Self) -> AttributeComparator:
        return AttributeComparator(cls)


class AttributeTag(Base):
    __tablename__ = "attribute_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    attribute_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(Attribute.id, ondelete="CASCADE"), nullable=False, index=True
    )
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey(Event.id, ondelete="CASCADE"), nullable=False, index=True)
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey(Tag.id, ondelete="CASCADE"), nullable=False, index=True)
    local: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    relationship_type: Mapped[str] = mapped_column(String(191), nullable=False, default="")

    attribute = relationship("Attribute", back_populates="attributetags", lazy="raise_on_sql")
    tag = relationship("Tag", back_populates="attributetags", lazy="raise_on_sql")


class AttributeMeta(DeclarativeMeta):
    def __new__(cls: Type[type], clsname: str, bases: tuple, dct: dict) -> "AttributeMeta":
        key = clsname[len("Attribute") :]
        dct["default_category"] = default_category[mapper_safe_clsname_val[key]]
        dct["categories"] = categories[mapper_safe_clsname_val[key]]
        dct["default_to_ids"] = to_ids[mapper_safe_clsname_val[key]]
        dct["__mapper_args__"] = {"polymorphic_identity": mapper_safe_clsname_val[key]}
        return super().__new__(cls, clsname, bases, dct)  # type:ignore[misc]


for k, _ in mapper_safe_clsname_val.items():
    vars()["Attribute" + k] = AttributeMeta("Attribute" + k, (Attribute,), dict())
