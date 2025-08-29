# app/v1/api.py
from fastapi import APIRouter
from app.core.routes.student import router as student_router

api_router = APIRouter()

# mount feature routers here
api_router.include_router(student_router, prefix="/students", tags=["students"])
