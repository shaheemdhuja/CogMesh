"""Integration tests for GET / and GET /health endpoints."""

import pytest


@pytest.mark.asyncio
async def test_get_root(client):
    """Test GET / root endpoint response."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "CogMesh Distributed Runtime"
    assert data["status"] == "running"
    assert "version" in data
    assert "system_info" in data


@pytest.mark.asyncio
async def test_get_health(client):
    """Test GET /health health status endpoint response with SQLite connectivity check."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "CogMesh Distributed Runtime"
    assert data["database"]["status"] == "connected"
    assert data["database"]["engine"] == "SQLite (aiosqlite)"
    assert data["database"]["latency_ms"] is not None
    assert "components" in data


@pytest.mark.asyncio
async def test_v1_health(client):
    """Test GET /api/v1/health mounted endpoint."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
