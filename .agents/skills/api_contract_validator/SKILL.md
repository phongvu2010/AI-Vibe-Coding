---
name: api_contract_validator
description: "Thẩm định cú pháp, tính đầy đủ và tính nhất quán của đặc tả OpenAPI 3.0+ (YAML/JSON) trước khi ký duyệt Quality Gate 2."
---

# API Contract Validator Skill (OpenAPI 3.0+ Linter)

## 🎯 Mục Đích
Đảm bảo bản hợp đồng giao tiếp giữa Frontend và Backend (`docs/specs/openapi.json` hoặc `openapi.yaml`) không có lỗi logic, đầy đủ mã phản hồi HTTP, schema kiểu dữ liệu và sẵn sàng cho việc sinh TypeScript interfaces.

## 🔍 Bộ Quy Tắc Thẩm Định (Validation Rules)

### 1. Chuẩn Cú Pháp OpenAPI 3.0+
- Phiên bản khai báo rõ ràng (`openapi: "3.0.3"` hoặc `openapi: "3.1.0"`).
- Phải có đầy đủ các khối: `info`, `paths`, `components/schemas`.
- Không có broken references (`$ref`) trỏ tới schema không tồn tại.

### 2. Chuẩn Đặt Tên RESTful (RESTful Naming Conventions)
- **Đường dẫn danh từ số nhiều:** 
  - ✅ `/api/v1/users`, `/api/v1/orders/{order_id}`
  - ❌ `/api/v1/getUser`, `/api/v1/updateOrder`
- **Casing đồng nhất:** Tất cả query parameters và body properties phải dùng `snake_case` (ví dụ: `page_size`, `created_at`, `user_id`).

### 3. Bộ Mã Phản Hồi HTTP Tiêu Chuẩn (HTTP Status Codes)
Mọi endpoint RESTful phải khai báo tường minh cả Happy path và Error schemas:
- `200 OK` (hoặc `201 Created` cho POST).
- `400 Bad Request` cho dữ liệu đầu vào không hợp lệ.
- `401 Unauthorized` cho endpoint cần đăng nhập nhưng thiếu token.
- `403 Forbidden` khi người dùng không đủ quyền RBAC.
- `404 Not Found` cho tài nguyên không tồn tại.
- `422 Unprocessable Entity` cho validation lỗi chi tiết của Pydantic v2.
- `500 Internal Server Error` với error response schema chuẩn `{"detail": "..."}`.

### 4. Rào Chắn Bảo Mật (Security Schemes)
- Các endpoint nhạy cảm (User Profile, Admin, Payment, CRUD) phải có `security: - bearerAuth: []`.
- Khối `components.securitySchemes` phải định nghĩa rõ:
  ```yaml
  components:
    securitySchemes:
      bearerAuth:
        type: http
        scheme: bearer
        bearerFormat: JWT
  ```

### 5. Lệnh Kiểm Tra Nhanh
```bash
python scripts/generate_openapi.py
python scripts/verify_contracts.py
```
Mọi sai lệch kiểu dữ liệu hoặc thiếu trường giữa OpenAPI và Database Model phải được phát hiện và sửa chữa trước khi qua Gate 2.
