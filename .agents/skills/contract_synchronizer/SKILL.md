---
name: contract_synchronizer
description: "Guidelines and verification rules for synchronizing cross-layer data contracts across Database Models, Backend Pydantic Schemas, and Frontend/Mobile TypeScript interfaces."
---

# Cross-Layer Data Contract Synchronization Skill

Kỹ năng này hướng dẫn `tech-planner`, `qa-tester`, và `code-reviewer` bảo đảm tính nhất quán dữ liệu giữa 3 tầng:

## 1. Ma Trận Ánh Xạ Dữ Liệu Chuẩn (Cross-Layer Data Contract Matrix)
Trong `docs/specs/<feature-slug>/plan.md`, luôn phải có bảng sau:

| Tên trường (`snake_case`) | Kiểu DB (SQLAlchemy) | Kiểu Backend (Pydantic v2) | Kiểu Client (TypeScript) | Ràng buộc / Rỗng |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `UUIDPrimaryKeyMixin` | `uuid.UUID` | `string` | Khóa chính tự sinh |
| `name` | `Mapped[str]` | `str = Field(..., min_length=1)` | `string` | Bắt buộc |
| `metadata_info` | `Mapped[dict] = mapped_column(JSON)` | `dict[str, Any]` | `Record<string, unknown>` | Tùy chọn |
| `created_at` | `Mapped[datetime]` | `datetime` | `string` | Tự động sinh |

## 2. Kiểm Tra Tự Động
- Chạy lệnh: `python scripts/verify_contracts.py <feature-slug>`.
- Nếu phát hiện thuộc tính dùng `camelCase` (ví dụ `userId` thay vì `user_id`), script sẽ báo lỗi và ngăn chặn quá trình chuyển tiếp sang bước review.
