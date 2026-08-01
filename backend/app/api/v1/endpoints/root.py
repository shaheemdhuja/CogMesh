"""System root information endpoint."""

from datetime import datetime, timezone
from fastapi import APIRouter
from app.core.config import settings
from app.schemas.system import RootResponse
from app.utils.sys_info import get_system_metadata

router = APIRouter()


@router.get(
    "/",
    response_model=RootResponse,
    summary="Get System Root Information",
    description="Returns metadata about the CogMesh node runtime, version, environment, and documentation URL.",
)
async def get_root_info() -> RootResponse:
    """Retrieve system root status and runtime information."""
    return RootResponse(
        name=settings.PROJECT_NAME,
        version=settings.VERSION,
        status="running",
        environment=settings.ENVIRONMENT,
        docs_url="/docs",
        timestamp=datetime.now(timezone.utc).isoformat(),
        system_info=get_system_metadata(),
    )
