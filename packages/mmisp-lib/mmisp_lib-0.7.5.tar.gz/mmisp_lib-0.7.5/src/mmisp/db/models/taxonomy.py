from sqlalchemy import Boolean, ForeignKey, Integer, String, Text

from mmisp.db.mypy import Mapped, mapped_column

from ..database import Base


class Taxonomy(Base):
    __tablename__ = "taxonomies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    namespace: Mapped[int] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    exclusive: Mapped[bool] = mapped_column(Boolean, default=False)
    required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    highlighted: Mapped[bool] = mapped_column(Boolean)


class TaxonomyPredicate(Base):
    __tablename__ = "taxonomy_predicates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    taxonomy_id: Mapped[int] = mapped_column(Integer, ForeignKey(Taxonomy.id), nullable=False, index=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    expanded: Mapped[str] = mapped_column(Text)
    colour: Mapped[str] = mapped_column(String(7))
    description: Mapped[str] = mapped_column(Text)
    exclusive: Mapped[bool] = mapped_column(Boolean, default=False)
    numerical_value: Mapped[int] = mapped_column(Integer, index=True)


class TaxonomyEntry(Base):
    __tablename__ = "taxonomy_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    taxonomy_predicate_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(TaxonomyPredicate.id), nullable=False, index=True
    )
    value: Mapped[str] = mapped_column(Text, nullable=False)
    expanded: Mapped[str] = mapped_column(Text)
    colour: Mapped[str] = mapped_column(String(7))
    description: Mapped[str] = mapped_column(Text)
    numerical_value: Mapped[int] = mapped_column(Integer, index=True)
