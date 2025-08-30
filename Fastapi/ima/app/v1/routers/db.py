# app/v1/routers/db.py
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db

router = APIRouter(tags=["db"])


@router.get("/v1/db-ping")
async def db_ping(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    # Simple connectivity probe
    await db.execute(text("SELECT 1"))
    return {"status": "ok"}
