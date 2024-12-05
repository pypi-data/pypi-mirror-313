from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from mmisp.db.mixins import DictMixin, UpdateMixin
from mmisp.db.mypy import Mapped, mapped_column
from mmisp.lib.uuid import uuid

from ..database import Base


class Galaxy(Base, DictMixin, UpdateMixin):
    __tablename__ = "galaxies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    uuid: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, default=uuid)
    name: Mapped[str] = mapped_column(String(255), nullable=False, default="", index=True)
    type: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[str] = mapped_column(String(255), nullable=False)
    icon: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    namespace: Mapped[str] = mapped_column(String(255), nullable=False, default="misp", index=True)
    kill_chain_order: Mapped[str] = mapped_column(String(255))
    """must be serialized"""
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    local_only: Mapped[bool] = mapped_column(Boolean, default=False)

    default: Mapped[bool] = mapped_column(Boolean, default=False)

    org_id: Mapped[int] = mapped_column(Integer, nullable=False)
    orgc_id: Mapped[int] = mapped_column(Integer, nullable=False)

    created: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    modified: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    distribution: Mapped[int] = mapped_column(Integer, nullable=False)

    galaxy_clusters = relationship(
        "GalaxyCluster",
        back_populates="galaxy",
        lazy="raise_on_sql",
    )  # type:ignore[assignment,var-annotated]
