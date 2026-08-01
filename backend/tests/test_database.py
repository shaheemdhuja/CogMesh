"""Unit tests for database session and SQLite connection ping."""

import pytest
from sqlalchemy import text
from app.database.session import check_database_connection


@pytest.mark.asyncio
async def test_database_session_execution(db_session):
    """Test raw SQL execution over SQLAlchemy 2.0 AsyncSession."""
    result = await db_session.execute(text("SELECT 42"))
    val = result.scalar()
    assert val == 42


@pytest.mark.asyncio
async def test_check_database_connection():
    """Test check_database_connection utility function."""
    is_connected, latency_ms = await check_database_connection()
    assert is_connected is True
    assert isinstance(latency_ms, float)
    assert latency_ms >= 0.0
