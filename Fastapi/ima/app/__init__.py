# app/__init__.py
from __future__ import annotations

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_v1
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.db.engine import engine

# Configure logging early
configure_logging(debug=settings.DEBUG)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    # Dispose async engine cleanly on shutdown (prevents dangling tasks)
    await engine.dispose()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)


# Function-based middleware (no BaseHTTPMiddleware)
@app.middleware("http")
async def org_context_middleware(request: Request, call_next):
    org_id = request.headers.get("x-org-id")
    request.state.org_id = (org_id.strip() or None) if org_id else None
    return await call_next(request)


# ✅ Disable CORS in tests by checking the ENV directly (not the cached settings)
_is_testing = os.getenv("IMA_TESTING", "").lower() == "true"
if settings.CORS_ORIGINS and not _is_testing:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Routers
app.include_router(api_v1)
