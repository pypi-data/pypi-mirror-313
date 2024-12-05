from sqlalchemy import DateTime, Integer, Text, text
from sqlalchemy.dialects.mysql import INTEGER

from mmisp.db.mypy import Mapped, mapped_column

from ..database import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    date_created: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    date_modified: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    user_id: Mapped[int] = mapped_column(INTEGER, nullable=False)
    contents: Mapped[str] = mapped_column(Text, nullable=False)
    post_id: Mapped[int] = mapped_column(INTEGER, nullable=False, index=True, server_default=text("0"))
    thread_id: Mapped[int] = mapped_column(INTEGER, nullable=False, index=True, server_default=text("0"))
