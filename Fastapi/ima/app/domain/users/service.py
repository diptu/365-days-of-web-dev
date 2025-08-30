from sqlalchemy.ext.asyncio import AsyncSession

from . import repo
from .models import User


async def ensure_user(db: AsyncSession, *, name: str, email: str) -> User:
    """Idempotent helper to get-or-create a user by email."""
    found = await repo.get_by_email(db, email)
    if found:
        return found
    return await repo.create(db, name=name, email=email)
