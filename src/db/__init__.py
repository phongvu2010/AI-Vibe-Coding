"""Database package (`db`) for SQLAlchemy 2.0 models, session, and repositories."""

try:
    from src.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
    from src.db.session import AsyncSessionLocal, engine, get_db, get_db_session
except ImportError:
    from db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
    from db.session import AsyncSessionLocal, engine, get_db, get_db_session

__all__ = [
    "AsyncSessionLocal",
    "Base",
    "TimestampMixin",
    "UUIDPrimaryKeyMixin",
    "engine",
    "get_db",
    "get_db_session",
]
