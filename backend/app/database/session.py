"""SQLAlchemy 2.0 Async Session management and database utilities."""

import time
from typing import AsyncGenerator, Tuple
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from loguru import logger
from app.core.config import settings
from app.database.base import Base

# Construct Async SQLAlchemy 2.0 Engine
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

# Async Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for providing transactional SQLAlchemy async sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as exc:
            await session.rollback()
            logger.error(f"Database session rollback due to exception: {exc}")
            raise
        finally:
            await session.close()


async def check_database_connection() -> Tuple[bool, float]:
    """Execute a lightweight test query ('SELECT 1') against SQLite to check connectivity and measure latency.
    
    Returns:
        Tuple[bool, float]: (is_connected, response_time_in_ms)
    """
    start_time = time.perf_counter()
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            value = result.scalar()
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            if value == 1:
                return True, round(elapsed_ms, 2)
            return False, round(elapsed_ms, 2)
    except Exception as exc:
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        logger.warning(f"Database health check failed: {exc}")
        return False, round(elapsed_ms, 2)


async def init_db() -> None:
    """Initialize database schemas and tables."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database schema initialized successfully.")
    except Exception as exc:
        logger.error(f"Error initializing database schema: {exc}")
        raise


async def close_database_connection() -> None:
    """Dispose of the SQLAlchemy async engine connections gracefully."""
    try:
        await engine.dispose()
        logger.info("Database engine connections disposed successfully.")
    except Exception as exc:
        logger.error(f"Error closing database connection: {exc}")
