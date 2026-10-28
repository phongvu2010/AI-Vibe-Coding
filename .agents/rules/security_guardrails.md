# Rào Chắn An Toàn & Bảo Mật (Security Guardrails)

Tất cả các Subagents và mã nguồn phải tuân thủ tuyệt đối các quy định an ninh sau:

---

## 1. Zero Hardcoded Secrets (Không lưu cứng bí mật)
- TUYỆT ĐỐI KHÔNG commit API keys, mật khẩu database, secret keys JWT, hoặc tokens vào mã nguồn.
- Mọi bí mật cấu hình phải nạp qua biến môi trường thông qua `pydantic-settings` (Backend) hoặc `process.env` (Frontend).
- File `.env.example` cung cấp giá trị mẫu an toàn, file `.env` thực tế nằm trong `.gitignore`.

---

## 2. Phòng Chống Lỗ Hổng OWASP Top 10
- **SQL Injection**: Tuyệt đối không nối chuỗi câu lệnh SQL thô (`raw SQL string concatenation`). Luôn sử dụng SQLAlchemy parameterized queries hoặc ORM expressions.
- **Cross-Site Scripting (XSS)**: Không render trực tiếp chuỗi HTML chưa qua khử trùng (sanitization). Sử dụng React / Next.js auto-escaping mặc định.
- **Broken Authentication & Session Management**:
  - Mật khẩu phải được băm bằng bcrypt hoặc Argon2.
  - JWT Tokens phải có thời hạn hết hạn (`exp`) rõ ràng.
- **Broken Object Level Authorization (BOLA / IDOR)**:
  - Mọi thao tác cập nhật, xem hoặc xóa tài nguyên phải kiểm tra xem người dùng hiện tại có quyền sở hữu tài nguyên đó không (`WHERE user_id = current_user.id`).

---

## 3. Rào Chắn Thực Thi Dòng Lệnh Theo Vai Trò (Role-based CLI Guardrails)

Nhằm đảm bảo tính cô lập và toàn vẹn của hệ thống, mọi tác tử phải tuân thủ nghiêm ngặt ma trận phân quyền thực thi lệnh:

### 3.1. Whitelist phân quyền theo từng vai trò:
| Vai trò / Subagent | Quyền hạn công cụ & Dòng lệnh được phép thực thi | Phạm vi cấm thực thi |
| :--- | :--- | :--- |
| **`account-lead`, `lead-ba`, `uiux-designer`** | • Sử dụng `ask_question` để phỏng vấn/làm rõ với User.<br/>• Đọc/ghi tài liệu trong `docs/specs/<slug>/`. | • TUYỆT ĐỐI KHÔNG chạy bất kỳ lệnh bash/shell nào.<br/>• Không can thiệp mã nguồn trong `src/`. |
| **`system-architect`, `security-architect`, `tech-planner`** | • Đọc/ghi tài liệu trong `docs/specs/<slug>/`.<br/>• Đọc cấu trúc mã nguồn `src/` để lập kế hoạch. | • Không chạy lệnh build, deploy hoặc chỉnh sửa code. |
| **`db-dev`** | • Chạy linter: `ruff check src/db/`.<br/>• Kiểm tra cú pháp: `python -m py_compile src/db/...`.<br/>• Migrations: `alembic check`, `alembic revision --autogenerate`, `alembic upgrade head`.<br/>• Seeds: `python src/db/seeds/runner.py`. | • Cấm sửa code ngoài `src/db/`.<br/>• Cấm xóa database runtime mà không có cờ test. |
| **`backend-dev`** | • Chạy linter: `ruff check src/backend/`.<br/>• Kiểm tra cú pháp: `python -m py_compile src/backend/...`.<br/>• Chạy test backend cô lập: `pytest src/backend/tests -v`. | • Cấm sửa code ngoài `src/backend/`.<br/>• Cấm gọi `pip install` trực tiếp không thông qua Tech Lead. |
| **`frontend-dev`** | • Kiểm tra kiểu: `npm --prefix src/frontend run typecheck`.<br/>• Linter & Build: `npm --prefix src/frontend run lint`, `npm --prefix src/frontend run build`.<br/>• Typecheck mobile: `npm --prefix src/mobile run typecheck`. | • Cấm sửa code ngoài `src/frontend/` và `src/mobile/`.<br/>• Cấm import remote external fonts gây gọi mạng ngoài trong sandbox. |
| **`qa-tester`** | • Chạy suite kiểm thử: `python scripts/smoke_test.py`, `pytest`, `python scripts/verify_contracts.py`.<br/>• Phân tích traceback lỗi: `python scripts/parse_traceback.py`. | • Cấm sửa trực tiếp logic nghiệp vụ trong `src/` (chỉ xuất bản báo cáo lỗi `test-report.md`). |
| **`code-reviewer`** | • Chỉ thực thi các lệnh đọc git diff: `git status --short`, `git diff --stat`, `git diff -- src/ docs/ ':!*package-lock.json' ':!*.lock'`. | • Cấm chạy lệnh ghi file mã nguồn hoặc commit. |
| **`devops-engineer`, `release-engineer`** | • Đóng gói: `python scripts/bundle_release.py`.<br/>• Docker lint & config: `docker compose config`. | • Cấm chạy `docker system prune -a` hoặc xóa images không liên quan. |
| **`Tech Lead (Main Agent)`** | • Độc quyền quản lý subagents qua `invoke_subagent`, `manage_subagents`.<br/>• Độc quyền cập nhật file manifest gốc (`pyproject.toml`, `package.json`, `docker-compose.yml`).<br/>• Độc quyền thực thi `git add`, `git commit`. | • Tuân thủ các quy tắc bảo vệ nhánh và an toàn dữ liệu. |

### 3.2. Blacklist tuyệt đối (Cấm toàn bộ Subagents):
1. **Lệnh phá hủy hệ thống**: Cấm `rm -rf` ngoài thư mục tạm `tmp/`, cấm `git reset --hard`, `git clean -fdx`, `git checkout .`, `git push --force`.
2. **Tự ý sửa đổi cấu hình dự án**: Cấm Subagents tự ý sửa đổi file cấu hình gốc (`pyproject.toml`, `alembic.ini`, `docker-compose.yml`, `package.json`). Khi cần bổ sung thư viện mới, Subagent BẮT BUỘC chỉ cắm cờ `[DEPENDENCY REQUIRED]` để Tech Lead phê duyệt.
3. **Thực thi lệnh không an toàn**: Cấm chạy `pip install` hoặc `npm install` tùy tiện trong môi trường sandbox; cấm gọi `python`, `pytest`, `ruff` trần không trỏ qua `.venv/`.
4. **Vi phạm biên giới phân vùng (Boundary Violation)**: Tác tử của từng layer không được phép ghi đè file của layer khác (Backend không sửa Frontend, Frontend không sửa DB).
