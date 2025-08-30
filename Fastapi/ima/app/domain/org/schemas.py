# app/domain/org/schemas.py
from __future__ import annotations
from uuid import UUID
from pydantic import BaseModel, Field


class OrgCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=1, max_length=120, pattern=r"^[a-z0-9-]+$")


class OrgOut(BaseModel):
    id: UUID  # ✅ use UUID, not str
    name: str
    slug: str

    model_config = {"from_attributes": True}  # pydantic v2 style
