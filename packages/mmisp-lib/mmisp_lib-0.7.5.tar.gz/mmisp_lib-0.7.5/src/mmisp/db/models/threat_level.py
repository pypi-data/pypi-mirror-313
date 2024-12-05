from sqlalchemy import Integer, String

from mmisp.db.mypy import Mapped, mapped_column

from ..database import Base


class ThreatLevel(Base):
    __tablename__ = "threat_levels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    form_description: Mapped[str] = mapped_column(String(255), nullable=False)
