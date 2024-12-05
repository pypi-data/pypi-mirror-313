from typing import Any, Self

from sqlalchemy.engine import Dialect
from sqlalchemy.types import String, TypeDecorator


class DBUUID(TypeDecorator):
    impl = String

    def load_dialect_impl(self: Self, dialect: Dialect) -> Any:
        return dialect.type_descriptor(String(36))

    def process_bind_param(self: Self, value: Any, dialect: Dialect) -> str | None:
        if value is None:
            return None
        return str(value)

    def process_result_value(self: Self, value: Any, dialect: Dialect) -> str:
        return value
