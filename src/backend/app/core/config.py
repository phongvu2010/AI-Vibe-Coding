"""Application Configuration & Environment Settings (Pydantic v2 Settings)."""

import json
import os

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Core Application Settings loaded from environment variables or .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # General Project Info
    PROJECT_NAME: str = "AI-Vibe-Coding Backend API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev_secret_key_vibe_coding_antigravity_2026")

    # API Prefix (hỗ trợ cả API_V1_STR và API_V1_PREFIX)
    API_V1_STR: str = os.getenv("API_V1_STR", os.getenv("API_V1_PREFIX", "/api/v1"))
    LOG_LEVEL: str = "INFO"

    @property
    def API_V1_PREFIX(self) -> str:
        """Bí danh tương thích ngược từ AI-Team-Dev."""
        return self.API_V1_STR

    # Database URLs
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/vibe_db"
    TEST_DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"

    # CORS Origins (accepts JSON array string or comma-separated string)
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://localhost:8081",  # Expo Metro bundler
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str]:
        """Parse comma-separated string or preserve list of origins."""
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        elif isinstance(v, list):
            return v
        return [v]


settings = Settings()
