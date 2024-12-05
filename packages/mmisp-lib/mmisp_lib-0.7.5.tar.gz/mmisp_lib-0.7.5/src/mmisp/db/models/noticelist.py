from sqlalchemy import Boolean, ForeignKey, Integer, String, Text

from mmisp.db.database import Base
from mmisp.db.mypy import Mapped, mapped_column


class Noticelist(Base):
    __tablename__ = "noticelists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    expanded_name: Mapped[str] = mapped_column(String(255), nullable=False)
    ref: Mapped[str] = mapped_column(String(255))  # data serialized as json
    geographical_area: Mapped[str] = mapped_column(String(255))  # data serialized as json
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class NoticelistEntry(Base):
    __tablename__ = "noticelist_entries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    noticelist_id: Mapped[int] = mapped_column(Integer, ForeignKey(Noticelist.id, ondelete="CASCADE"), nullable=False)
    data: Mapped[str] = mapped_column(Text, nullable=False)  # data serialized as json
