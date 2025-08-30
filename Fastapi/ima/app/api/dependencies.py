# app/api/dependencies.py
from __future__ import annotations

from fastapi import Request


def get_org_context(request: Request) -> dict[str, str | None]:
    """
    Returns a small org context dict. Routers can depend on this.
    """
    return {"org_id": getattr(request.state, "org_id", None)}
