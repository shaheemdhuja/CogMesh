"""Pydantic v2 schemas for health check endpoint GET /health."""

from typing import Dict, Optional
from pydantic import BaseModel, Field


class DatabaseHealth(BaseModel):
    """Database connectivity and health metrics schema."""

    status: str = Field(..., description="Database connection status: 'connected' or 'disconnected'")
    latency_ms: Optional[float] = Field(None, description="Query execution latency in milliseconds")
    engine: str = Field(..., description="Database dialect/engine name")


class HealthResponse(BaseModel):
    """Full health check endpoint response schema."""

    status: str = Field(..., description="Overall health status ('healthy' or 'unhealthy')")
    service: str = Field(..., description="Service identifier")
    version: str = Field(..., description="Service version")
    uptime_seconds: float = Field(..., description="Server uptime in seconds")
    timestamp: str = Field(..., description="ISO 8601 server timestamp")
    database: DatabaseHealth = Field(..., description="Database health status detail")
    components: Dict[str, str] = Field(..., description="Subsystem operational readiness map")
