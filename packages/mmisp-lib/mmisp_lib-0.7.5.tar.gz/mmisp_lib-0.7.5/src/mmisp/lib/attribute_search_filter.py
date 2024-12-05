from typing import TYPE_CHECKING

from sqlalchemy import and_

from mmisp.db.models.attribute import Attribute

if TYPE_CHECKING:
    from sqlalchemy import ColumnExpressionArgument
else:
    ColumnExpressionArgument = any


def get_search_filters(
    value: str | None = None,
    value1: str | None = None,
    value2: str | None = None,
    type: str | None = None,
    category: str | None = None,
    org: str | None = None,
    tags: list[str] | None = None,
    from_: str | None = None,
    to: str | None = None,
    last: int | None = None,
    eventid: str | None = None,
    published: bool | None = None,
    to_ids: bool | None = None,
    deleted: bool | None = None,
    **kwargs,
) -> ColumnExpressionArgument:
    cond = [True]  # for empty filters
    if value is not None:
        cond.append(Attribute.value == value)
    if value1 is not None:
        cond.append(Attribute.value1 == value1)
    if value2 is not None:
        cond.append(Attribute.value2 == value2)
    if type is not None:
        cond.append(Attribute.type == type)
    if category is not None:
        cond.append(Attribute.category == category)
    if org is not None:
        raise NotImplementedError("filtering by org is currently not implemented")
    if tags is not None:
        raise NotImplementedError("filtering by tags is currently not implemented")
    if from_ is not None:
        raise NotImplementedError("filtering by from is currently not implemented")
    if to is not None:
        raise NotImplementedError("filtering by to is currently not implemented")
    if last is not None:
        raise NotImplementedError("filtering by last is currently not implemented")
    if eventid is not None:
        raise NotImplementedError("filtering by eventid is currently not implemented")
    if published is not None:
        raise NotImplementedError("filtering by published is currently not implemented")
    if to_ids is not None:
        cond.append(Attribute.to_ids == to_ids)
    if deleted is not None:
        cond.append(Attribute.deleted == deleted)

    return and_(*cond)
