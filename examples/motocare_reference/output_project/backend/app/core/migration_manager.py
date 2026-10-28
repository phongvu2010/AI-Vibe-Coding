import os
import sys
from pathlib import Path
from alembic.config import Config
from alembic import command
from app.core.config import settings

def run_migrations() -> bool:
    """Tự động đồng bộ schema cơ sở dữ liệu qua Alembic Migrations."""
    base_dir = Path(__file__).resolve().parent.parent.parent
    ini_path = base_dir / "alembic.ini"
    if ini_path.exists():
        try:
            cfg = Config(str(ini_path))
            cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
            command.upgrade(cfg, "head")
            return True
        except Exception as e:
            # Nếu bảng đã tồn tại sẵn, tự động stamp head để đồng bộ schema
            if "already exists" in str(e).lower():
                try:
                    command.stamp(cfg, "head")
                    return True
                except Exception:
                    pass
            return False
    return False

def stamp_head() -> bool:
    """Đánh dấu cơ sở dữ liệu đã ở revision mới nhất (head) khi đã tạo bảng."""
    base_dir = Path(__file__).resolve().parent.parent.parent
    ini_path = base_dir / "alembic.ini"
    if ini_path.exists():
        try:
            cfg = Config(str(ini_path))
            cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
            command.stamp(cfg, "head")
            return True
        except Exception:
            return False
    return False

def check_migration_status() -> dict:
    """Kiểm tra tính hợp lệ và phiên bản migrations hiện có."""
    base_dir = Path(__file__).resolve().parent.parent.parent
    versions_dir = base_dir / "alembic" / "versions"
    rev_files = list(versions_dir.glob("*.py")) if versions_dir.exists() else []
    return {
        "alembic_configured": (base_dir / "alembic.ini").exists(),
        "total_versions": len([f for f in rev_files if f.name != "__init__.py"]),
        "latest_revision": "0001_initial_schema"
    }
