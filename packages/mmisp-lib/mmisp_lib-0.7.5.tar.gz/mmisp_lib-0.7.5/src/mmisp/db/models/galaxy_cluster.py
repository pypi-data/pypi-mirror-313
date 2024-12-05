import json
from typing import Self

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from mmisp.db.mixins import DictMixin, UpdateMixin
from mmisp.db.mypy import Mapped, mapped_column
from mmisp.db.uuid_type import DBUUID
from mmisp.lib.uuid import uuid

from ..database import Base
from .galaxy import Galaxy


class GalaxyCluster(Base, UpdateMixin, DictMixin):
    __tablename__ = "galaxy_clusters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    uuid: Mapped[str] = mapped_column(DBUUID, unique=True, default=uuid, index=True)
    collection_uuid: Mapped[str] = mapped_column(String(255), nullable=False, index=True, default="")
    type: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    tag_name: Mapped[str] = mapped_column(String(255), nullable=False, default="", index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    galaxy_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(Galaxy.id, ondelete="CASCADE"), nullable=False, index=True
    )
    source: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    _authors: Mapped[str] = mapped_column("authors", Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=0, index=True)
    distribution: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sharing_group_id: Mapped[int] = mapped_column(Integer, index=True, nullable=True, default=None)
    org_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, default=0)
    orgc_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, default=0)
    default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    locked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    extends_uuid: Mapped[str] = mapped_column(String(40), index=True)
    extends_version: Mapped[int] = mapped_column(Integer, index=True, nullable=True, default=None)
    published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    org = relationship(
        "Organisation",
        primaryjoin="GalaxyCluster.org_id == Organisation.id",
        back_populates="galaxy_clusters",
        lazy="raise_on_sql",
        foreign_keys="GalaxyCluster.org_id",
    )  # type:ignore[assignment,var-annotated]
    orgc = relationship(
        "Organisation",
        primaryjoin="GalaxyCluster.orgc_id == Organisation.id",
        back_populates="galaxy_clusters_created",
        lazy="raise_on_sql",
        foreign_keys="GalaxyCluster.orgc_id",
    )  # type:ignore[assignment,var-annotated]
    galaxy = relationship(
        "Galaxy",
        back_populates="galaxy_clusters",
        lazy="raise_on_sql",
    )  # type:ignore[assignment,var-annotated]
    galaxy_elements = relationship(
        "GalaxyElement",
        back_populates="galaxy_cluster",
        lazy="raise_on_sql",
    )  # type:ignore[assignment,var-annotated]
    tag = relationship(
        "Tag",
        primaryjoin="GalaxyCluster.tag_name == Tag.name",
        back_populates="galaxy_cluster",
        lazy="raise_on_sql",
        foreign_keys="GalaxyCluster.tag_name",
        single_parent=True,
        uselist=False,
    )  # type:ignore[assignment,var-annotated]

    def __init__(self: Self, *arg, **kwargs) -> None:
        if "authors" in kwargs:
            self._authors = json.dumps(kwargs["authors"])
            del kwargs["authors"]
        super().__init__(*arg, **kwargs)

    @hybrid_property
    def authors(self: Self) -> list[str]:
        return json.loads(self._authors)

    @authors.setter  # type: ignore[no-redef]
    def authors(self: Self, value: list[str]) -> None:
        self._authors = json.dumps(value)


class GalaxyElement(Base, DictMixin, UpdateMixin):
    __tablename__ = "galaxy_elements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    galaxy_cluster_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(GalaxyCluster.id, ondelete="CASCADE"), nullable=False, index=True
    )
    key: Mapped[str] = mapped_column(String(255), nullable=False, default="", index=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)

    galaxy_cluster = relationship(
        "GalaxyCluster",
        back_populates="galaxy_elements",
        lazy="raise_on_sql",
    )  # type:ignore[assignment,var-annotated]


class GalaxyReference(Base):
    __tablename__ = "galaxy_reference"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    galaxy_cluster_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(GalaxyCluster.id, ondelete="CASCADE"), nullable=False, index=True
    )
    referenced_galaxy_cluster_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    referenced_galaxy_cluster_uuid: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    referenced_galaxy_cluster_type: Mapped[str] = mapped_column(Text, nullable=False)
    referenced_galaxy_cluster_value: Mapped[str] = mapped_column(Text, nullable=False)
