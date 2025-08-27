# app/models/shared.py
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Outlet(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(
        String(64), unique=True, index=True, nullable=False
    )  # slug like 'dhaka-01'
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    users: Mapped[list["User"]] = relationship(
        back_populates="outlet", cascade="all,delete-orphan"
    )
    notes: Mapped[list["Note"]] = relationship(
        back_populates="outlet", cascade="all,delete-orphan"
    )


class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )

    # Optional: central control users have outlet_id = NULL
    outlet_id: Mapped[int | None] = mapped_column(
        ForeignKey("outlet.id"), nullable=True, index=True
    )
    outlet: Mapped[Outlet | None] = relationship(back_populates="users")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Note(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Notes are per-outlet; keep it required
    outlet_id: Mapped[int] = mapped_column(
        ForeignKey("outlet.id"), nullable=False, index=True
    )
    outlet: Mapped[Outlet] = relationship(back_populates="notes")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
