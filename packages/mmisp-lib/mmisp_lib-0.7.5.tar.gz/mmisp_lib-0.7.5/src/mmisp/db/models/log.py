from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text

from mmisp.db.mypy import Mapped, mapped_column

from ..database import Base


class Log(Base):
    """
    A python class representation of the database model for logs in MISP.

    Further explanation for some of the central attributes of the database model:
    - Action: Describes the action that was logged, e.g. a login or workflow execution
    - Change: A string-representation of the changes made to the logged object or of
              central information about the logged object.
    """

    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=True)
    created: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    model: Mapped[str] = mapped_column(String(80), nullable=False)
    model_id: Mapped[int] = mapped_column(Integer, nullable=False)
    action: Mapped[str] = mapped_column(String(20), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    change: Mapped[str] = mapped_column(Text, nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    org: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    ip: Mapped[str] = mapped_column(String(45), nullable=True)
