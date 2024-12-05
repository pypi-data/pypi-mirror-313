from sqlalchemy import Boolean, Integer, String, Text

from mmisp.db.mypy import Mapped, mapped_column

from ..database import Base


class WorkflowBlueprint(Base):
    """
    A python class representation of the database model for blueprints of workflows in MISP.

    The most attributes of this model are similar to the attributes of workflows,
    except the attributes "enabled", "counter", "trigger_id" and "debug_enabled", because these
    attributes are not useful or sensible for blueprints.

    Also, the attribute "default" is added, which is a boolean clarifying whether the blueprint
    is a default MISP blueprint.
    """

    __tablename__ = "workflow_blueprints"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)  # primary_key ??
    uuid: Mapped[str] = mapped_column(String(40), nullable=False)
    name: Mapped[str] = mapped_column(String(191), nullable=False)
    description: Mapped[str] = mapped_column(String(191), nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)  # TODO: technically tinyint(1)
    data: Mapped[str] = mapped_column(Text, nullable=True)
