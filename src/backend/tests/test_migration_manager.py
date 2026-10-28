"""Unit tests for Migration Manager (`src/backend/app/core/migration_manager.py`)."""

from src.backend.app.core.migration_manager import (
    check_migration_status,
    find_alembic_ini,
    get_alembic_config,
)


def test_find_alembic_ini_locates_root_file():
    """Verify find_alembic_ini successfully discovers alembic.ini in project root."""
    ini_path = find_alembic_ini()
    assert ini_path is not None
    assert ini_path.name == "alembic.ini"
    assert ini_path.exists()


def test_get_alembic_config_instantiates_valid_config():
    """Verify get_alembic_config constructs an Alembic Config object."""
    cfg = get_alembic_config()
    assert cfg is not None
    assert cfg.config_file_name is not None
    assert "alembic.ini" in cfg.config_file_name


def test_check_migration_status_reports_revisions():
    """Verify check_migration_status returns valid metadata about migration files."""
    status = check_migration_status()
    assert status["alembic_configured"] is True
    assert status["total_versions"] >= 1
    assert "0001_initial_schema" in status["versions"]
    assert status["latest_revision"] == "0001_initial_schema"
