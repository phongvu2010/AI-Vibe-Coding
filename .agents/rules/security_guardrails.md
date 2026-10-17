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

## 3. Rào Chắn Thực Thi Dòng Lệnh (CLI Execution Guardrails)
- Các tác tử tài liệu (`lead-ba`, `tech-planner`, `uiux-designer`, `tech-writer`, `handover-lead`): TUYỆT ĐỐI KHÔNG chạy lệnh terminal làm thay đổi hệ thống.
- Các tác tử dev (`db-dev`, `frontend-dev`, `backend-dev`): Chỉ chạy các lệnh kiểm tra cú pháp và linter trong thư mục sở hữu.
- Nghiêm cấm chạy các lệnh phá hoại: `rm -rf /`, `drop database`, `git reset --hard`, `git push --force`.
