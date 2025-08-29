from fastapi import APIRouter
from app.v1.routers.health import router as health_router
from app.v1.routers.db import router as db_router
from app.v1.routers.whoami import router as whoami_router

api = APIRouter(prefix="/v1")
api.include_router(health_router)
api.include_router(db_router)
api.include_router(whoami_router)
