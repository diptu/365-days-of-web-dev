from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


class OrgContextMiddleware(BaseHTTPMiddleware):
    """Stores X-Org-ID (if provided) on request.state.org_id."""

    async def dispatch(self, request: Request, call_next):
        request.state.org_id = request.headers.get("X-Org-ID")
        return await call_next(request)
