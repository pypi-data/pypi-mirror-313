from time import time

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from mmisp.db.mypy import Mapped, mapped_column

from ..database import Base
from .organisation import Organisation


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    org_id: Mapped[int] = mapped_column(Integer, ForeignKey(Organisation.id), nullable=False, index=True)
    server_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    autoalert: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    authkey: Mapped[str] = mapped_column(String(40), nullable=True, default=None)
    invited_by: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    gpgkey: Mapped[str] = mapped_column(Text)
    certif_public: Mapped[str] = mapped_column(Text)
    nids_sid: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    termsaccepted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    newsread: Mapped[int] = mapped_column(Integer, default=0)
    role_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    change_pw: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    contactalert: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    expiration = mapped_column(DateTime, default=None)
    current_login: Mapped[int] = mapped_column(Integer, default=0)
    last_login: Mapped[int] = mapped_column(Integer, default=0)
    force_logout: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    date_created: Mapped[int] = mapped_column(Integer, default=time)
    date_modified: Mapped[int] = mapped_column(Integer, default=time, onupdate=time)
    sub: Mapped[str] = mapped_column(String(255), unique=True)
    external_auth_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    external_auth_key: Mapped[str] = mapped_column(Text)
    last_api_access: Mapped[int] = mapped_column(Integer, default=0)
    notification_daily: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    notification_weekly: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    notification_monthly: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    totp: Mapped[str] = mapped_column(String(255))
    hotp_counter: Mapped[int] = mapped_column(Integer)
    last_pw_change: Mapped[int] = mapped_column(BigInteger)

    # Relationships
    org = relationship("Organisation", back_populates="users", lazy="raise_on_sql")
    server = relationship(
        "Server",
        primaryjoin="Server.id == User.server_id",
        foreign_keys="User.server_id",
        back_populates="users",
        lazy="raise_on_sql",
    )
    role = relationship(
        "Role",
        primaryjoin="User.role_id == Role.id",
        foreign_keys="User.role_id",
        lazy="raise_on_sql",
    )
