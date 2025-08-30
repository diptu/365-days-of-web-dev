# app/v1/routers/whoami.py
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.dependencies import get_org_context


class WhoAmI(BaseModel):
    org_id: Optional[str] = None


router = APIRouter(tags=["whoami"])


@router.get("/v1/whoami", response_model=WhoAmI)
async def whoami(ctx: dict = Depends(get_org_context)) -> WhoAmI:
    return WhoAmI(org_id=ctx["org_id"])
