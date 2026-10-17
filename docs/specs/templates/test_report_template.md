# Báo Cáo Kiểm Thử Tự Động (Test Report)

---
feature_slug: "<feature-slug>"
tester: "Automated QA Tester (qa-tester)"
timestamp: "<ISO-8601-Timestamp>"
overall_status: "PASSED | FAILED"
---

## 1. Kết Quả Kiểm Thử 5 Tầng (5-Layer Test Results)
| Tầng kiểm thử | Công cụ | Trạng thái | Ghi chú |
| :--- | :--- | :--- | :--- |
| **Tầng 1: Linter & Syntax** | Ruff & py_compile | `PASSED` | 0 lỗi linter |
| **Tầng 2: Contract Sync** | `verify_contracts.py` | `PASSED` | 100% trường dữ liệu snake_case |
| **Tầng 3: Migration DAG** | `verify_migrations.py` | `PASSED` | Đồ thị Alembic liên tục không đứt gãy |
| **Tầng 4: Pytest Backend & DB**| Pytest Isolated | `PASSED` | 100% test cases passed |
| **Tầng 5: Client Typecheck** | `tsc --noEmit` | `PASSED` | 0 lỗi typecheck |

## 2. Chi Tiết Lỗi & Nhật Ký Self-Healing (Nếu có)
- Số lần lặp lại: `<0-3>`
- Trạng thái Circuit Breaker: `NORMAL | TRIPPED`
- Traceback cắt tỉa trọng tâm:
```text
<Không có lỗi>
```
