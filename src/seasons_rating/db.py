from __future__ import annotations

from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"
ASYNC_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite3"


def get_engine(url: str = SQLALCHEMY_DATABASE_URL, **kwargs) -> Engine:
    """Create synchronous SQLAlchemy engine."""
    return create_engine(url, future=True, **kwargs)


def get_async_engine(
    url: str = ASYNC_SQLALCHEMY_DATABASE_URL, **kwargs
) -> AsyncEngine:
    """Create asynchronous SQLAlchemy engine."""
    return create_async_engine(url, future=True, **kwargs)


def get_session_maker(engine: Engine) -> sessionmaker[Session]:
    """Create a synchronous session factory bound to *engine*."""
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_async_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Create an asynchronous session factory bound to *engine*."""
    return async_sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Convenience helpers

def session_scope(engine: Engine) -> Generator[Session, None, None]:
    """Context manager yielding a synchronous session."""
    SessionLocal = get_session_maker(engine)
    with SessionLocal() as session:
        yield session


async def async_session_scope(
    engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """Async context manager yielding an asynchronous session."""
    SessionLocal = get_async_session_maker(engine)
    async with SessionLocal() as session:
        yield session
