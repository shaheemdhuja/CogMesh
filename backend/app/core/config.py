"""Application configuration management using Pydantic v2 Settings."""

from typing import List, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """CogMesh Distributed Runtime Settings configuration class."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    PROJECT_NAME: str = Field(default="CogMesh Distributed Runtime", description="Application name")
    VERSION: str = Field(default="0.1.0", description="Application version")
    DEBUG: bool = Field(default=True, description="Debug mode flag")
    ENVIRONMENT: str = Field(default="development", description="Runtime environment")
    API_V1_STR: str = Field(default="/api/v1", description="V1 API route prefix")

    HOST: str = Field(default="0.0.0.0", description="Server bind host")
    PORT: int = Field(default=8000, description="Server listen port")

    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./cogmesh.db",
        description="Async SQLAlchemy database connection string",
    )

    LOG_LEVEL: str = Field(default="INFO", description="Logging level (DEBUG, INFO, WARNING, ERROR)")
    LOG_FILE_PATH: str = Field(default="logs/cogmesh.log", description="File path for log storage")
    LOG_RETENTION: str = Field(default="10 days", description="Log file retention duration")
    LOG_ROTATION: str = Field(default="10 MB", description="Log file rotation max size")

    CORS_ORIGINS: Union[List[str], str] = Field(
        default=["*"],
        description="Allowed CORS origins",
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Validate and parse CORS origins into a list of strings."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


settings = Settings()
