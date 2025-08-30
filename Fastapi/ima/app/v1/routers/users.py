# app/v1/routers/users.py
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_db
from app.domain.users.schemas import UserCreate, UserOut
from app.domain.users.repo import get_user_by_email, create_user

router = APIRouter(tags=["users"])


@router.post("/v1/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user_handler(
    payload: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserOut:
    if await get_user_by_email(db, payload.email):
        raise HTTPException(status_code=409, detail="email_already_exists")
    user = await create_user(db, email=payload.email, full_name=payload.full_name)
    return UserOut.model_validate(user)
