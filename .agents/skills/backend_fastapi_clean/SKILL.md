---
name: backend_fastapi_clean
description: "Guidelines for Clean Architecture with FastAPI, Pydantic v2 validation (strict snake_case), separation of services and routers, and standardized HTTP error responses."
---

# FastAPI Clean Architecture & Pydantic v2 Engineering Skill

Kỹ năng này hướng dẫn `backend-dev` xây dựng dịch vụ API phân tầng:

## 1. Phân Tách Trách Nhiệm (Separation of Concerns)
- **Schemas (`app/schemas/`)**: Pydantic v2 validation, bắt buộc dùng `snake_case`. Tách biệt `Create`, `Update`, `Response`.
- **Services (`app/services/`)**: Xử lý toàn bộ logic nghiệp vụ, giao tiếp với repositories. Bắt lỗi và ném `HTTPException` với thông điệp rõ ràng.
- **Routers (`app/api/v1/`)**: Controllers mỏng nhận request, gọi service, trả response với HTTP Status code phù hợp (200, 201, 204, 400, 404).

## 2. Chuẩn Hóa Lỗi HTTP
- Mọi phản hồi lỗi phải có cấu trúc: `{"detail": "Mô tả lỗi rõ ràng"}` để Client dễ dàng phân tích và hiển thị cho người dùng.
