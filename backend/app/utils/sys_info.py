"""System information and uptime tracking utilities."""

import platform
import sys
import time
from datetime import datetime, timezone

# Record application start timestamp
START_TIME = time.time()
START_DATETIME = datetime.now(timezone.utc)


def get_uptime_seconds() -> float:
    """Calculate process uptime in seconds."""
    return round(time.time() - START_TIME, 2)


def get_system_metadata() -> dict:
    """Retrieve system, platform, and python environment runtime details."""
    return {
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "architecture": platform.machine(),
        "start_time": START_DATETIME.isoformat(),
        "uptime_seconds": get_uptime_seconds(),
    }
