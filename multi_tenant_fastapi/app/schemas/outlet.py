# app/schemas/outlet.py
from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict
from .common import CreatedAt


class OutletCreate(BaseModel):
    code: str = Field(..., min_length=1, max_length=64, pattern=r"^[a-z0-9_-]+$")
    name: str = Field(..., min_length=1, max_length=255)


class OutletOut(CreatedAt):
    id: int
    code: str
    name: str
    model_config = ConfigDict(from_attributes=True)
