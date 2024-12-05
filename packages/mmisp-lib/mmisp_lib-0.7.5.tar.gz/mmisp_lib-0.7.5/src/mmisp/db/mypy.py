from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.orm import Mapped, mapped_column  # type:ignore[attr-defined]
else:
    from sqlalchemy import Column

    Mapped = Column
    mapped_column = Column
