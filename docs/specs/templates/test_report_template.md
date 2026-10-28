# Báo Cáo Kiểm Thử Tự Động (Test Report)

---
feature_slug: "<feature-slug>"
tester: "Automated QA Tester (qa-tester)"
timestamp: "<ISO-8601-Timestamp>"
overall_status: "PASSED | FAILED" # PASSED khi 100% test đạt; FAILED nếu có bất kỳ lỗi nào
circuit_breaker_tripped: false    # true nếu vượt quá 3 lần lặp Self-Healing
---

## 1. Kết Quả Kiểm Thử 5 Tầng (5-Layer Test Results)
| Tầng kiểm thử | Công cụ | Trạng thái | Chi tiết / Độ phủ |
| :--- | :--- | :--- | :--- |
| **Tầng 1: Linter & Syntax** | Ruff & py_compile | `PASSED` | 0 lỗi cú pháp |
| **Tầng 2: Contract Sync** | `verify_contracts.py` | `PASSED` | 100% trường dữ liệu snake_case |
| **Tầng 3: Migration DAG** | `verify_migrations.py` | `PASSED` | Đồ thị Alembic liên tục không đứt gãy |
| **Tầng 4: Pytest Backend & DB**| Pytest Isolated | `PASSED` | 100% test cases passed (Coverage: $\ge 80\%$) |
| **Tầng 5: Client Typecheck** | `tsc --noEmit` | `PASSED` | 0 lỗi typecheck TypeScript |

---

## 2. Số Đo Kiểm Thử Chi Tiết (Test Metrics)
- **Tổng số Test Cases**: `<count>`
- **Số lượng Test PASSED**: `<count>`
- **Số lượng Test FAILED**: `<count>`
- **Thời gian thực thi (Execution Time)**: `<seconds>`s
- **Độ phủ kiểm thử (Code Coverage)**: `<percentage>`% (Ngưỡng yêu cầu: $\ge 80\%$)

---

## 3. Lệnh Tái Hiện Kiểm Thử (Reproduction Command)
```bash
# 1. Chạy toàn bộ Smoke Test 5 tầng 1-click:
python scripts/smoke_test.py

# 2. Chạy cô lập kiểm thử Pytest Backend:
PYTHONPATH=src .venv/bin/pytest src/backend/tests/ -v

# 3. Kiểm tra kiểu dữ liệu Frontend:
npm --prefix src/frontend run typecheck
```

---

## 4. Phiếu Báo Lỗi Chi Tiết (Structured Micro-Patch Tickets — Dành cho Self-Healing)

> 💡 Nếu toàn bộ bài test đều `PASSED`, ghi: *"Không phát hiện lỗi. Hệ thống đạt 100% tiêu chí nghiệm thu kiểm thử."*
> ⚠️ **Quy chuẩn Micro-Patch**: Trích xuất đúng 5-10 dòng code ngữ cảnh và bắt buộc Dev Squad CHỈ dùng công cụ `replace_file_content` để sửa đúng dòng phát sinh lỗi, tuyệt đối không viết lại toàn bộ file.

### [BUG-01] `<Tiêu đề lỗi ngắn gọn>`
- **Mã Lỗi**: `BUG-01`
- **Mức độ (Severity)**: `CRITICAL` | `MAJOR` | `MINOR`
- **Tác tử Chịu trách nhiệm (Target Agent)**: `db-dev` (`src/db/`) | `backend-dev` (`src/backend/`) | `frontend-dev` (`src/frontend/`)
- **Vị trí Phát hiện (Target File & Line Range)**: `src/.../file.py#L42-L55`
- **Mã Kịch bản Thất bại (Failed Test ID)**: `TC-01` (`test_function_name`)
- **Đoạn Mã Lỗi Cô Lập (Context Snippet — 5-10 Dòng có đánh dấu `>>`)**:
  ```python
  >>  48:  if existing_user:
  >>  49:      raise HTTPException(status_code=400, detail="User already exists")
  ```
- **Nhật ký Lỗi Rút Gọn (Diagnostics qua parse_traceback.py)**:
  ```text
  AssertionError: assert res.status_code == 409, received 400
  ```
- **Phân tích Nguyên nhân Gốc (Root Cause Analysis)**:
  - Trả về status code 400 thay vì 409 Conflict theo chuẩn REST API khi duplicate resource.
- **Chỉ Dẫn Micro-Patch**:
  - Yêu cầu Dev Squad CHỈ DÙNG CÔNG CỤ `replace_file_content` sửa đúng dòng vi phạm trong line range đã định vị. TUYỆT ĐỐI KHÔNG viết lại toàn bộ file.
- **Các bước Tái hiện (Reproduction Command)**:
  ```bash
  PYTHONPATH=src .venv/bin/pytest src/backend/tests/test_file.py -k "test_function_name"
  ```
- **Trạng thái Xử lý (Status)**: `OPEN` # OPEN | IN_PROGRESS | RESOLVED | RE-TESTED

---

## 5. Nhật Ký Vòng Lặp Tự Sửa Lỗi (Self-Healing Loop Log)
- **Vòng lặp hiện tại**: `1/3`
- **Hành động điều phối của Tech Lead**: Đã điều hướng ticket `BUG-01` đến `backend-dev` kèm chỉ dẫn micro-patch cô lập.
- **Trạng thái Circuit Breaker**: `NORMAL` (Chưa vượt ngưỡng ngắt mạch 3 lần).
