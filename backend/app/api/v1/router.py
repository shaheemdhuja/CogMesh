"""API V1 Router combining v1 endpoint sub-routers."""

from fastapi import APIRouter
from app.api.v1.endpoints import health, root

api_v1_router = APIRouter()

# Include endpoint routers with tags
api_v1_router.include_router(root.router, tags=["System Root"])
api_v1_router.include_router(health.router, tags=["Health Assessment"])
