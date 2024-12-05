from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text

from mmisp.db.mixins import DictMixin
from mmisp.db.mypy import Mapped, mapped_column
from mmisp.lib.uuid import uuid

from ..database import Base


class SharingGroup(Base, DictMixin):
    __tablename__ = "sharing_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name = mapped_column(String(255), nullable=False, unique=True)
    releasability = mapped_column(Text, nullable=False)
    description = mapped_column(Text, nullable=False, default="")
    uuid = mapped_column(String(40), unique=True, default=uuid, nullable=False)
    organisation_uuid = mapped_column(String(40), nullable=False)
    org_id = mapped_column(Integer, nullable=False, index=True)
    sync_user_id = mapped_column(Integer, nullable=False, default=0, index=True)
    active = mapped_column(Boolean, nullable=False, default=False)
    created = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    modified = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    local = mapped_column(Boolean, nullable=False, default=True)
    roaming = mapped_column(Boolean, default=False, nullable=False)


class SharingGroupOrg(Base, DictMixin):
    __tablename__ = "sharing_group_orgs"

    id = mapped_column(Integer, primary_key=True, nullable=False)
    sharing_group_id = mapped_column(Integer, index=True, nullable=False)
    org_id = mapped_column(Integer, index=True, nullable=False)
    extend = mapped_column(Boolean, default=False, nullable=False)


class SharingGroupServer(Base, DictMixin):
    __tablename__ = "sharing_group_servers"

    id = mapped_column(Integer, primary_key=True, nullable=False)
    sharing_group_id = mapped_column(Integer, index=True, nullable=False)
    server_id = mapped_column(Integer, index=True, nullable=False)
    all_orgs = mapped_column(Boolean, index=True, nullable=False, default=False)
