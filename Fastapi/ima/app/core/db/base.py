# app/core/db/base.py
from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Global SQLAlchemy declarative base."""

    pass
