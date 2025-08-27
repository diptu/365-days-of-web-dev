# app/schemas/user.py
from __future__ import annotations

from pydantic import BaseModel, EmailStr, ConfigDict
from .common import CreatedAt


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    email: EmailStr


class UserOut(CreatedAt):
    """Schema for returning user details."""

    id: int
    email: EmailStr

    # Pydantic v2 style ORM mode
    model_config = ConfigDict(from_attributes=True)
