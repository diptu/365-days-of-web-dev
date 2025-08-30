# app/v1/routers/orgs.py
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db
from app.domain.org.schemas import OrgCreate, OrgOut
from app.domain.org.repo import get_org_by_slug, create_org

router = APIRouter(tags=["orgs"])


@router.post("/v1/orgs", response_model=OrgOut, status_code=status.HTTP_201_CREATED)
async def create_organization(
    payload: OrgCreate, db: AsyncSession = Depends(get_db)
) -> OrgOut:
    if await get_org_by_slug(db, payload.slug):
        raise HTTPException(status_code=409, detail="slug_already_exists")
    org = await create_org(db, name=payload.name, slug=payload.slug)
    return OrgOut.model_validate(org)
