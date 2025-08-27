# app/schemas/note.py
from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict
from .common import CreatedAt


class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Note title")
    body: str | None = Field(default=None, description="Optional note body")


class NoteOut(CreatedAt):
    id: int
    title: str
    body: str | None = None

    # Pydantic v2: enable ORM mode for SQLAlchemy instances
    model_config = ConfigDict(from_attributes=True)
