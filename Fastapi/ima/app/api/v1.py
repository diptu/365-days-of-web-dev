# app/api/v1.py (or app/api/v1/__init__.py)
from __future__ import annotations
from fastapi import APIRouter

from app.v1.routers.health import router as health_router
from app.v1.routers.db import router as db_router
from app.v1.routers.whoami import router as whoami_router
from app.v1.routers.orgs import router as orgs_router
from app.v1.routers.users import router as users_router
from app.v1.routers.members import router as members_router  # ✅

api_v1 = APIRouter()
api_v1.include_router(health_router)
api_v1.include_router(db_router)
api_v1.include_router(whoami_router)
api_v1.include_router(orgs_router)
api_v1.include_router(users_router)
api_v1.include_router(members_router)  # ✅
