from sqlalchemy import BigInteger, ForeignKey, Integer, String

from mmisp.db.database import Base
from mmisp.db.mypy import Mapped, mapped_column
from mmisp.lib.uuid import uuid

from .attribute import Attribute
from .event import Event
from .organisation import Organisation


class Sighting(Base):
    __tablename__ = "sightings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    uuid: Mapped[str] = mapped_column(String(40), unique=True, default=uuid)
    attribute_id: Mapped[int] = mapped_column(Integer, ForeignKey(Attribute.id), index=True, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey(Event.id), index=True, nullable=False)
    org_id: Mapped[int] = mapped_column(Integer, ForeignKey(Organisation.id), index=True, nullable=False)
    date_sighting: Mapped[int] = mapped_column(BigInteger, nullable=False)
    source: Mapped[str] = mapped_column(String(255), index=True, default="")
    type: Mapped[int] = mapped_column(Integer, index=True, default=0)
