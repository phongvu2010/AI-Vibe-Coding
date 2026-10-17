import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Lớp nền tảng SQLAlchemy Declarative Base"""
    pass

class UUIDPrimaryKeyMixin:
    """Mixin cung cấp khóa chính UUID tự sinh phía Python"""
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

class TimestampMixin:
    """Mixin cung cấp các trường thời gian tự động tạo và cập nhật"""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
