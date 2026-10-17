# Quy Chuẩn Lập Trình Dự Án (Coding Standards)

Mọi dòng mã được sinh ra trong workspace này phải tuân thủ nghiêm ngặt các quy tắc sau:

---

## 1. Phân Tầng Clean Architecture (Backend)
- Phân tầng nghiêm ngặt từ dưới lên:
  - `src/db/models/`: Định nghĩa thực thể dữ liệu với SQLAlchemy 2.0 (Declarative Mapped), khóa chính UUID, timestamp `created_at` / `updated_at`.
  - `src/db/repositories/`: Thao tác dữ liệu async, độc lập với web framework.
  - `src/backend/app/schemas/`: Pydantic v2 schemas phục vụ validation request/response, bắt buộc dùng `snake_case`.
  - `src/backend/app/services/`: Logic nghiệp vụ thuần túy, không phụ thuộc trực tiếp vào HTTP Request/Response.
  - `src/backend/app/api/v1/`: FastAPI routers nhận request, gọi service, trả response.

---

## 2. Quy Chuẩn Đồng Bộ Hợp Đồng (Contract Synchronization)
- Toàn bộ tên thuộc tính (fields) phải dùng chuẩn `snake_case` trên cả 3 tầng:
  - Database Column: `user_id`, `created_at`, `phone_number`.
  - Pydantic Schema: `user_id: uuid.UUID`, `created_at: datetime`, `phone_number: str`.
  - TypeScript Interface: `user_id: string; created_at: string; phone_number: string;`.
- Nghiêm cấm việc tầng này dùng `snake_case`, tầng khác tự ý đổi sang `camelCase` khi không có serializer mapping rõ ràng.

---

## 3. Quy Chuẩn Frontend & Mobile (UI States)
- Mọi component hiển thị dữ liệu bất đồng bộ phải xử lý đủ 5 trạng thái giao diện:
  1. `default`: Trạng thái ban đầu trước khi tương tác.
  2. `loading`: Hiển thị Skeleton hoặc Spinner khi đang fetch API.
  3. `empty`: Hiển thị Empty State thân thiện khi dữ liệu trả về rỗng (`[]`).
  4. `error`: Hiển thị thông báo lỗi rõ ràng kèm nút thử lại (Retry button).
  5. `success`: Hiển thị dữ liệu chính xác khi request thành công.
- Tuyệt đối không dùng hardcoded colors, luôn dùng Tailwind CSS theme tokens.
- Nghiêm cấm nạp font từ xa (remote fonts) gây chậm trễ rendering.

---

## 4. Quy Chuẩn Kiểm Thử & Linter
- Python: Bắt buộc vượt qua `ruff check src/` với 0 warnings/errors.
- TypeScript: Bắt buộc vượt qua `tsc --noEmit` không có lỗi type.
- Mọi API endpoint mới phải có ít nhất 1 test case Happy Path và 1 test case Unhappy Path (Validation Error / Not Found).
