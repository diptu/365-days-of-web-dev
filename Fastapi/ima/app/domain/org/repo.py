# app/domain/org/repo.py
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.org.models import Organization


async def get_org_by_slug(db: AsyncSession, slug: str) -> Organization | None:
    res = await db.execute(select(Organization).where(Organization.slug == slug))
    return res.scalar_one_or_none()


async def create_org(db: AsyncSession, *, name: str, slug: str) -> Organization:
    org = Organization(name=name, slug=slug)
    db.add(org)
    await db.flush()  # get PK
    await db.refresh(org)
    return org
