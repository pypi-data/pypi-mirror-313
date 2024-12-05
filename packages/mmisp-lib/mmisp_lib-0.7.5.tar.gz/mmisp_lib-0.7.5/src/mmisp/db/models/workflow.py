from uuid import uuid4 as _uuid4

from sqlalchemy import Boolean, Integer, String

from mmisp.db.mypy import Mapped, mapped_column

from ...workflows.graph import WorkflowGraph
from ...workflows.legacy import JSONGraphType
from ..database import Base


def uuid() -> str:
    return str(_uuid4())


class Workflow(Base):
    """
    A python class representation of the database model for workflows in MISP.

    The most central of the attributes in this model is the data attribute,
    containing the information about the workflow structure and the modules contained in the workflow,
    represented/stored as a JSON-String.
    (The other attributes are what their name sais, e.g. counter represents the numer
    of times the workflow was executed.)
    """

    __tablename__ = "workflows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String(40), default=uuid, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(191), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(191), nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    counter: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    trigger_id: Mapped[str] = mapped_column(String(191), nullable=False, index=True)
    debug_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=0)
    data: Mapped[WorkflowGraph] = mapped_column(JSONGraphType, nullable=False, default=0)
