"""SQLAlchemy 2.0 Declarative Models Package (`src.db.models` / `db.models`).

Provides automatic discovery and dynamic importing of all model modules in this package
to ensure `Base.metadata` contains all table schemas when Alembic generates migrations.
"""

import pkgutil
from importlib import import_module
from pathlib import Path

try:
    from src.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
except ImportError:
    from db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

# Auto-discover and import all model modules in this package
_pkg_path = Path(__file__).parent
for _, _module_name, _ in pkgutil.iter_modules([str(_pkg_path)]):
    if not _module_name.startswith("_"):
        try:
            import_module(f"{__name__}.{_module_name}")
        except Exception:
            pass

try:
    from src.db.models.user import User
except ImportError:
    try:
        from db.models.user import User
    except ImportError:
        User = None

__all__ = ["Base", "UUIDPrimaryKeyMixin", "TimestampMixin"]
if User is not None:
    __all__.append("User")
