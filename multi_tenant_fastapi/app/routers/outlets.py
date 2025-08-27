# app/routers/outlets.py
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..models.shared import Outlet
from ..schemas.outlet import OutletCreate, OutletOut
from ..tenancy.context import get_current_outlet

router = APIRouter(prefix="/outlets", tags=["outlets"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Db = Annotated[Session, Depends(get_db)]


@router.post("", response_model=OutletOut, status_code=status.HTTP_201_CREATED)
def create_outlet(payload: OutletCreate, db: Db) -> OutletOut:
    if get_current_outlet():
        # You are on outlet subdomain; creation only allowed at tenant root
        raise HTTPException(
            status_code=403, detail="Create outlets from tenant domain."
        )
    outlet = Outlet(code=payload.code, name=payload.name)
    db.add(outlet)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="Outlet code already exists."
        ) from exc
    db.refresh(outlet)
    return outlet


@router.get("", response_model=list[OutletOut])
def list_outlets(db: Db) -> list[OutletOut]:
    if get_current_outlet():
        # On outlet subdomain, show only self
        stmt = select(Outlet).where(Outlet.code == get_current_outlet())
        return db.execute(stmt).scalars().all()
    # Tenant-level: list all
    stmt = select(Outlet).order_by(Outlet.id)
    return db.execute(stmt).scalars().all()
