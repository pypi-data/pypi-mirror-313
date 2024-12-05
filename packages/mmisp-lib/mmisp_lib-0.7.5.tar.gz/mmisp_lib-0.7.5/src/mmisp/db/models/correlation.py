from sqlalchemy import Integer, String, Text

from mmisp.db.mypy import Mapped, mapped_column

from ..database import Base


class OverCorrelatingValue(Base):
    """
    Class to represent the table of the over correlating values in the misp_sql database.
    """

    __tablename__ = "over_correlating_values"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    value: Mapped[str] = mapped_column(String(191), nullable=False, index=True, unique=True)
    occurrence: Mapped[int] = mapped_column(Integer, nullable=False, index=True)


class CorrelationValue(Base):
    """
    Class to represent the table of the correlation values in the misp_sql database.
    """

    __tablename__ = "correlation_values"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    value: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True)


class CorrelationExclusions(Base):
    __tablename__ = "correlation_exclusions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    value: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True)
    from_json: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    comment: Mapped[str] = mapped_column(Text, nullable=False)


class DefaultCorrelation(Base):
    __tablename__ = "default_correlations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    attribute_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    object_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    org_id: Mapped[int] = mapped_column(Integer, nullable=False)
    distribution: Mapped[int] = mapped_column(Integer, nullable=False)
    object_distribution: Mapped[int] = mapped_column(Integer, nullable=False)
    event_distribution: Mapped[int] = mapped_column(Integer, nullable=False)
    sharing_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    object_sharing_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    event_sharing_group_id: Mapped[int] = mapped_column(Integer, nullable=False)
    attribute_id_1: Mapped[int] = mapped_column("1_attribute_id", Integer, nullable=False, index=True)
    object_id_1: Mapped[int] = mapped_column("1_object_id", Integer, nullable=False, index=True)
    event_id_1: Mapped[int] = mapped_column("1_event_id", Integer, nullable=False, index=True)
    org_id_1: Mapped[int] = mapped_column("1_org_id", Integer, nullable=False)
    distribution_1: Mapped[int] = mapped_column("1_distribution", Integer, nullable=False)
    object_distribution_1: Mapped[int] = mapped_column("1_object_distribution", Integer, nullable=False)
    event_distribution_1: Mapped[int] = mapped_column("1_event_distribution", Integer, nullable=False)
    sharing_group_id_1: Mapped[int] = mapped_column("1_sharing_group_id", Integer, nullable=False)
    object_sharing_group_id_1: Mapped[int] = mapped_column("1_object_sharing_group_id", Integer, nullable=False)
    event_sharing_group_id_1: Mapped[int] = mapped_column("1_event_sharing_group_id", Integer, nullable=False)
    value_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
