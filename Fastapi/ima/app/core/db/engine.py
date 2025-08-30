# app/core/db/engine.py
from __future__ import annotations

from sqlalchemy import pool  # ✅ add this
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import settings


def get_async_engine() -> AsyncEngine:
    """
    One global async engine for Postgres (asyncpg).
    - Uses settings.DATABASE_URL normalized to postgresql+asyncpg
    - Passes a real boolean 'ssl' via connect_args for asyncpg
    - NullPool avoids background pool tasks across event loops (tests)
    """
    return create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        poolclass=pool.NullPool,  # ✅ key change
        connect_args={"ssl": settings.ASYNCPG_SSL},
    )


engine: AsyncEngine = get_async_engine()
