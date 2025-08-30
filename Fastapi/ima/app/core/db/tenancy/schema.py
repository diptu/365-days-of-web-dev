# app/core/db/tenancy/schema.py
from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from app.core.db.tenancy.names import slug_to_schema


async def ensure_schema_for_org(session: AsyncSession, slug: str) -> str:
    """
    Create tenant schema if it doesn't exist. No-op if it does.
    Returns the schema name.
    """
    schema = slug_to_schema(slug)
    conn: AsyncConnection = await session.connection()  # ✅ await
    await conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
    return schema


async def set_search_path(session: AsyncSession, schema: str) -> None:
    """
    Set search_path to the given schema followed by public.
    Use within a transaction for per-request isolation where needed.
    """
    conn: AsyncConnection = await session.connection()  # ✅ await
    await conn.execute(text(f'SET search_path TO "{schema}", public'))
