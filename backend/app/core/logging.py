"""Loguru logging setup and standard library logging interceptor."""

import logging
import sys
from pathlib import Path
from loguru import logger
from app.core.config import settings


class InterceptHandler(logging.Handler):
    """Intercept standard logging messages and redirect them to Loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        """Route log record to Loguru logger with corresponding severity level."""
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging() -> None:
    """Configure Loguru logging handlers, sinks, and intercept standard loggers."""
    # Remove existing default loguru sinks
    logger.remove()

    # Ensure log directory exists
    log_file = Path(settings.LOG_FILE_PATH)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Console sink (Colorized stdout/stderr)
    logger.add(
        sys.stderr,
        level=settings.LOG_LEVEL.upper(),
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
        colorize=True,
    )

    # File sink (Rotated & retained logs)
    logger.add(
        str(log_file),
        level=settings.LOG_LEVEL.upper(),
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation=settings.LOG_ROTATION,
        retention=settings.LOG_RETENTION,
        compression="zip",
        enqueue=True,
    )

    # Intercept standard library loggers
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error", "fastapi", "sqlalchemy.engine"):
        mod_logger = logging.getLogger(logger_name)
        mod_logger.handlers = [InterceptHandler()]
        mod_logger.propagate = False

    logger.info(f"Logging initialized. Log level: {settings.LOG_LEVEL}")
