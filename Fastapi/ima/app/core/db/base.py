# app/core/db/base.py
from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Global SQLAlchemy declarative base."""

    pass


# Alembic will import model modules in env.py so autogenerate sees them.
