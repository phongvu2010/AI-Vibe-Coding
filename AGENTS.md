# AI-Vibe-Coding: Điều Phối Toàn Cục & Cẩm Nang Tác Tử (AGENTS.md)

Tài liệu này là chỉ dẫn tối cao cho **Tech Lead (Main Agent)** và hệ sinh thái **15 Subagents thuộc 5 Sub-Teams** vận hành công ty phát triển phần mềm AI trên nền tảng **Antigravity 2.0**.

---

## 🏛️ 1. Cơ Cấu Tổ Chức 5 Sub-Teams (15 Subagents)

```text
[Khách Hàng / Product Owner]
              │ (Yêu cầu thô / RFP / Feature Request)
              ▼
┌────────────────────────────────────────────────────────────────────────┐
│ SUB-TEAM 1: PRODUCT DISCOVERY & SOLUTIONS SQUAD                        │
│ • account-lead    : Tiếp nhận yêu cầu, bóc tách Scope & T-Shirt sizing │
│ • lead-ba         : Phỏng vấn (ask_question), Gherkin stories, PRD.md   │
│ • uiux-designer   : Luồng màn hình (Mermaid), Design Tokens, 5 UI states│
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ [QUALITY GATE 1: Client Sign-off]
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ SUB-TEAM 2: ARCHITECTURE & SYSTEM PLANNING SQUAD                       │
│ • system-architect: Kiến trúc tổng thể, mô hình ERD, C4 diagrams       │
│ • security-architect: STRIDE threat model, RBAC/ABAC, OWASP Guardrails │
│ • tech-planner    : plan.md, Data Contract Matrix, openapi.yaml, DAG   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ [QUALITY GATE 2: Architecture Sign-off]
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ SUB-TEAM 3: CORE ENGINEERING SQUAD (2-Wave Execution)                  │
│ [Wave 1: Song song]                                                    │
│ • db-dev          : SQLAlchemy 2.0 Models, Alembic, Repos, Async Seeds │
│ • frontend-dev    : Web Next.js 15 / Vite + Mobile Expo, UI 5-States   │
│ [Wave 2: Nối mạng & Triển khai]                                        │
│ • backend-dev     : Pydantic v2 schemas, FastAPI routes kết nối DB     │
│ • devops-engineer : Dockerfile, docker-compose, CI/CD, startup scripts │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ SUB-TEAM 4: QUALITY ASSURANCE & SECURITY SQUAD                         │
│ • qa-tester       : 5-Layer Smoke Test, Pytest, Contract & Migrations  │
│ • code-reviewer   : Token-optimized Git Diff Audit, Scorecard, OWASP   │
│ [Feedback Loop]   : Tự động gửi traceback (parse_traceback.py, max 3x) │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ [QUALITY GATE 3: Production Readiness]
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ SUB-TEAM 5: RELEASE, DOCUMENTATION & HANDOVER SQUAD                    │
│ • release-engineer: Build check, Git Conventional Commit, Release .zip │
│ • tech-writer     : USER_MANUAL.md, API_GUIDE.md, DEPLOYMENT.md        │
│ • handover-lead   : UAT_CHECKLIST.md, Hướng dẫn 1-click cho Khách hàng │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 2. Ma Trận Trách Nhiệm & Rào Chắn Lệnh (RACI Matrix & Guardrails)

| Subagent ID | Tên vai trò | Thư mục sở hữu (Ownership) | Lệnh được phép (Whitelist) | Lệnh cấm tuyệt đối (Blacklist) | Model Tier |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tech Lead** | Main Agent (Orchestrator) | Toàn bộ dự án | `invoke_subagent`, `send_message`, `manage_subagents`, cập nhật `pyproject.toml`, `package.json`, `docker-compose.yml`, `git commit` | `git reset --hard`, `git push --force` | `inherit` |
| **`account-lead`** | Client Liaison Lead | `docs/specs/<slug>/` | `view_file`, `write_to_file`, `replace_file_content` | Cấm chạy shell commands, cấm sửa code | `flash` |
| **`lead-ba`** | Principal BA | `docs/specs/<slug>/` | `ask_question`, `view_file`, `write_to_file`, `replace_file_content` | Cấm chạy shell commands, cấm sửa code | `pro` |
| **`uiux-designer`** | UI/UX Designer | `docs/specs/<slug>/` | `view_file`, `write_to_file`, `replace_file_content` | Cấm chạy shell commands, cấm sửa code | `flash` |
| **`system-architect`**| System Architect | `docs/specs/<slug>/` | `view_file`, `write_to_file`, `replace_file_content` | Cấm chạy shell commands, cấm sửa code | `pro` |
| **`security-architect`**| Security Specialist | `docs/specs/<slug>/` | `view_file`, `write_to_file`, `replace_file_content` | Cấm chạy shell commands, cấm sửa code | `pro` |
| **`tech-planner`** | Technical Planner | `docs/specs/<slug>/` | `view_file`, `write_to_file`, `replace_file_content` | Cấm chạy shell commands, cấm sửa code | `pro` |
| **`db-dev`** | Database Specialist | `src/db/` | `python -m ruff check src/db/`, `python -m py_compile src/db/...`, `alembic` | Cấm `rm -rf`, cấm sửa `pyproject.toml`, cấm ghi file ngoài `src/db/` | `inherit` |
| **`frontend-dev`** | Frontend & Mobile Dev | `src/frontend/`, `src/mobile/` | `npm --prefix src/frontend run typecheck`, `run lint`, `run build`, `npm --prefix src/mobile run typecheck` | Cấm `npm install` trần, cấm sửa `package.json`, cấm ghi file ngoài frontend/mobile | `inherit` |
| **`backend-dev`** | Backend Specialist | `src/backend/` | `python -m ruff check src/backend/`, `python -m py_compile src/backend/...` | Cấm `pip install` trần, cấm sửa `pyproject.toml`, cấm ghi ngoài `src/backend/` | `inherit` |
| **`devops-engineer`** | DevOps & Cloud | `docker-compose.yml`, `scripts/` | `docker compose config`, `docker build` | Cấm xóa volume dữ liệu, cấm push cloud credentials | `flash` |
| **`qa-tester`** | Automated QA Tester | `docs/specs/`, `tests/` | `python scripts/smoke_test.py`, `python scripts/verify_contracts.py`, `python scripts/verify_migrations.py`, `pytest`, `npm run typecheck` | Cấm tự ý sửa đổi mã nguồn nghiệp vụ `src/` | `flash` |
| **`code-reviewer`** | Principal Reviewer | `docs/specs/` | `git status --short`, `git diff --stat`, `git diff -- src/ docs/` | Cấm sửa code, cấm tạo git commit | `pro` |
| **`release-engineer`**| Release Engineer | `dist/`, `scripts/` | `python scripts/bundle_release.py`, `git tag` | Cấm sửa code nghiệp vụ | `flash_lite`|
| **`tech-writer`** | Technical Writer | `docs/specs/`, `docs/company/` | `view_file`, `write_to_file`, `replace_file_content` | Cấm sửa code, cấm chạy lệnh shell | `flash_lite`|
| **`handover-lead`** | Client Handover Lead | `docs/specs/<slug>/` | `view_file`, `write_to_file`, `replace_file_content` | Cấm sửa code, cấm chạy lệnh shell | `flash` |

---

## 🔄 3. Giao Thức Điều Phối Giữa Tech Lead & Subagents (Dispatch Protocol)

1. **Khởi động Subagent**: Tech Lead sử dụng `invoke_subagent` truyền `TypeName` (ví dụ: `lead-ba`), `Role`, và `Prompt` mục tiêu rõ ràng kèm đường dẫn tài liệu.
2. **Theo dõi Tiến độ**: Antigravity 2.0 tự động kích hoạt resume khi subagent hoàn thành, Tech Lead KHÔNG polling lặp.
3. **Phản hồi Lỗi & Tự Sửa (Self-Healing Dispatch)**:
   - Khi QA hoặc Code Review phát hiện lỗi, Tech Lead sử dụng mẫu tin:
     ```markdown
     [SELF-HEALING ACTION REQUIRED]
     Lỗi phát hiện tại: <file-path>:<line>
     Tóm tắt lỗi (Đã cắt tỉa):
     <15-25 lines traceback>
     Yêu cầu: Khắc phục lỗi và phản hồi [FIX-COMPLETED] kèm danh sách file đã sửa.
     ```
4. **Dọn dẹp Tài nguyên (Subagent Lifecycle Cleanup)**:
   - Khi một Phase hoặc Feature kết thúc, Tech Lead chủ động gọi `manage_subagents(Action="kill_all")` để giải phóng bộ nhớ và giữ workspace luôn sạch sẽ.
