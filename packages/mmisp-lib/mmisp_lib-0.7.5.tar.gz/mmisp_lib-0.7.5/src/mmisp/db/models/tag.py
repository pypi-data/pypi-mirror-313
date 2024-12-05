from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import relationship

from mmisp.db.database import Base
from mmisp.db.mypy import Mapped, mapped_column


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    colour: Mapped[int] = mapped_column(String(7), nullable=False)
    exportable: Mapped[bool] = mapped_column(Boolean, nullable=False)
    org_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    hide_tag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    numerical_value: Mapped[int] = mapped_column(Integer, index=True)
    is_galaxy: Mapped[bool] = mapped_column(Boolean, default=False)
    is_custom_galaxy: Mapped[bool] = mapped_column(Boolean, default=False)
    local_only: Mapped[bool] = mapped_column(Boolean, default=False)

    attributetags = relationship("AttributeTag", back_populates="tag", lazy="raise_on_sql", viewonly=True)
    eventtags = relationship("EventTag", back_populates="tag", lazy="raise_on_sql", viewonly=True)
    galaxy_cluster = relationship(
        "GalaxyCluster",
        primaryjoin="Tag.name == GalaxyCluster.tag_name",
        back_populates="tag",
        lazy="raise_on_sql",
        foreign_keys="GalaxyCluster.tag_name",
        single_parent=True,
        uselist=False,
    )  # type:ignore[assignment,var-annotated]
