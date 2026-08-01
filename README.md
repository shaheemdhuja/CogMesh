# CogMesh: Distributed Runtime Project

CogMesh is a distributed runtime system.

## Sprint 1: Runtime Foundation

Sprint 1 establishes the production-quality runtime foundation:
- **FastAPI Core**: Async web application with lifecycle management.
- **Async Database Layer**: SQLAlchemy 2.0 with SQLite (`aiosqlite`) and database ping check.
- **Loguru Logging**: Unified log management with file rotation and colorized console sinks.
- **Endpoints**: `GET /` (Runtime metadata) and `GET /health` (Database connectivity & health status).
- **WebSocket Manager Foundation**: Connection management and broadcast capabilities.
- **Testing**: Complete `pytest` suite with `httpx` async testing client.
- **Database Migrations**: Alembic migration setup.

## Project Structure

```
backend/
├── app/
│   ├── api/          # Route handlers & versioning
│   ├── core/         # Settings, logging, lifecycle events
│   ├── database/     # SQLAlchemy 2.0 async engine, sessions, base
│   ├── models/       # Abstract base models
│   ├── schemas/      # Pydantic v2 schemas
│   ├── services/     # Business logic & health checks
│   ├── websocket/    # Connection manager foundation
│   ├── utils/        # System info & metrics utilities
│   └── main.py       # FastAPI application entrypoint
├── alembic/          # Database migration environment
├── tests/            # Automated async test suite
├── .env              # Development environment variables
├── requirements.txt  # Project dependencies
└── README.md         # Detailed backend guide
```

For detailed backend documentation and execution instructions, see [`backend/README.md`](file:///d:/CogMesh/backend/README.md).
