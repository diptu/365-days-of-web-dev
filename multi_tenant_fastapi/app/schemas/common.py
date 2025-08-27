# app/schemas/common.py
from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class Paging(BaseModel):
    """Common pagination parameters."""

    limit: int = Field(default=20, ge=1, le=100, description="Max items per page")
    offset: int = Field(default=0, ge=0, description="Number of items to skip")


class CreatedAt(BaseModel):
    """Common field for created_at timestamps."""

    created_at: datetime
