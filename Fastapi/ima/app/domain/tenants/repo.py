# app/domain/tenants/repo.py
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tenants.models import OrgUser, Membership


async def get_org_user_by_email(db: AsyncSession, email: str) -> OrgUser | None:
    res = await db.execute(select(OrgUser).where(OrgUser.email == email))
    return res.scalar_one_or_none()


async def create_org_user(
    db: AsyncSession, *, email: str, full_name: str | None
) -> OrgUser:
    user = OrgUser(email=email, full_name=full_name)
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


async def create_membership(db: AsyncSession, *, user_id) -> Membership:
    m = Membership(user_id=user_id)
    db.add(m)
    await db.flush()
    await db.refresh(m)
    return m


async def create_member(
    db: AsyncSession, *, email: str, full_name: str | None
) -> tuple[OrgUser, Membership]:
    """
    If the user doesn't exist in this tenant schema, create it; then add a membership.
    """
    user = await get_org_user_by_email(db, email)
    if not user:
        user = await create_org_user(db, email=email, full_name=full_name)
    mem = await create_membership(db, user_id=user.id)
    return user, mem


async def list_members(db: AsyncSession) -> list[tuple[OrgUser, Membership | None]]:
    """
    Return OrgUsers with their (optional) membership rows.
    """
    stmt = (
        select(OrgUser, Membership)
        .join(Membership, Membership.user_id == OrgUser.id, isouter=True)
        .order_by(OrgUser.created_at.desc())
    )
    res = await db.execute(stmt)
    return list(res.all())
