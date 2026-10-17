---
name: test_runner_suite
description: "Instructions for running the 5-layer automated testing suite, parsing tracebacks with parse_traceback.py, and operating the self-healing loop with a 3-iteration circuit breaker."
---

# Automated Test Runner Suite & Self-Healing Skill

Kỹ năng này hướng dẫn `qa-tester` thực thi chu trình kiểm thử và điều phối vòng lặp tự sửa lỗi:

## 1. Chu Trình Kiểm Thử 5 Tầng
Thực thi lệnh 1-chạm:
```bash
python scripts/smoke_test.py
```
Quy trình sẽ tự động chạy:
1. `python -m ruff check src/`
2. `python scripts/verify_contracts.py`
3. `python scripts/verify_migrations.py`
4. `pytest src/backend/tests src/db/tests`
5. `npm --prefix src/frontend run typecheck`

## 2. Xử Lý Khi Có Lỗi (Self-Healing Protocol)
Khi một tầng kiểm thử thất bại:
1. **Cắt tỉa log lỗi**:
   ```bash
   python scripts/parse_traceback.py <log_file>
   ```
2. **Gửi thông điệp có cấu trúc cho Dev Squad**:
   ```markdown
   [SELF-HEALING ACTION REQUIRED]
   Lỗi phát hiện tại: src/backend/app/services/auth_service.py:45
   Tóm tắt lỗi (Đã cắt tỉa):
   E   AssertionError: Expected status 200, got 401
   Yêu cầu: Khắc phục lỗi và phản hồi [FIX-COMPLETED]
   ```
3. **Bộ ngắt mạch (Circuit Breaker)**:
   - Theo dõi số lần lặp lại sửa lỗi.
   - Nếu đã qua 3 lần lặp mà vẫn fail: NGỪNG TOÀN BỘ TIẾN TRÌNH, báo cáo Tech Lead / User can thiệp.
