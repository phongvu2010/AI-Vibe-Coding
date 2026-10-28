"""FastAPI Application Entrypoint (`src/backend/app/main.py`)."""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from backend.app.api.v1.health import router as health_router
    from backend.app.api.v1.router import api_router
    from backend.app.core.config import settings
    from backend.app.core.migration_manager import run_migrations
except ImportError:
    from src.backend.app.api.v1.health import router as health_router
    from src.backend.app.api.v1.router import api_router
    from src.backend.app.core.config import settings
    from src.backend.app.core.migration_manager import run_migrations

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager for startup and shutdown events."""
    # Tự động đồng bộ schema và self-healing database migrations nếu AUTO_MIGRATE được bật
    auto_migrate = os.getenv("AUTO_MIGRATE", "false").lower() in ("true", "1", "yes")
    if auto_migrate:
        logger.info("AUTO_MIGRATE is enabled. Running database migrations...")
        try:
            run_migrations()
        except Exception as e:
            logger.warning(f"Database migration check encountered an issue: {e}")
    yield


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        description="Backend API built on Antigravity 2.0 AI-Vibe-Coding Architecture",
        lifespan=lifespan,
    )

    # Cấu hình CORS an toàn (chuẩn hóa loại bỏ trailing slashes)
    if settings.CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin).rstrip("/") for origin in settings.CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Expose /health at root level for Docker/Orchestrator healthcheck
    app.include_router(health_router)

    # Gắn toàn bộ router tập trung phiên bản API v1
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/")
    async def root():
        return {
            "message": "Welcome to AI-Vibe-Coding API",
            "docs": f"{settings.API_V1_STR}/docs",
            "status": "healthy",
            "version": settings.VERSION,
        }

    return app


app = create_app()
