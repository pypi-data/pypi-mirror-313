from typing import AsyncGenerator
from src.core.config import settings
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


string_db = (
    f"postgresql+asyncpg://{settings.database_user}:"
    f"{settings.database_password}@{settings.database_host}:5432/"
    f"{settings.database_name}"
)

engine = create_async_engine(
    string_db,
    pool_size=20,
    max_overflow=10,
    echo=False,
)

async_db = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
    class_=AsyncSession,
)


@asynccontextmanager
async def async_session_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_db() as session:
        yield session
