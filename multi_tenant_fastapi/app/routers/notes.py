from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..models.shared import Note, Outlet
from ..schemas.note import NoteCreate, NoteOut
from ..tenancy.context import get_current_outlet

router = APIRouter(prefix="/notes", tags=["notes"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Limit = Annotated[int, Query(ge=1, le=100)]
Offset = Annotated[int, Query(ge=0)]
Db = Annotated[Session, Depends(get_db)]  # alias


@router.get("", response_model=list[NoteOut])
def list_notes(
    db: Db,  # non-default first
    limit: Limit = 20,  # then defaults
    offset: Offset = 0,
) -> list[NoteOut]:
    stmt = select(Note).order_by(Note.id).limit(limit).offset(offset)
    return db.execute(stmt).scalars().all()
