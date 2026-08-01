# CogMesh Backend - Sprint 1 Foundation

Production-grade distributed runtime foundation built with Python 3.12, FastAPI, SQLAlchemy 2.0, SQLite (aiosqlite), Loguru, Pydantic v2, and Alembic.

## 🚀 Overview

Sprint 1 establishes the foundational architecture for the CogMesh distributed runtime:
- **FastAPI Core**: Async ASGI web framework with OpenAPI Swagger UI at `/docs`.
- **SQLAlchemy 2.0 Async Engine**: Connected to SQLite via `aiosqlite` with auto-ping connection health check (`SELECT 1`).
- **Loguru Logging**: Structured logging intercepting standard Python loggers with colorized console output and file rotation (`logs/cogmesh.log`).
- **Lifespan Management**: Graceful startup event (DB connection test & initialization) and shutdown event (engine disposal).
- **WebSocket Manager Foundation**: Connection tracking and broadcasting manager for future node-to-node streaming.
- **Alembic Migrations**: Async database migration environment pre-configured.

---

## 📁 File Structure & Architectural Purpose

| Directory / File | Description & Purpose |
| :--- | :--- |
| `app/main.py` | Application entry point and factory function `create_application()`. Configures FastAPI instance, CORS, lifespan, Swagger metadata, and mounts routers. |
| `app/core/config.py` | Type-safe configuration management using Pydantic v2 `BaseSettings` reading environment variables from `.env`. |
| `app/core/logging.py` | Loguru logging interceptor and setup. Intercepts standard loggers (`uvicorn`, `fastapi`, `sqlalchemy`) and outputs to stderr & rotating files. |
| `app/core/events.py` | Lifespan context manager (`@asynccontextmanager`) managing application startup tasks (DB verification, schema creation) and shutdown tasks. |
| `app/database/base.py` | SQLAlchemy 2.0 `DeclarativeBase` baseline class. |
| `app/database/session.py` | Async engine creation (`sqlite+aiosqlite:///./cogmesh.db`), `async_sessionmaker`, `get_db` route dependency, `check_database_connection()` ping utility (`SELECT 1`), and engine cleanup. |
| `app/database/init_db.py` | Database table schema creation runner. |
| `app/models/base.py` | Abstract `BaseModel` class providing primary key `id`, timezone-aware `created_at`, `updated_at` columns, and `to_dict()` helper. |
| `app/models/__init__.py` | Model export registry. |
| `app/schemas/health.py` | Pydantic v2 schemas (`DatabaseHealth`, `HealthResponse`) for `/health` endpoint payload validation. |
| `app/schemas/system.py` | Pydantic v2 schema (`RootResponse`) for `/` endpoint response payload validation. |
| `app/schemas/__init__.py` | Schema export registry. |
| `app/services/health_service.py` | Service layer encapsulating SQLite ping execution, latency calculation, uptime tracking, and overall system health aggregation. |
| `app/services/__init__.py` | Service export registry. |
| `app/websocket/manager.py` | Production-ready `ConnectionManager` class for managing active socket clients, disconnects, unicast messages, and broadcasts. |
| `app/websocket/__init__.py` | WebSocket manager export registry. |
| `app/utils/sys_info.py` | Uptime calculation and platform/system runtime metadata generator. |
| `app/utils/__init__.py` | Utility export registry. |
| `app/api/v1/endpoints/root.py` | Handler for `GET /` returning system version, status, environment, and docs link. |
| `app/api/v1/endpoints/health.py` | Handler for `GET /health` executing DB ping tests and returning component status. |
| `app/api/v1/router.py` | Aggregator for API V1 endpoints with Swagger tags. |
| `app/api/router.py` | Main API router prefixing V1 routes under `/api/v1`. |
| `alembic.ini` | Configuration file for Alembic database migrations. |
| `alembic/env.py` | Async migration environment runner utilizing `aiosqlite` and `AsyncEngine`. |
| `alembic/script.py.mako` | Migration script template. |
| `alembic/versions/0001_initial_schema.py` | Initial migration script. |
| `tests/conftest.py` | Pytest setup containing in-memory SQLite database fixtures and `httpx.AsyncClient`. |
| `tests/test_config.py` | Unit tests for Pydantic v2 configuration parser. |
| `tests/test_database.py` | Unit tests for async database session and `SELECT 1` ping query. |
| `tests/test_health.py` | Integration tests for `GET /` and `GET /health` endpoints. |
| `.env` | Environment configuration file. |
| `.env.example` | Template for environment variable settings. |
| `requirements.txt` | Explicit Python dependency requirements file with version pins. |

---

## 🛠️ Setup & Local Execution

### 1. Prerequisites
Ensure Python **3.12+** is installed on your system.

### 2. Create Virtual Environment
```bash
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Migrations
Run Alembic database migrations:
```bash
alembic upgrade head
```

### 5. Start Application Server
Run the FastAPI development server with Uvicorn:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🧪 Running Automated Tests

Run the complete pytest suite:
```bash
pytest -v
```

---

## 📑 API Endpoints & Swagger Documentation

Once the server is running, interactive API documentation is available at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Core Endpoints:
- `GET /` : Node metadata and system information.
- `GET /health` : Database connection test (`SELECT 1`) and system health assessment.
- `GET /api/v1/health` : Mounted API v1 health check.
