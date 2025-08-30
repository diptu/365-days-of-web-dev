# app/api/dependencies.py
from __future__ import annotations

from fastapi import Request

from typing import AsyncGenerator
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import AsyncSessionLocal
from app.core.db.tenancy import slug_to_schema, set_search_path


async def get_tenant_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = AsyncSessionLocal()
    try:
        org_id = getattr(request.state, "org_id", None)
        if org_id:
            await set_search_path(session, slug_to_schema(org_id))
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


def get_org_context(request: Request) -> dict[str, str | None]:
    """
    Returns a small org context dict. Routers can depend on this.
    """
    return {"org_id": getattr(request.state, "org_id", None)}
