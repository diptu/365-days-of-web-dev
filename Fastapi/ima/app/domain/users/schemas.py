# app/domain/users/schemas.py
from __future__ import annotations
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str | None = Field(default=None, max_length=200)


class UserOut(BaseModel):
    id: UUID  # ✅ use UUID, not str
    email: EmailStr
    full_name: str | None = None

    model_config = {"from_attributes": True}
