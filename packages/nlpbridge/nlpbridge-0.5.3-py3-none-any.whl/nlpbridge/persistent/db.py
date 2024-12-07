import contextlib
from typing import Any, AsyncIterator

from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from nlpbridge.config import CONFIG


class Base(DeclarativeBase):
    # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
    __mapper_args__ = {"eager_defaults": True}


# Heavily inspired by https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html
class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine, expire_on_commit=False)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")
        try:
            session = self._sessionmaker()
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.invalidate()


SQLALCHEMY_DATABASE_URI = f"mysql+asyncmy://{CONFIG.mysql.user}:{CONFIG.mysql.password}@{CONFIG.mysql.host}:{CONFIG.mysql.port}/{CONFIG.mysql.db}"
engine_kwargs = {"pool_size": 64, "max_overflow": 0, "pool_recycle": 3600, "pool_pre_ping": True, "echo": False,
                 "echo_pool": True, "poolclass": AsyncAdaptedQueuePool, "pool_timeout": 5}
sessionmanager = DatabaseSessionManager(SQLALCHEMY_DATABASE_URI, engine_kwargs)
