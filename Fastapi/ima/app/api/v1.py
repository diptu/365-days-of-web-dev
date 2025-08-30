# app/api/v1.py
from __future__ import annotations
from fastapi import APIRouter

from app.v1.routers.health import router as health_router
from app.v1.routers.db import router as db_router
from app.v1.routers.whoami import router as whoami_router
from app.v1.routers.orgs import router as orgs_router  # ← ensure this import exists
from app.v1.routers.users import router as users_router  # optional but recommended

api_v1 = APIRouter()
api_v1.include_router(health_router)
api_v1.include_router(db_router)
api_v1.include_router(whoami_router)
api_v1.include_router(orgs_router)  # ← ensure this line exists
api_v1.include_router(users_router)  # optional
