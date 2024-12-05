from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, String, Text

from mmisp.db.database import Base
from mmisp.db.models.event import Event
from mmisp.db.models.organisation import Organisation
from mmisp.db.mypy import Mapped, mapped_column
from mmisp.lib.uuid import uuid


class ShadowAttribute(Base):
    __tablename__ = "shadow_attributes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    old_id: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    uuid: Mapped[str] = mapped_column(String(40), unique=True, default=uuid, nullable=False, index=True)
    org_id: Mapped[int] = mapped_column(Integer, ForeignKey(Organisation.id), nullable=False, index=True)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey(Event.id), nullable=False, index=True)
    event_uuid: Mapped[str] = mapped_column(String(40), ForeignKey(Event.uuid), nullable=False, index=True)
    event_org_id: Mapped[int] = mapped_column(Integer, ForeignKey(Organisation.id), nullable=False)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    value1: Mapped[str] = mapped_column(Text, nullable=True)
    value2: Mapped[str] = mapped_column(Text, nullable=True)
    to_ids: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    proposal_to_delete: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    disable_correlation: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    first_seen: Mapped[int] = mapped_column(BigInteger, nullable=True)
    last_seen: Mapped[str] = mapped_column(BigInteger, nullable=True)
