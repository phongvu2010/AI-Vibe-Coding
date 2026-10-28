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

## 2. Quy Chuẩn Đồng Bộ Hợp Đồng (Contract Synchronization & Uniform Casing)
- Toàn bộ tên thuộc tính (fields) phải dùng chuẩn `snake_case` trên cả 3 tầng (Database, Backend API, Frontend & Mobile TS):
  - Database Column: `user_id`, `created_at`, `phone_number`.
  - Pydantic Schema: `user_id: uuid.UUID`, `created_at: datetime`, `phone_number: str`.
  - TypeScript Interface: `user_id: string; created_at: string; phone_number: string;`.
- Nghiêm cấm việc tầng này dùng `snake_case`, tầng khác tự ý đổi sang `camelCase` khi không có serializer mapping rõ ràng (loại trừ triệt để lỗi `undefined` tại runtime).
- **Quy Chuẩn 4 Kiểu Dữ Liệu Bắt Buộc (Cross-Layer Data Types)**:
  - **UUID**: DB dùng `Uuid(as_uuid=True)` (Python `default=uuid.uuid4`), Backend dùng `UUID` / `str`, Frontend TS dùng `string` (chuẩn RFC 4122).
  - **Timestamps**: DB dùng `DateTime(timezone=True)`, Backend dùng `datetime` (UTC), Frontend TS dùng `string` (định dạng ISO 8601 có đuôi `Z`, ví dụ `2026-10-02T12:00:00Z`).
  - **Mảng dữ liệu**: DB dùng `JSON` (mặc định `default=list`), Backend dùng `list[T]`, Frontend TS dùng `T[]`.
  - **Enums**: Backend dùng Python `StrEnum`, Frontend TS dùng `string literal union type` (ví dụ: `'PENDING' | 'CONFIRMED' | 'CANCELLED'`).
- **Strict Typing**: Tuyệt đối không dùng kiểu `any` trong TypeScript; khai báo interfaces rõ ràng tại `types/`.

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

---

## 5. Quy Chuẩn Cơ Sở Dữ Liệu & Supabase (Transaction Pooler vs Session Mode DDL)
- **DATABASE_URL (Port 6543)**: Sử dụng cho ứng dụng FastAPI runtime kết nối qua Supavisor Transaction Pooler (`port 6543`, `ssl=require`, `prepared_statement_cache_size=0`). Đã được cấu hình tự động trong `src/db/session.py`.
- **DIRECT_DATABASE_URL (Port 5432)**: BẮT BUỘC dùng cho Alembic DDL migrations kết nối qua Session Mode hoặc Direct (`port 5432`, `ssl=require`) do Transaction Pooler không hỗ trợ prepared statements và session-level locks khi thực thi migration DDL.
- Khóa chính luôn sinh bằng UUID (`default=uuid.uuid4` hoặc kế thừa `UUIDPrimaryKeyMixin`) để đảm bảo tính toàn vẹn tuyệt đối trên cả SQLite test và PostgreSQL production.

---

## 6. Kiểm Thử Cross-DB & Tính Năng PostgreSQL Nâng Cao
- Khi sử dụng các tính năng độc quyền của PostgreSQL (`pgvector`, `tsvector` Full-Text Search, PostgreSQL native `ENUM`, `ARRAY`, `JSONB` path operators):
  - Luôn cung cấp kiểu tương thích qua `.with_variant(...)` khi khả thi.
  - Đánh dấu test case bằng marker `@pytest.mark.postgres_only` trong thư mục tests.
  - Môi trường SQLite async in-memory tự động skip an toàn các test `postgres_only` với lý do rõ ràng mà không làm vỡ test suite tổng thể.
  - Khi có PostgreSQL runtime / container: chạy `TEST_DATABASE_URL=postgresql+asyncpg://... make test` để kiểm thử trực tiếp trên PostgreSQL engine.

---

## 7. Quy Chuẩn Git Commits & Quản Lý File Môi Trường (Git Standards & Environment Discipline)
- **Conventional Commits**: Mọi commit phải tuân thủ chuẩn Conventional Commits thống nhất:
  - `feat:` Tính năng mới hoàn chỉnh.
  - `fix:` Sửa lỗi / bản vá defect ticket.
  - `docs:` Thêm hoặc cập nhật tài liệu specs, PRD, architecture, user manual.
  - `style:` Định dạng code, dấu cách, linter styling (không đổi logic).
  - `refactor:` Tái cấu trúc mã nguồn (không đổi tính năng bên ngoài).
  - `test:` Bổ sung hoặc chỉnh sửa unit test, e2e test, fixtures.
  - `chore:` Cập nhật cấu hình build, dependencies, tooling, script bảo trì.
- **Atomic Changes**: Mỗi commit hoặc pull request chỉ giải quyết chính xác **một sub-task** được định nghĩa trong DAG backlog (`task_backlog_dag.json`), tuyệt đối không gom nhiều task độc lập vào một commit để bảo đảm khả năng rollback an toàn.
- **Quản lý Môi trường & Bí Mật**: Tất cả thông tin nhạy cảm, thông số kết nối và bí mật phải nằm trong `.env`. Nghiêm cấm commit file `.env` vào Git; bắt buộc luôn cập nhật đồng bộ cấu hình mẫu tại `.env.example`.
