"""Pydantic v2 schema for system root endpoint response."""

from typing import Dict
from pydantic import BaseModel, Field


class RootResponse(BaseModel):
    """Schema for root endpoint GET / response."""

    name: str = Field(..., description="Application name")
    version: str = Field(..., description="Application version string")
    status: str = Field(..., description="Current system operational status")
    environment: str = Field(..., description="Current execution environment")
    docs_url: str = Field(..., description="Link to Swagger API documentation")
    timestamp: str = Field(..., description="Current server ISO timestamp")
    system_info: Dict[str, str | float] = Field(..., description="System runtime metadata")
