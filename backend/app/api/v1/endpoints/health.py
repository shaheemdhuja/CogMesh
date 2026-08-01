"""System health check endpoint with database ping test."""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.schemas.health import HealthResponse
from app.services.health_service import HealthService

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Get Operational Health Status",
    description="Performs database connection tests ('SELECT 1') and returns readiness metrics for all system components.",
)
async def get_health() -> JSONResponse | HealthResponse:
    """Check health status of database, API server, and system components."""
    health_data = await HealthService.get_health_status()
    
    # Return HTTP 200 OK if healthy, HTTP 533 Service Unavailable if unhealthy
    status_code = status.HTTP_200_OK if health_data.status == "healthy" else status.HTTP_503_SERVICE_UNAVAILABLE
    return JSONResponse(status_code=status_code, content=health_data.model_dump())
