#!/usr/bin/env python3

"""
USAGE:
    - Run `python -m mmisp.db.print_changes`
"""

import asyncio
import pprint
from collections import defaultdict

from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from sqlalchemy import MetaData

import mmisp.db.all_models  # noqa

from .database import Base, sessionmanager

metadata = MetaData()


def create_diff(conn) -> list:  # noqa
    mc = MigrationContext.configure(conn)
    diff = compare_metadata(mc, Base.metadata)  # type:ignore[attr-defined]
    return diff


async def print_changes() -> None:
    changes = defaultdict(list)
    sessionmanager.init()
    assert sessionmanager._engine is not None
    async with sessionmanager._engine.begin() as connection:
        assert connection is not None
        diff = await connection.run_sync(create_diff)
        for elem in diff:
            if isinstance(elem, list):
                for inner_elem in elem:
                    changes[inner_elem[0]].append(inner_elem)
            else:
                changes[elem[0]].append(elem)
    pprint.pprint(changes, indent=2, width=20)
    for k, v in changes.items():
        print(k, len(v))


asyncio.run(print_changes())
