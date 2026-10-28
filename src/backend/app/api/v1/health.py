from datetime import datetime

from fastapi import APIRouter
from src.backend.app.core.config import settings

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    """Kiểm tra tình trạng hoạt động của hệ thống API"""
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.now().isoformat()
    }
