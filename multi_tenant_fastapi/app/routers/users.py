# app/routers/users.py
from __future__ import annotations

from typing import Annotated, Generator

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..models.shared import User, Outlet
from ..schemas.user import UserCreate, UserOut
from ..tenancy.context import get_current_outlet

router = APIRouter(prefix="/users", tags=["users"])


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Db = Annotated[Session, Depends(get_db)]


def _resolve_outlet_id(db: Session) -> int | None:
    code = get_current_outlet()
    if not code:
        return None
    outlet = db.execute(select(Outlet).where(Outlet.code == code)).scalar_one_or_none()
    if not outlet:
        raise HTTPException(status_code=404, detail="Outlet not found.")
    return outlet.id


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Db) -> UserOut:
    outlet_id = _resolve_outlet_id(db)  # None at tenant root → central user
    user = User(email=payload.email, outlet_id=outlet_id)
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists.") from exc
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: Annotated[int, Path(ge=1)], db: Db) -> UserOut:
    # On outlet subdomain, you can only access users in that outlet
    outlet_id = _resolve_outlet_id(db)
    stmt = select(User).where(User.id == user_id)
    if outlet_id is not None:
        stmt = stmt.where((User.outlet_id == outlet_id))
    user = db.execute(stmt).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user
