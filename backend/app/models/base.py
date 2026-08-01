"""Abstract base model with standard timestamp and primary key fields."""

from datetime import datetime, timezone
from typing import Any, Dict
from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base


def utc_now() -> datetime:
    """Return timezone-aware current UTC datetime."""
    return datetime.now(timezone.utc)


class BaseModel(Base):
    """Abstract base model providing common fields for future CogMesh models."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert ORM model instance into dictionary format."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
