# app/domain/users/repo.py
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.users.models import User


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    res = await db.execute(select(User).where(User.email == email))
    return res.scalar_one_or_none()


async def create_user(db: AsyncSession, *, email: str, full_name: str | None) -> User:
    user = User(email=email, full_name=full_name)
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user
