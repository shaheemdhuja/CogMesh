"""Application lifecycle events handling startup and shutdown procedures."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from loguru import logger
from app.core.config import settings
from app.core.logging import setup_logging
from app.database.session import check_database_connection, close_database_connection, init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """FastAPI lifespan context manager for application startup and shutdown events."""
    # Startup tasks
    setup_logging()
    logger.info(f"Starting {settings.PROJECT_NAME} (v{settings.VERSION})...")
    logger.info(f"Environment: {settings.ENVIRONMENT} | Debug: {settings.DEBUG}")

    # Initialize database tables
    await init_db()

    # Ping database
    db_connected, response_time_ms = await check_database_connection()
    if db_connected:
        logger.info(f"Database connection verified successfully (ping: {response_time_ms:.2f}ms).")
    else:
        logger.error("Failed to establish database connection during startup!")

    yield

    # Shutdown tasks
    logger.info(f"Shutting down {settings.PROJECT_NAME}...")
    await close_database_connection()
    logger.info("Database engine closed cleanly. Shutdown complete.")
