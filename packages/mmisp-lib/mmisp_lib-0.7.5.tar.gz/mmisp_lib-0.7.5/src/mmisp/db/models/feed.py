from sqlalchemy import Boolean, Integer, String, Text

from mmisp.db.database import Base
from mmisp.db.mypy import Mapped, mapped_column


class Feed(Base):
    __tablename__ = "feeds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    provider: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    rules: Mapped[str] = mapped_column(Text, default=None)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    distribution: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sharing_group_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    tag_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    default: Mapped[bool] = mapped_column(Boolean, default=False)
    source_format: Mapped[str] = mapped_column(String(255), default="misp")
    fixed_event: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    delta_merge: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    publish: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    override_ids: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    settings: Mapped[str] = mapped_column(Text)
    input_source: Mapped[str] = mapped_column(String(255), nullable=False, default="network", index=True)
    delete_local_file: Mapped[bool] = mapped_column(Boolean, default=False)
    lookup_visible: Mapped[bool] = mapped_column(Boolean, default=False)
    headers: Mapped[str] = mapped_column(Text)
    caching_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    force_to_ids: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    orgc_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
