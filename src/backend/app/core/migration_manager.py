"""Database Migration Manager with Self-Healing (`src/backend/app/core/migration_manager.py`).

Provides runtime schema migration management, health checks, and self-healing
recovery when tables already exist or revisions drift (e.g. stamp head).
Part of AI-Vibe-Coding (Antigravity 2.0).
"""

import logging
from pathlib import Path
from typing import Any

from alembic import command
from alembic.config import Config

logger = logging.getLogger(__name__)


def find_alembic_ini() -> Path | None:
    """Locate alembic.ini by traversing parent directories upward."""
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        ini = parent / "alembic.ini"
        if ini.exists():
            return ini
    return None


def get_alembic_config(database_url: str | None = None) -> Config | None:
    """Create Alembic Config instance configured with the appropriate database URL."""
    ini_path = find_alembic_ini()
    if not ini_path:
        logger.warning("alembic.ini not found in project hierarchy.")
        return None

    cfg = Config(str(ini_path))
    if database_url:
        cfg.set_main_option("sqlalchemy.url", database_url)
    return cfg


def run_migrations(database_url: str | None = None) -> bool:
    """Tự động đồng bộ schema cơ sở dữ liệu qua Alembic Migrations kèm cơ chế tự phục hồi (Self-Healing)."""
    cfg = get_alembic_config(database_url)
    if not cfg:
        return False

    try:
        command.upgrade(cfg, "head")
        logger.info("Database migrations applied successfully to 'head'.")
        return True
    except Exception as e:
        error_msg = str(e).lower()
        # Nếu bảng đã tồn tại sẵn (schema đã đồng bộ trước đó), tự động stamp head để sửa lỗi lệch revision
        if "already exists" in error_msg or ("table" in error_msg and "exists" in error_msg):
            logger.warning("Table already exists in database. Attempting automatic self-healing via 'stamp head'...")
            try:
                command.stamp(cfg, "head")
                logger.info("Successfully self-healed database schema by stamping revision to 'head'.")
                return True
            except Exception as stamp_err:
                logger.error(f"Failed to self-heal migration via stamp head: {stamp_err}")
                return False
        else:
            logger.warning(f"Could not apply migrations automatically: {e}")
            return False


def stamp_head(database_url: str | None = None) -> bool:
    """Đánh dấu cơ sở dữ liệu đã ở revision mới nhất (head) khi đã tạo bảng trước đó."""
    cfg = get_alembic_config(database_url)
    if not cfg:
        return False
    try:
        command.stamp(cfg, "head")
        logger.info("Database migration successfully stamped to 'head'.")
        return True
    except Exception as e:
        logger.error(f"Failed to stamp head: {e}")
        return False


def check_migration_status() -> dict[str, Any]:
    """Kiểm tra tính hợp lệ và danh sách migration revisions hiện có trên đĩa."""
    ini_path = find_alembic_ini()
    if not ini_path:
        return {
            "alembic_configured": False,
            "total_versions": 0,
            "versions": [],
            "latest_revision": None,
        }

    versions_dir = ini_path.parent / "src" / "db" / "migrations" / "versions"
    rev_files = [f for f in versions_dir.glob("*.py") if f.name != "__init__.py"] if versions_dir.exists() else []
    sorted_revs = sorted([f.stem for f in rev_files])
    latest = sorted_revs[-1] if sorted_revs else None

    return {
        "alembic_configured": True,
        "ini_path": str(ini_path),
        "total_versions": len(rev_files),
        "versions": sorted_revs,
        "latest_revision": latest,
    }
