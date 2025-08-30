# app/domain/tenants/schemas.py
from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class MemberCreate(BaseModel):
    email: EmailStr
    full_name: str | None = Field(default=None, max_length=200)


class MemberOut(BaseModel):
    id: str
    email: EmailStr
    full_name: str | None = None
    joined_at: datetime | None = None
