"""Unit tests for configuration loader and settings."""

from app.core.config import settings, Settings


def test_default_settings_values():
    """Verify default values loaded into application settings."""
    assert settings.PROJECT_NAME == "CogMesh Distributed Runtime"
    assert settings.VERSION == "0.1.0"
    assert settings.API_V1_STR == "/api/v1"
    assert settings.PORT == 8000


def test_cors_origins_parsing():
    """Test string to list parsing of CORS origins."""
    test_settings = Settings(CORS_ORIGINS="http://localhost:3000, http://127.0.0.1:8000")
    assert test_settings.CORS_ORIGINS == ["http://localhost:3000", "http://127.0.0.1:8000"]
