---
name: test_runner_suite
description: "Instructions for running the 5-layer automated testing suite, enforcing the >=80% coverage threshold and zero schema drift policy, parsing tracebacks with parse_traceback.py, generating test_summary.json, and operating the self-healing loop with a 3-iteration circuit breaker."
---

# Automated Test Runner Suite & Self-Healing Skill

Kỹ năng này hướng dẫn `qa-tester` thực thi toàn diện chu trình kiểm thử tự động, thẩm định Zero Schema Drift, đo lường độ phủ Code Coverage, và điều phối vòng lặp tự sửa lỗi (Self-Healing Loop).

---

## 1. Chu Trình Kiểm Thử 5 Tầng Chuẩn Hóa

### Cách 1: Thực thi Tự Động Hóa 1-Chạm (Khuyên dùng)
```bash
python scripts/smoke_test.py
```

### Cách 2: Thực thi Chi Tiết Từng Tầng (Manual Granular Verification)
1. **Tầng 1 - Linting & Code Hygiene**:
   ```bash
   python -m ruff check src/
   ```
2. **Tầng 2 - Cross-Layer Data Contract Validation**:
   ```bash
   python scripts/verify_contracts.py [feature-slug]
   ```
3. **Tầng 3 - Database Migration DAG & Zero Schema Drift**:
   ```bash
   python scripts/verify_migrations.py
   # Thẩm định Zero Schema Drift giữa SQLAlchemy 2.0 Models và Database:
   alembic check
   ```
   *Tiêu chí đạt: Zero Drift (`No new upgrade operations detected`).*
4. **Tầng 4 - Backend & DB Tests kèm Code Coverage**:
   ```bash
   pytest src/backend/tests src/db/tests -v --cov=src/backend/app --cov-report=term-missing
   ```
   *Ngưỡng tối thiểu bắt buộc: Độ phủ Code Coverage đạt $\ge 80\%$.*
5. **Tầng 5 - Client Typecheck**:
   ```bash
   npm --prefix src/frontend run typecheck
   npm --prefix src/mobile run typecheck
   ```

---

## 2. Xuất Bản Kết Quả Máy Đọc Được (`test_summary.json`)

Sau khi chạy chuỗi kiểm thử, `qa-tester` trích xuất và cập nhật kết quả vào file:
`workspaces/artifacts/04_quality/test_summary.json` (hoặc `docs/specs/<feature-slug>/test_summary.json`):

```json
{
  "test_engine": "PyTest Asyncio + pytest-cov Runner & Client Typecheck",
  "timestamp": "2026-10-25T12:00:00Z",
  "backend_tests": {
    "total_test_cases": 15,
    "passed": 15,
    "failed": 0,
    "coverage_percentage": 92.5,
    "coverage_status": "PASSED",
    "threshold_required": 80.0
  },
  "database_migrations": {
    "engine": "Alembic 1.13+",
    "migration_configured": true,
    "schema_drift_check": "ZERO_DRIFT",
    "status": "PASSED"
  },
  "frontend_tests": {
    "typecheck_passed": true,
    "ui_states_handled": true,
    "mock_fixtures_ready": true
  },
  "security_audit": {
    "secret_leaks_found": 0,
    "status": "PASSED"
  }
}
```

---

## 3. Vòng Lặp Sửa Lỗi Tự Động (Self-Healing & Micro-Patcher)

Khi một bài kiểm thử bị thất bại (`FAILED`):

### 1. Bóc tách log lỗi trực tiếp bằng Traceback Patcher:
```bash
python -m pytest src/backend/tests src/db/tests -v | python scripts/parse_traceback.py
```

### 2. Xuất phiếu lỗi Micro-Patch Ticket:
Ghi nhận lỗi vào báo cáo kiểm thử và gửi thông điệp yêu cầu sửa lỗi tới Dev Squad:
```markdown
[SELF-HEALING ACTION REQUIRED]
- Mã Lỗi: BUG-01
- Mức độ: CRITICAL | MAJOR
- Tác tử chịu trách nhiệm: backend-dev (hoặc db-dev / frontend-dev)
- Vị trí phát hiện: src/backend/app/services/user_service.py#L42-L58
- Mã test case thất bại: TC-02 (test_create_user_duplicate_email)
- Đoạn mã lỗi cô lập (5-10 dòng):
  >>  48:  if existing_user:
  >>  49:      raise HTTPException(status_code=400, detail="User already exists")
- Chi tiết lỗi: AssertionError: Expected 409 Conflict, received 400 Bad Request
- Chỉ dẫn Micro-Patch: Chỉ dùng công cụ replace_file_content sửa đúng dòng 49 thành HTTP 409. TUYỆT ĐỐI KHÔNG viết lại toàn bộ file.
```

### 3. Bộ ngắt mạch an toàn (Circuit Breaker):
- Giới hạn tối đa **3 vòng lặp sửa lỗi**.
- Nếu sau 3 lần sửa mà test vẫn fail: Tác tử kích hoạt `[CIRCUIT BREAKER ESCALATION]`, ngừng toàn bộ tiến trình tự động và yêu cầu Tech Lead / User can thiệp.
