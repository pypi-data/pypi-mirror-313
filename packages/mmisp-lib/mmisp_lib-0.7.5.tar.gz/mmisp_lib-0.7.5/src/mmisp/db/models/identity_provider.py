from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String

from mmisp.db.mypy import Mapped, mapped_column

from ..database import Base


class OIDCIdentityProvider(Base):
    __tablename__ = "oidc_identity_providers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    org_id: Mapped[int] = mapped_column(Integer, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    base_url: Mapped[str] = mapped_column(String(255), nullable=False)
    client_id: Mapped[str] = mapped_column(String(255), nullable=False)
    client_secret: Mapped[str] = mapped_column(String(255), nullable=False)
    scope: Mapped[str] = mapped_column(String(255))
    """Possibility to add more scopes to be requested from the idp in addition to the default scopes,
    currently not used."""
    created: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    modified: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
