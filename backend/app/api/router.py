"""Main API router including versioned endpoints."""

from fastapi import APIRouter
from app.api.v1.router import api_v1_router
from app.core.config import settings

api_router = APIRouter()

# Mount API V1 routes under prefix (e.g. /api/v1)
api_router.include_router(api_v1_router, prefix=settings.API_V1_STR)
