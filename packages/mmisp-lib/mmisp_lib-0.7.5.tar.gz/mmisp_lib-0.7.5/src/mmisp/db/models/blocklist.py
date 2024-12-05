from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text

from mmisp.db.mypy import Mapped, mapped_column

from ..database import Base


class GalaxyClusterBlocklist(Base):
    __tablename__ = "galaxy_cluster_blocklists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    cluster_uuid: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    created: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    cluster_info: Mapped[str] = mapped_column(Text, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    cluster_orgc: Mapped[int] = mapped_column(String(255), nullable=False)


class EventBlocklist(Base):
    __tablename__ = "event_blocklists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    event_uuid: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    created: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    event_info: Mapped[str] = mapped_column(Text, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    event_orgc: Mapped[int] = mapped_column(String(255), nullable=False)


class OrgBlocklist(Base):
    __tablename__ = "org_blocklists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    org_uuid: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    created: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    org_name: Mapped[str] = mapped_column(String(255), nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
