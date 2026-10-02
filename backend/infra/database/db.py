from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.infra.config.settings import settings
from backend.infra.database.base import Base
from backend.infra.database.entities import load_entities

settings.db_path.parent.mkdir(parents=True, exist_ok=True)


engine = create_async_engine(
    f"sqlite+aiosqlite:///{settings.db_path.as_posix()}",
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with SessionLocal() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise


async def init_db() -> None:
    load_entities()

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    await engine.dispose()