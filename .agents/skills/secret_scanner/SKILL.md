---
name: secret_scanner
description: "Instructions for scanning codebase for hardcoded secrets, private keys, API tokens, and passwords before release."
---

# Secret Scanner & Security Audit Skill

Kỹ năng này hướng dẫn `security-architect` và `code-reviewer` rà soát mã nguồn nhằm bảo đảm **Zero Hardcoded Secrets**:

## 1. Các Mẫu Bí Mật Cần Quét (Patterns)
- JWT Secrets: `secret_key\s*=\s*['\"][a-zA-Z0-9_\-]{16,}['\"]`
- API Keys: `(api_key|apikey|bearer)\s*=\s*['\"][a-zA-Z0-9_\-]{20,}['\"]`
- Passwords: `password\s*=\s*['\"][^'\"]+['\"]` (ngoại trừ test fixtures cô lập)
- Database URLs có thông tin đăng nhập: `postgres://.*:.*@`

## 2. Quy Tắc Khắc Phục
- Toàn bộ giá trị cấu hình nhạy cảm phải nạp qua `pydantic-settings` (Backend) hoặc biến môi trường `process.env` (Frontend).
- File `.env.example` chỉ chứa giá trị placeholder (ví dụ: `SECRET_KEY=change_this_in_production`).
