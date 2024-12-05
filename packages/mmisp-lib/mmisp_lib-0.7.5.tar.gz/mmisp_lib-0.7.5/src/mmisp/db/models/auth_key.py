from time import time

from sqlalchemy import Boolean, ForeignKey, Integer, String

from mmisp.db.mypy import Mapped, mapped_column
from mmisp.lib.uuid import uuid

from ..database import Base


class AuthKey(Base):
    __tablename__ = "auth_keys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    uuid: Mapped[str] = mapped_column(String(255), unique=True, default=uuid, nullable=False)
    authkey: Mapped[str] = mapped_column(String(255), nullable=False)
    authkey_start: Mapped[str] = mapped_column(String(255), nullable=False)
    authkey_end: Mapped[str] = mapped_column(String(255), nullable=False)
    created: Mapped[int] = mapped_column(Integer, nullable=False, default=time)
    expiration: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    read_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=0)
    comment: Mapped[str] = mapped_column(String(255))
    allowed_ips: Mapped[str] = mapped_column(String(255))
    unique_ips: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
