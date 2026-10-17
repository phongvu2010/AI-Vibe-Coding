from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.backend.app.api.v1.health import router as health_router
from src.backend.app.api.v1.users import router as users_router
from src.backend.app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
)

# Cấu hình CORS an toàn
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gắn các routers phiên bản API v1
app.include_router(health_router, prefix=settings.API_V1_STR)
app.include_router(users_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": "Welcome to AI-Vibe-Coding API",
        "docs": f"{settings.API_V1_STR}/docs"
    }
