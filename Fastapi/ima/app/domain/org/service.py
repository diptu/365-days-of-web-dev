from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.org.repo import get_org_by_slug, create_org as repo_create_org


async def create_org(session: AsyncSession, name: str, slug: str):
    # Enforce unique slug
    existing = await get_org_by_slug(session, slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Slug already exists",
        )
    return await repo_create_org(session, name=name, slug=slug)
