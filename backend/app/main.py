"""CogMesh FastAPI Application Entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.api.v1.endpoints import health, root
from app.core.config import settings
from app.core.events import lifespan


def create_application() -> FastAPI:
    """Application factory for instantiating FastAPI runtime with middleware, handlers, and routers."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=(
            "CogMesh Distributed Runtime Foundation API. "
            "Provides runtime lifecycle management, database connectivity, and health monitoring."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Configure CORS Middleware
    if settings.CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Mount root level endpoints required by Sprint 1 specification
    app.include_router(root.router, tags=["System Root"])
    app.include_router(health.router, tags=["Health Assessment"])

    # Mount versioned API routes under prefix /api/v1
    app.include_router(api_router)

    return app


app = create_application()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
