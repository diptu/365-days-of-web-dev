# app/models/base.py
from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """Declarative base with auto __tablename__ = lowercased class name."""

    # NOTE: declared_attr already behaves like a classmethod.
    @declared_attr.directive
    def __tablename__(cls) -> str:  # pylint: disable=no-self-argument
        return cls.__name__.lower()
