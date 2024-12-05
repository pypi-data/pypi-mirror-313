from sqlalchemy import Integer, String, Text

from mmisp.db.mypy import Mapped, mapped_column

from ..database import Base


class AdminSetting(Base):
    """
    A python class representation of the database model for admin settings in MISP
    """

    __tablename__ = "admin_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    setting: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
