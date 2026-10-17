---
name: db_sqlalchemy_alembic
description: "Best practices and implementation guidelines for SQLAlchemy 2.0 Async declarative models, Alembic migrations, avoidance of N+1 queries via selectinload, and repository pattern."
---

# SQLAlchemy 2.0 Async & Alembic Engineering Skill

Kỹ năng này hướng dẫn `db-dev` xây dựng tầng dữ liệu chuẩn mực:

## 1. Nguyên Tắc Mô Hình Hóa Dữ Liệu
- Sử dụng cú pháp `Mapped` và `mapped_column` của SQLAlchemy 2.0.
- Luôn kế thừa `Base`, `UUIDPrimaryKeyMixin` và `TimestampMixin` từ `src.db.base`.
- Mọi quan hệ ORM (relationship) phải sử dụng `lazy="selectinload"` hoặc chỉ định `selectinload` trong query để triệt tiêu lỗi N+1 Query.

## 2. Quy Chuẩn Khởi Tạo Migration
- Mỗi lần bổ sung hoặc sửa đổi model, tạo file revision mới tại `src/db/migrations/versions/`.
- Tên file theo định dạng: `<4_so_thu_tu>_<slug_mo_ta>.py` (ví dụ: `0002_add_bookings.py`).
- Cung cấp đầy đủ hàm `upgrade()` và `downgrade()`.
