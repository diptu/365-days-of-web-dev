# app/tests/utils/ensure_tenant_tables.py
from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

TENANT_TABLE_DDL = [
    # org_users
    """
    CREATE TABLE IF NOT EXISTS org_users (
        id uuid PRIMARY KEY,
        email varchar(320) NOT NULL UNIQUE,
        full_name varchar(200),
        created_at timestamptz NOT NULL DEFAULT now()
    );
    """,
    "CREATE INDEX IF NOT EXISTS ix_org_users_email ON org_users (email);",
    # memberships
    """
    CREATE TABLE IF NOT EXISTS memberships (
        id uuid PRIMARY KEY,
        user_id uuid NOT NULL REFERENCES org_users(id) ON DELETE CASCADE,
        joined_at timestamptz NOT NULL DEFAULT now()
    );
    """,
    "CREATE INDEX IF NOT EXISTS ix_memberships_user_id ON memberships (user_id);",
]


async def ensure_tenant_tables(session: AsyncSession, schema: str) -> None:
    # Target the tenant schema for unqualified DDL
    await session.execute(text(f'SET search_path TO "{schema}", public'))
    for ddl in TENANT_TABLE_DDL:
        await session.execute(text(ddl))
    await session.commit()
