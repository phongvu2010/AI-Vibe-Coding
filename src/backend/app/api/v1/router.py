"""API v1 Router aggregator (`src/backend/app/api/v1/router.py`).

Central router mounting all feature-specific sub-routers for API v1.
Backend developers register feature endpoints here.
"""

from fastapi import APIRouter
from src.backend.app.api.v1.health import router as health_router
from src.backend.app.api.v1.users import router as users_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(users_router, tags=["Users"])
