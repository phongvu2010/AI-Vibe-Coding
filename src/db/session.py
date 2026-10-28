import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/vibe_db"
)

# Chuyển đổi cờ phù hợp cho SQLite và Supavisor / PgBouncer
connect_args = {}
if "sqlite" in DATABASE_URL:
    connect_args["check_same_thread"] = False

# Supavisor / PgBouncer Transaction Pooler (e.g. Supabase port 6543) does not support
# session-level prepared statements. Disable statement cache in asyncpg if connecting to pooler.
if (
    ":6543" in DATABASE_URL
    or "pooler.supabase.com" in DATABASE_URL
    or os.getenv("DB_DISABLE_STATEMENT_CACHE", "false").lower() == "true"
):
    connect_args["prepared_statement_cache_size"] = 0
    connect_args["statement_cache_size"] = 0

engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("SQL_ECHO", "false").lower() == "true",
    pool_pre_ping=True,
    connect_args=connect_args,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency cung cấp session kết nối cơ sở dữ liệu async"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Alias for compatibility across all subagent conventions
get_db_session = get_db

