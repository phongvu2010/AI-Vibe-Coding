# AI-Vibe-Coding: Antigravity 2.0 Workspace Guidelines

Chào mừng bạn đến với **AI-Vibe-Coding** — Hệ thống công ty phát triển phần mềm AI toàn diện (AI Software Development Company) vận hành tối ưu trên nền tảng **Antigravity 2.0**.

---

## 🏛️ 1. Nguyên Tắc Vận Hành Cốt Lõi (Core Operating Principles)

1. **Tech Lead Orchestrator**: Main Agent đóng vai trò là **Tech Lead & Tổng Quản Lý Dự Án**. Tech Lead nhận yêu cầu trực tiếp từ Khách hàng / Product Owner (User), lập kế hoạch, kích hoạt các Sub-Teams qua `invoke_subagent`, gửi chỉ thị qua `send_message`, và chỉ trực tiếp chỉnh sửa các tệp cấu hình toàn cục (`pyproject.toml`, `package.json`, `docker-compose.yml`, `Makefile`).
2. **5 Sub-Teams & 15 Subagents Chuyên Trách**: Mọi tác vụ nghiệp vụ, thiết kế, lập trình, kiểm thử và bàn giao đều được ủy quyền cho các Subagents chuyên biệt thuộc 5 Sub-Teams (Discovery, Architecture, Engineering, QA/Review, Release/Delivery).
3. **Phân Vùng Sở Hữu Mã Nguồn (Strict File Partitioning)**:
   - Hồ sơ nghiệp vụ & thiết kế: `docs/specs/<feature-slug>/` (chỉ dành cho `account-lead`, `lead-ba`, `uiux-designer`, `system-architect`, `security-architect`, `tech-planner`).
   - Tầng Dữ liệu: `src/db/` (chỉ dành cho `db-dev`).
   - Tầng Giao diện Web & Mobile: `src/frontend/` và `src/mobile/` (chỉ dành cho `frontend-dev`).
   - Tầng Dịch vụ API: `src/backend/` (chỉ dành cho `backend-dev`).
   - Tài liệu Bàn giao & Kiểm thử: `docs/specs/<feature-slug>/` và `dist/` (chỉ dành cho `qa-tester`, `code-reviewer`, `release-engineer`, `tech-writer`, `handover-lead`).
4. **Đồng Bộ Hợp Đồng Đa Tầng 3 Chiều (Cross-Layer Contract Sync)**:
   - Quy tắc casing: Bắt buộc dùng `snake_case` cho tất cả tên trường dữ liệu từ Database (SQLAlchemy) $\leftrightarrow$ Backend (Pydantic v2) $\leftrightarrow$ Frontend/Mobile (TypeScript Interfaces).
   - Kiểm tra tự động bằng `python scripts/verify_contracts.py <feature-slug>` trước khi sang bước Review.
5. **Vòng Lặp Tự Sửa Lỗi Có Ngắt Mạch (Self-Healing Loop & Circuit Breaker)**:
   - Lỗi kiểm thử và review được cắt tỉa ngắn gọn (15-25 dòng trọng tâm qua `scripts/parse_traceback.py`) để chống phình ngữ cảnh (token context).
   - Tối đa **3 vòng lặp** sửa lỗi. Nếu vượt quá, kích hoạt Circuit Breaker xin ý kiến Tech Lead / User.

---

## 🚦 2. 3 Chốt Chặn Human-in-the-Loop (Quality Gates)

- **Gate 1 - Client Sign-off (`review_gate_1_prd.md`)**: Khách hàng duyệt PRD, User Stories (Gherkin format), Scope và UI Concept trước khi sang pha Kỹ thuật.
- **Gate 2 - Architecture & Contract Sign-off (`review_gate_2_architecture.md`)**: Duyệt thiết kế hệ thống, ERD, API specs (`openapi.yaml`), và Cross-Layer Data Contract Matrix.
- **Gate 3 - Production Readiness Sign-off (`review_gate_3_deploy.md`)**: Đạt 100% kiểm thử 5 tầng (`smoke_test.py`), điểm Code Review $\ge 85/100$, zero lỗ hổng bảo mật nghiêm trọng.

---

## 🧠 3. Định Tuyến Mô Hình AI (Model Cost Routing)

Dự án áp dụng cấu hình `config/model_router.yaml` phân bổ mô hình theo năng lực nhận thức để tiết kiệm 65-80% token:
- **Tier PRO (`pro`)**: Dành cho `lead-ba`, `system-architect`, `security-architect`, `tech-planner`, `code-reviewer`.
- **Tier FLASH (`flash`)**: Dành cho `account-lead`, `uiux-designer`, `qa-tester`, `handover-lead`, `devops-engineer`.
- **Tier FLASH-LITE (`flash_lite`)**: Dành cho `release-engineer`, `tech-writer`.
- **Tier INHERIT (`inherit`)**: Dành cho Dev Squad (`db-dev`, `backend-dev`, `frontend-dev`) theo mô hình của Tech Lead.
