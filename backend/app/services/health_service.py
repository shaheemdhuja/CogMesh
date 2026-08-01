"""Service encapsulating health check logic and database ping testing."""

from datetime import datetime, timezone
from app.core.config import settings
from app.database.session import check_database_connection
from app.schemas.health import DatabaseHealth, HealthResponse
from app.utils.sys_info import get_uptime_seconds


class HealthService:
    """Service providing operational health assessments for CogMesh."""

    @staticmethod
    async def get_health_status() -> HealthResponse:
        """Perform system checks including SQLite connectivity test and aggregate status.
        
        Returns:
            HealthResponse: Detailed health response schema.
        """
        db_ok, latency_ms = await check_database_connection()

        db_status_str = "connected" if db_ok else "disconnected"
        overall_status = "healthy" if db_ok else "unhealthy"

        database_health = DatabaseHealth(
            status=db_status_str,
            latency_ms=latency_ms if db_ok else None,
            engine="SQLite (aiosqlite)",
        )

        components = {
            "api_router": "operational",
            "database_session": "operational" if db_ok else "degraded",
            "websocket_manager": "operational",
            "event_loop": "operational",
        }

        return HealthResponse(
            status=overall_status,
            service=settings.PROJECT_NAME,
            version=settings.VERSION,
            uptime_seconds=get_uptime_seconds(),
            timestamp=datetime.now(timezone.utc).isoformat(),
            database=database_health,
            components=components,
        )
