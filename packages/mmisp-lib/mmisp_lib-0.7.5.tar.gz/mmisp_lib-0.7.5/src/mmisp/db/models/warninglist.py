from sqlalchemy import Boolean, ForeignKey, Integer, String

from mmisp.db.database import Base
from mmisp.db.mypy import Mapped, mapped_column


class Warninglist(Base):
    __tablename__ = "warninglists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(255), nullable=False, default="string")
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    default: Mapped[bool] = mapped_column(Boolean, default=True)
    category: Mapped[str] = mapped_column(String(255))


class WarninglistEntry(Base):
    __tablename__ = "warninglist_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    value: Mapped[str] = mapped_column(String(255), nullable=False)
    warninglist_id: Mapped[int] = mapped_column(Integer, ForeignKey(Warninglist.id, ondelete="CASCADE"), nullable=False)
    comment: Mapped[str] = mapped_column(String(255))


class WarninglistType(Base):
    __tablename__ = "warninglist_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    warninglist_id: Mapped[int] = mapped_column(Integer, ForeignKey(Warninglist.id, ondelete="CASCADE"), nullable=False)
