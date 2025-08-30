# app/v1/routers/health.py
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/v1/health", tags=["health"])


@router.get("")
async def health() -> dict[str, str]:
    return {"status": "ok"}
