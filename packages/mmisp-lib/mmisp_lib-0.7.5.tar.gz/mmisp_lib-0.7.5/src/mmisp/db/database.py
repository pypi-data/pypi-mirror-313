import contextlib
import time
from collections.abc import AsyncIterator
from typing import Self, TypeAlias

from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

from mmisp.db.config import config

Session: TypeAlias = AsyncSession

# , poolclass=NullPool)
# async_session = sessionmaker(autoflush=False, expire_on_commit=False, class_=AsyncSession, bind=engine)

Base = declarative_base()

_no_database: str = "DatabaseSessionManager is not initialized"


class DatabaseSessionManager:
    def __init__(self: Self, db_url: str = config.DATABASE_URL) -> None:
        self._engine: AsyncEngine | None = None
        self._sessionmaker: sessionmaker | None = None

        self._url = make_url(db_url)

    def init(self: Self, nullpool: bool = False) -> None:
        retries = 0
        while retries < config.MAX_RETRIES:
            try:
                if nullpool:
                    self._engine = create_async_engine(
                        self._url, echo=False, hide_parameters=not (config.DEBUG), poolclass=NullPool
                    )
                else:
                    self._engine = create_async_engine(self._url, echo=False, hide_parameters=not (config.DEBUG))
                break
            except OperationalError as e:
                retries += 1
                print(f"Attempt {retries} failed: {e}")
                time.sleep(config.RETRY_SLEEP)
        self._sessionmaker = sessionmaker(
            autocommit=False, autoflush=False, expire_on_commit=False, bind=self._engine, class_=AsyncSession
        )

    async def close(self: Self) -> None:
        if self._engine is None:
            raise Exception(_no_database)
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self: Self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception(_no_database)

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self: Self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception(_no_database)

        session = self._sessionmaker()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    # Used for testing
    async def create_all(self: Self, engine: AsyncEngine | None = None) -> None:
        if engine is None:
            engine = self._engine

        retries = 0
        while retries < config.MAX_RETRIES:
            try:
                async with engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
                break
            except OperationalError as e:
                retries += 1
                print(f"Attempt {retries} failed: {e}")
                time.sleep(config.RETRY_SLEEP)

    async def drop_all(self: Self, engine: AsyncEngine | None = None) -> None:
        if engine is None:
            engine = self._engine
        assert engine is not None
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)  # type:ignore[attr-defined]


async def get_db() -> AsyncIterator[Session]:
    async with sessionmanager.session() as session:
        yield session


async def create_all_models() -> None:
    await sessionmanager.create_all()


sessionmanager = DatabaseSessionManager()
