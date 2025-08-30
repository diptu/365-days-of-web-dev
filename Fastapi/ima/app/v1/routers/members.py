# app/v1/routers/members.py
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_tenant_db
from app.domain.tenants.schemas import MemberCreate, MemberOut
from app.domain.tenants.repo import create_member, list_members

router = APIRouter(tags=["members"])


@router.get("/v1/members", response_model=list[MemberOut])
async def get_members(db: AsyncSession = Depends(get_tenant_db)) -> list[MemberOut]:
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="missing_tenant_context"
        )
    rows = await list_members(db)
    out: list[MemberOut] = []
    for org_user, membership in rows:
        out.append(
            MemberOut(
                id=str(org_user.id),
                email=org_user.email,
                full_name=org_user.full_name,
                joined_at=membership.joined_at if membership else None,
            )
        )
    return out


@router.post(
    "/v1/members", response_model=MemberOut, status_code=status.HTTP_201_CREATED
)
async def create_member_handler(
    payload: MemberCreate,
    db: AsyncSession = Depends(get_tenant_db),
) -> MemberOut:
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="missing_tenant_context"
        )
    user, membership = await create_member(
        db, email=payload.email, full_name=payload.full_name
    )
    return MemberOut(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        joined_at=membership.joined_at,
    )
