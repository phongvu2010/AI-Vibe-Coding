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

### 1.1. Ba Chế Độ Vận Hành Đa Cấp Độ (Tri-Tier Execution Architecture)
Hệ thống cho phép Tech Lead linh hoạt lựa chọn 1 trong 3 chế độ vận hành tùy theo quy mô tác vụ:
1. **Chế độ Enterprise 5 Sub-Teams (15 Agents)**: Áp dụng cho toàn bộ dự án mới hoặc phân hệ lớn của khách hàng, vận hành đầy đủ 5 Sub-Teams và 3 Chốt chặn HITL Gates (Gate 1 PRD $\rightarrow$ Gate 2 Architecture $\rightarrow$ Gate 3 Production Readiness).
2. **Chế độ Lean Matrix 7 Tác Tử (Kế thừa từ `AI-Team-Dev`)**: Dành cho tính năng quy mô vừa (thêm 1 bảng DB / 1 API module / 1 luồng giao diện). Tech Lead điều phối trực tiếp với 7 subagent cốt lõi (`ba`, `planner`, `db-dev`, `frontend-dev`, `backend-dev`, `qa-tester`, `code-reviewer`) thao tác trực tiếp trên `src/`, bỏ qua thủ tục họp 3 HITL Gates, tiết kiệm token tối đa.
3. **Chế độ Tactical Fast-Track Squad**: Dành cho micro-tasks, bugfix, thêm field hoặc sửa style giao diện. Kích hoạt `@fast-track-squad` qua `make task TASK="..."` với cơ chế impact analysis, snapshot an toàn và auto-commit.

### 1.2. Cơ Chế Phân Định Hai Không Gian Thực Thi (Target Workspace Dual Mode)
Để triệt tiêu tuyệt đối sự nhầm lẫn về nơi đọc/ghi mã nguồn của các tác tử, hệ thống phân định rạch ròi 2 không gian làm việc:
1. **Chế độ In-Place Development (`src/`) — Mặc định**:
   - Áp dụng khi phát triển, mở rộng tính năng mới hoặc bảo trì ứng dụng full-stack có sẵn trong repo.
   - Thư mục làm việc: `src/db/`, `src/backend/`, `src/frontend/`, `src/mobile/`.
   - Toàn bộ subagents dev và QA thao tác trực tiếp trên cây thư mục `src/`.
2. **Chế độ Greenfield Autonomous Generation (`workspaces/output_project/`)**:
   - Áp dụng khi người dùng cung cấp một Client Brief độc lập hoàn toàn mới và chạy chu trình tự động hóa qua CLI (`make dev PROJECT=... FILE=...` hoặc `python scripts/runner.py`).
   - Kết quả mã nguồn và tài liệu phát sinh được cô lập hoàn toàn trong `workspaces/output_project/` và `workspaces/artifacts/`, không làm ảnh hưởng đến mã nguồn khung tại `src/`.
   - Có thể dọn dẹp hoặc sao lưu độc lập qua `make clean-project` và `make backup`.

---

## 📋 2. Ma Trận Trách Nhiệm & Rào Chắn Lệnh (RACI Matrix & Guardrails)

| Subagent ID | Tên vai trò | Thư mục sở hữu (Ownership) | Lệnh được phép (Whitelist) | Lệnh cấm tuyệt đối (Blacklist) | Model Tier |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tech Lead** | Main Agent (Orchestrator) | Toàn bộ dự án | `invoke_subagent`, `send_message`, `manage_subagents`, cập nhật `pyproject.toml`, `package.json`, `docker-compose.yml`, `git commit` | `git reset --hard`, `git push --force` | `inherit` |
| **`account-lead`** | Client Liaison Lead | `docs/specs/<slug>/` | `view_file`, `write_to_file`, `replace_file_content` | Cấm chạy shell commands, cấm sửa code | `flash` |
| **`lead-ba`** (`@ba`) | Principal BA | `docs/specs/<slug>/` | `ask_question`, `view_file`, `write_to_file`, `replace_file_content` | Cấm chạy shell commands, cấm sửa code | `pro` |
| **`uiux-designer`** | UI/UX Designer | `docs/specs/<slug>/` | `view_file`, `write_to_file`, `replace_file_content` | Cấm chạy shell commands, cấm sửa code | `flash` |
| **`system-architect`**| System Architect | `docs/specs/<slug>/` | `view_file`, `write_to_file`, `replace_file_content` | Cấm chạy shell commands, cấm sửa code | `pro` |
| **`security-architect`**| Security Specialist | `docs/specs/<slug>/` | `view_file`, `write_to_file`, `replace_file_content` | Cấm chạy shell commands, cấm sửa code | `pro` |
| **`tech-planner`** (`@planner`)| Technical Planner | `docs/specs/<slug>/` | `view_file`, `write_to_file`, `replace_file_content` | Cấm chạy shell commands, cấm sửa code | `pro` |
| **`db-dev`** | Database Specialist | `src/db/` | `python -m ruff check src/db/`, `python -m py_compile src/db/...`, `alembic` | Cấm `rm -rf`, cấm sửa `pyproject.toml`, cấm ghi file ngoài `src/db/` | `inherit` |
| **`frontend-dev`** | Frontend & Mobile Dev | `src/frontend/`, `src/mobile/` | `npm --prefix src/frontend run typecheck`, `run lint`, `run build`, `npm --prefix src/mobile run typecheck`, `python scripts/setup_frontend.py` | Cấm `npm install` trần, cấm sửa `package.json`, cấm ghi file ngoài frontend/mobile | `inherit` |
| **`backend-dev`** | Backend Specialist | `src/backend/` | `python -m ruff check src/backend/`, `python -m py_compile src/backend/...` | Cấm `pip install` trần, cấm sửa `pyproject.toml`, cấm ghi ngoài `src/backend/` | `inherit` |
| **`devops-engineer`** | DevOps & Cloud | `docker-compose.yml`, `scripts/` | `docker compose config`, `docker build` | Cấm xóa volume dữ liệu, cấm push cloud credentials | `flash` |
| **`qa-tester`** | Automated QA Tester | `docs/specs/`, `tests/` | `python scripts/smoke_test.py`, `python scripts/verify_contracts.py`, `python scripts/verify_migrations.py`, `pytest`, `npm run typecheck` | Cấm tự ý sửa đổi mã nguồn nghiệp vụ `src/` | `flash` |
| **`code-reviewer`** | Principal Reviewer | `docs/specs/` | `git status --short`, `git diff --stat`, `git diff -- src/ docs/` | Cấm sửa code, cấm tạo git commit | `pro` |
| **`release-engineer`**| Release Engineer | `dist/`, `scripts/` | `python scripts/bundle_release.py`, `git tag` | Cấm sửa code nghiệp vụ | `flash_lite`|
| **`tech-writer`** | Technical Writer | `docs/specs/`, `docs/company/` | `view_file`, `write_to_file`, `replace_file_content` | Cấm sửa code, cấm chạy lệnh shell | `flash_lite`|
| **`handover-lead`** | Client Handover Lead | `docs/specs/<slug>/` | `view_file`, `write_to_file`, `replace_file_content` | Cấm sửa code, cấm chạy lệnh shell | `flash` |
| **`fast-track-squad`** | Tactical Agile Squad | `src/` | `python scripts/verify_contracts.py`, `pytest`, `npm run typecheck`, sửa code trong `src/` | Cấm xóa volume dữ liệu, cấm `git reset --hard` | `flash` |

### 2.1. Rào Chắn Thực Thi Dòng Lệnh Phân Quyền (Role-Based Command Whitelist)

> [!IMPORTANT]
> **Quy Chuẩn Đường Dẫn Môi Trường Ảo (Virtualenv Binary Resolution)**:
> Khi thực thi lệnh shell trong Antigravity Sandbox, subagents **BẮT BUỘC** ưu tiên gọi Python qua đường dẫn môi trường ảo `.venv` để tránh trỏ nhầm vào Python toàn cục của hệ thống (gây lỗi `ModuleNotFoundError` do thiếu packages):
> - **Windows**: `.\.venv\Scripts\python.exe -m <module>` (hoặc `.\.venv\Scripts\pytest.exe`, `.\.venv\Scripts\ruff.exe`)
> - **macOS / Linux / POSIX**: `.venv/bin/python -m <module>` (hoặc `.venv/bin/pytest`, `.venv/bin/ruff`)
> - **Bộ công cụ tự động đa nền tảng**: Khuyên dùng các runner tự nhận diện môi trường: `python scripts/smoke_test.py`, `.\run.ps1 <cmd>` hoặc `make <target>`.

Mỗi tác tử chỉ được phép thực thi các lệnh trong danh mục whitelist tương ứng:
- **`lead-ba` / `ba` & `tech-planner` / `planner` & `account-lead` & `uiux-designer` & `system-architect` & `security-architect`**:
  - Chỉ sử dụng công cụ phỏng vấn (`ask_question`) và công cụ đọc/ghi file: `view_file`, `write_to_file`, `replace_file_content`.
  - **Tuyệt đối KHÔNG chạy shell commands** làm biến đổi môi trường hoặc mã nguồn.
- **`db-dev`** (Chỉ thao tác trong `src/db/`):
  - *Windows*: `.\.venv\Scripts\python.exe -m ruff check src/db/`, `.\.venv\Scripts\python.exe -m py_compile src/db/...`, `.\.venv\Scripts\python.exe scripts/verify_migrations.py`, `.\.venv\Scripts\python.exe src/db/seeds/runner.py`, `.\.venv\Scripts\alembic.exe ...`
  - *macOS / Linux*: `.venv/bin/python -m ruff check src/db/`, `.venv/bin/python -m py_compile src/db/...`, `.venv/bin/python scripts/verify_migrations.py`, `.venv/bin/python src/db/seeds/runner.py`, `.venv/bin/alembic ...`
- **`backend-dev`** (Chỉ thao tác trong `src/backend/`):
  - *Windows*: `.\.venv\Scripts\python.exe -m ruff check src/backend/`, `.\.venv\Scripts\python.exe -m py_compile src/backend/...`
  - *macOS / Linux*: `.venv/bin/python -m ruff check src/backend/`, `.venv/bin/python -m py_compile src/backend/...`
- **`frontend-dev`** (Chỉ thao tác trong `src/frontend/` và `src/mobile/`):
  - `npm --prefix src/frontend run typecheck`, `npm --prefix src/frontend run lint`, `npm --prefix src/frontend run build`
  - `npm --prefix src/mobile run typecheck`, `npm --prefix src/mobile run lint`
- **`qa-tester`** (Kiểm tra toàn diện):
  - *Universal 1-Click*: `python scripts/smoke_test.py`
  - *Windows*: `.\.venv\Scripts\python.exe scripts/verify_contracts.py <slug>`, `.\.venv\Scripts\python.exe scripts/verify_migrations.py`, `.\.venv\Scripts\pytest.exe src/backend/tests src/db/tests -v`, `npm --prefix src/frontend run typecheck`
  - *macOS / Linux*: `.venv/bin/python scripts/verify_contracts.py <slug>`, `.venv/bin/python scripts/verify_migrations.py`, `.venv/bin/pytest src/backend/tests src/db/tests -v`, `npm --prefix src/frontend run typecheck`
- **`code-reviewer`** (Chỉ thẩm định read-only):
  - `git status --short`, `git diff --stat`, `git diff -- src/ docs/ ':!*package-lock.json' ':!*.lock' ':!*.min.*'`, `git diff`
- **`tech-lead`** (Orchestrator):
  - Khởi chạy các công cụ tự động hóa: `python scripts/smoke_test.py`, `python scripts/checkpoint.py`, `python scripts/run_headless_sdlc.py`, `python scripts/bundle_release.py`.
  - Cập nhật các file manifest gốc (`pyproject.toml`, `docker-compose.yml`, `alembic.ini`, `package.json`) khi nhận cờ `[DEPENDENCY REQUIRED]`.
  - Quản lý vòng đời subagent qua `manage_subagents(Action="kill"|"kill_all")`.

### 2.2. Danh Mục Lệnh Cấm Tuyệt Đối (Strict Command Blacklist)
Mọi tác tử (kể cả Orchestrator) **tuyệt đối không được phép thực thi** các lệnh sau:
- 🚫 **Lệnh phá hủy dữ liệu/lịch sử Git**: `rm -rf` ngoài thư mục tạm, `git reset --hard`, `git clean -fdx`, `git checkout .`, `git push --force`.
- 🚫 **Lệnh xóa DB trực tiếp**: `dropdb`, `DROP DATABASE`, `rm -rf src/db/migrations/versions/*`.
- 🚫 **Lệnh/Thao tác sửa File Cấu hình Gốc (Root Configuration Protection)**: Các subagents dev/qa/ba **TUYỆT ĐỐI KHÔNG ĐƯỢC PHÉP TRỰC TIẾP CHỈNH SỬA** các file cấu hình gốc: `pyproject.toml`, `docker-compose.yml`, `alembic.ini`, `src/frontend/package.json`, `src/mobile/package.json`. Nếu cần thêm thư viện, phải gửi yêu cầu leo thang `[DEPENDENCY REQUIRED]` để duy nhất Tech Lead Orchestrator phê duyệt và chỉnh sửa, triệt tiêu race condition trong `Workspace: "inherit"`.
- 🚫 **Lệnh cài đặt gói tự do (Unpinned Package Installation)**: Cấm chạy `pip install <package>` hoặc `npm install <package>` trực tiếp trong shell.
- 🚫 **Lệnh import font ngoại trú trong Sandbox**: Không dùng `next/font/google` fetch online gây nghẽn timeout; luôn dùng system fonts hoặc Tailwind CSS classes để build offline 100%.
- 🚫 **Lệnh vi phạm phân vùng file (Path Boundary Violation)**: Subagent không bao giờ được phép sửa đổi hoặc xóa file nằm ngoài thư mục quyền sở hữu của mình (`src/db/` cho db-dev, `src/backend/` cho backend-dev, `src/frontend/` và `src/mobile/` cho frontend-dev).

### 2.3. Quy Chuẩn Cơ Sở Dữ Liệu, Supabase & Cross-DB Testing
- **Kiến Trúc Supabase Runtime vs Migration**:
  - `DATABASE_URL`: Dùng cho ứng dụng FastAPI runtime kết nối qua Supavisor Transaction Pooler (`port 6543`, `ssl=require`, `prepared_statement_cache_size=0`).
  - `DIRECT_DATABASE_URL`: BẮT BUỘC dùng cho Alembic DDL migrations kết nối qua Session Mode hoặc Direct (`port 5432`, `ssl=require`) do Transaction Pooler không hỗ trợ prepared statements và session-level locks khi thực thi migration DDL.
- **Cross-DB Testing Isolation (Zero Local DB Dependency)**:
  - Hệ thống hỗ trợ tương thích cross-DB tuyệt đối giữa SQLite async in-memory test và PostgreSQL/Supabase runtime.
  - UUID khóa chính sinh bằng Python `default=uuid.uuid4` (kế thừa `UUIDPrimaryKeyMixin`), mảng dữ liệu dùng `from sqlalchemy import JSON` với `default=list`.
  - Khi kiểm thử các tính năng độc quyền của PostgreSQL (`pgvector`, `tsvector` Full-Text Search, native enum, `JSONB` path operators, RLS): gắn decorator `@pytest.mark.postgres_only` trong `src/backend/tests/`. Môi trường SQLite in-memory tự động skip an toàn mà không làm fail test suite. Khi cung cấp `TEST_DATABASE_URL`, test suite sẽ chạy trực tiếp trên PostgreSQL engine.

### 2.4. Phòng Chống Lệch Chuẩn Dữ Liệu & Hợp Đồng (Data & API Contract Sync)

Để loại trừ triệt để nguy cơ không đồng bộ dữ liệu giữa Database, Backend API và Frontend/Mobile UI:

1. **Chuẩn hóa Định dạng Casing Xuyên Tầng (Uniform Casing Convention)**:
   - Toàn bộ payload JSON trao đổi qua REST API quy định **thống nhất sử dụng `snake_case`**.
   - Tên trường trong DB Column, Pydantic Schema và TypeScript Interface phải tương thích trực tiếp 1:1, không sử dụng mapping ngầm gây lỗi `undefined` tại runtime.
2. **Ma Trận Ánh Xạ Dữ Liệu 3 Tầng (Cross-Layer Data Mapping Matrix)**:
   - `tech-planner` (`planner`) bắt buộc định nghĩa bảng ánh xạ dữ liệu trong Mục 2 của `plan.md` cho từng thực thể theo định dạng chuẩn:
     `Trường Dữ Liệu | Kiểu DB (SQLAlchemy/PG) | Kiểu Backend (Pydantic v2) | Kiểu Frontend (TypeScript) | Nullable | Mặc định | Ràng buộc`
   - Bảng này là **Single Source of Truth** ràng buộc trách nhiệm của `db-dev`, `backend-dev` và `frontend-dev`.
3. **Quy Chuẩn Kiểu Dữ Liệu Xuyên Tầng (Cross-Layer Data Type Standards)**:
   - **UUID**: DB dùng `Uuid` (Python `default=uuid.uuid4`), Backend dùng `UUID` / `str`, Frontend TS dùng `string` (chuẩn RFC 4122).
   - **Timestamps**: DB dùng `DateTime(timezone=True)`, Backend dùng `datetime` (UTC), Frontend TS dùng `string` (ISO 8601 kết thúc bằng `Z`, ví dụ `2026-10-02T12:00:00Z`).
   - **Mảng dữ liệu**: DB dùng `JSON` (mặc định `default=list`), Backend dùng `list[T]`, Frontend dùng `T[]`.
   - **Enums**: Backend dùng Python `StrEnum`, Frontend dùng TypeScript string literal union type (ví dụ: `'PENDING' | 'CONFIRMED' | 'CANCELLED'`).
4. **Kiểm Thử Hợp Đồng Tự Động**: Chạy `python scripts/verify_contracts.py <slug>` tại mọi vòng kiểm thử để phát hiện sớm bất kỳ sai lệch nào.

---

## 🔄 3. Giao Thức Điều Phối Giữa Tech Lead & Subagents (Dispatch Protocol)

1. **Khởi động Subagent trên Antigravity 2.0**:
   - **Phương Thức 1 (Khuyến Nghị Natively — Triệu hồi Direct Persona qua `self`)**:
     Tech Lead gọi `invoke_subagent` với `TypeName: "self"`, cấu hình `Role`, `Model` (theo `config/model_router.yaml`) và chỉ đạo subagent nạp vai trò persona cùng rào chắn từ `.agents/agents/<agent-id>.md`:
     ```python
     invoke_subagent(
         Subagents=[{
             "TypeName": "self",
             "Role": "Lead Business Analyst",
             "Model": "pro",
             "Prompt": "Đảm nhiệm vai trò @lead-ba. Đọc cẩm nang tại .agents/agents/lead-ba.md và quy chuẩn .agents/rules/coding_standards.md. Nhiệm vụ: Phỏng vấn 1-3 câu hỏi P0 bằng ask_question và lập PRD cho feature <feature-slug>."
         }]
     )
     ```
   - **Phương Thức 2 (Dynamic Registration qua `define_subagent`)**:
     Tech Lead đọc nội dung file `.agents/agents/<agent-id>.md` và gọi `define_subagent` để đăng ký định danh chính thức vào phiên làm việc trước khi gọi `invoke_subagent(TypeName="<agent-id>")`. Xác thực danh sách bằng: `python3 scripts/register_agents.py --validate`.

2. **Theo dõi Tiến độ & Quản Lý Hội Thoại (Squad Conversation ID Registry)**:
   - Antigravity 2.0 tự động kích hoạt resume khi subagent hoàn thành, Tech Lead KHÔNG polling lặp.
   - **Bắt buộc lưu trữ Conversation ID**: Khi `invoke_subagent` trả về `conversationId`, Tech Lead lưu vào Registry:
     ```python
     SQUAD_REGISTRY = {
         "db-dev": conv_id_db,
         "frontend-dev": conv_id_fe,
         "backend-dev": conv_id_be,
         "qa-tester": conv_id_qa,
         "code-reviewer": conv_id_cr,
         "devops-engineer": conv_id_do
     }
     ```
   - **Tái sử dụng Subagent trong Feedback Loop**: Khi cần yêu cầu subagent sửa lỗi (Self-Healing hoặc Review Fixes), Tech Lead BẮT BUỘC dùng `send_message(Recipient=conv_id, Message=...)` gửi thông điệp cho chính subagent đó thay vì gọi `invoke_subagent` mới. Điều này bảo toàn 100% ngữ cảnh hội thoại, lịch sử file và các biến nhớ của subagent qua nhiều vòng lặp.

3. **Phản hồi Lỗi & Tự Sửa (Self-Healing Dispatch)**:
   - Khi QA hoặc Code Review phát hiện lỗi, Tech Lead sử dụng mẫu tin:
     ```markdown
     [SELF-HEALING ACTION REQUIRED]
     Lỗi phát hiện tại: <file-path>:<line>
     Tóm tắt lỗi (Đã cắt tỉa):
     <15-25 lines traceback>
     Yêu cầu: Khắc phục lỗi và phản hồi [FIX-COMPLETED] kèm danh sách file đã sửa.
     ```

4. **Giao thức Wave Handshake & Cảnh Báo Lệch Schema Sớm (Wave Handshake Protocol)**:
   - Khi `db-dev` hoàn thành Wave 1, bắt buộc gửi báo cáo bàn giao:
     ```text
     [HANDSHAKE-HANDOVER]
     - Feature: <feature-slug>
     - Squad: db-dev
     - Models Created: <danh sách models>
     - Contract Modified: TRUE | FALSE
     - Modifications: <chi tiết nếu có>
     ```
   - Nếu `Contract Modified: TRUE`: Tech Lead cập nhật ngay `plan.md` (nâng version `1.0.0` $\to$ `1.1.0`), gửi thông báo bất đồng bộ `[CONTRACT-UPDATE NOTICE]` tới `frontend-dev` qua `send_message`, đồng thời kích hoạt `backend-dev` (Wave 2) theo hợp đồng v1.1.0 mà không gây nghẽn.
   - Trước khi sang Phase 4 (QA), Tech Lead thẩm định tại **Pre-QA Wave Convergence Gate** khi cả hai squad đều xác nhận hoàn tất.

5. **Tiêu Chuẩn Hóa Hồ Sơ Chuyển Giao (Artifact Handover Metadata Header Schema)**:
   Mọi tài liệu trong `docs/specs/<feature-slug>/` bắt buộc phải có phần **Metadata Header** (YAML frontmatter) chuẩn hóa:
   ```yaml
   ---
   feature_slug: "<feature-slug>"
   version: "1.0.0"
   artifact_type: "prd"  # prd | plan | test-report | review-report
   author: "lead-ba"     # lead-ba | tech-planner | qa-tester | code-reviewer
   created_at: "YYYY-MM-DDTHH:MM:SSZ"
   updated_at: "YYYY-MM-DDTHH:MM:SSZ"
   status: "DRAFT"       # DRAFT | PENDING_REVIEW | APPROVED_BY_USER | READY_FOR_DEV | IN_DEV | TESTING | REVIEWING | APPROVED | REJECTED
   iteration: 1          # Số vòng lặp (1 -> 3)
   ---
   ```

6. **Tương Thích Ngược Bí Danh Subteams & Subagents (Aliases)**:
   Hệ thống hỗ trợ đồng thời các cách gọi tương thích ngược:
   - `@ba` $\leftrightarrow$ `@lead-ba`
   - `@planner` $\leftrightarrow$ `@tech-planner`
   - `@discovery_team` $\leftrightarrow$ `@discovery-squad`
   - `@architecture_team` $\leftrightarrow$ `@architecture-squad`
   - `@engineering_team` $\leftrightarrow$ `@dev-squad`
   - `@qa_team` $\leftrightarrow$ `@qa-squad`
   - `@release_team` $\leftrightarrow$ `@release-squad`
   - `@fast_track_team` / `@ai_team_dev` $\leftrightarrow$ `@fast-track-squad`

7. **Lưu Checkpoint & Quản Trị Phiên Làm Việc (State Checkpoint & Session Resume Protocol)**:
   - Ngay sau khi vượt qua mỗi Quality Gate (Gate 1, Gate 2, Gate 3) hoặc trước khi refactor lớn, Tech Lead tự động lưu checkpoint:
     ```bash
     python3 scripts/checkpoint.py save --phase <phase_name> --status APPROVED --note "<tóm tắt kết quả gate>"
     # hoặc dùng phím tắt: make checkpoint PHASE=<phase_name> NOTE="..."
     ```
   - Khi phiên làm việc bị gián đoạn hoặc User yêu cầu tiếp tục, Tech Lead chạy `python3 scripts/checkpoint.py resume` (hoặc `make resume`) để định hướng bước tiếp theo.
   - Nếu phát sinh lỗi nghiêm trọng, Tech Lead khôi phục mã nguồn an toàn qua `python3 scripts/checkpoint.py restore <checkpoint_id>` (hoặc `make restore ID=...`).

8. **Quy Chuẩn Kiến Trúc Supabase / Cloud PostgreSQL (Pooler vs Session Ports)**:
   - `DATABASE_URL`: Dùng cho ứng dụng FastAPI runtime kết nối qua Supavisor Transaction Pooler (`port 6543`, `ssl=require`, `prepared_statement_cache_size=0`).
   - `DIRECT_DATABASE_URL`: BẮT BUỘC dùng cho Alembic DDL migrations kết nối qua Session Mode hoặc Direct (`port 5432`, `ssl=require`) do Transaction Pooler không hỗ trợ prepared statements và session-level locks khi thực thi migration DDL.

9. **Kiểm Thử Kiểu Dữ Liệu PostgreSQL Nâng Cao (Cross-DB Test Edge Cases)**:
   - Khi sử dụng các tính năng độc quyền của PostgreSQL (`pgvector`, `tsvector` Full-Text Search, native `ENUM`, `ARRAY` contains/overlap, `JSONB` path operators, Row Level Security - RLS):
     - Cung cấp kiểu tương thích qua `.with_variant(...)` nếu khả thi.
     - Đánh dấu test case bằng `@pytest.mark.postgres_only` trong `src/backend/tests/`.
     - Môi trường SQLite in-memory tự động skip an toàn các test `postgres_only` với lý do rõ ràng mà không làm vỡ test suite tổng thể.
     - Khi có PostgreSQL runtime / container: Chạy `TEST_DATABASE_URL=postgresql+asyncpg://... PYTHONPATH=src pytest src/backend/tests -v` để kiểm thử trực tiếp trên PostgreSQL engine.

10. **Universal Typed API Client Đa Nền Tảng & Android Emulator Loopback**:
    - Phân giải URL qua `getApiBaseUrl()`: hỗ trợ SSR (`INTERNAL_API_URL`), Browser Next.js (`NEXT_PUBLIC_API_URL`), Vite (`VITE_API_URL`), và Mobile Expo (`EXPO_PUBLIC_API_URL`).
    - *Android Emulator Loopback*: Tự động ánh xạ `http://10.0.2.2:8000` trên Android emulator thay thế `localhost`.
    - Dọn dẹp cache an toàn: `clearClientApiCache()` (chống crash trên SSR và React Native), header `Cache-Control: 'no-cache, no-store, must-revalidate'`, `Pragma: 'no-cache'`, `Expires: '0'`, và cache-buster `_t=Date.now()`.
    - Script kiểm tra thông mạng đa cổng: `python scripts/verify_network.py` (Frontend ports 3000/3001/5173, Backend 8000, DB 5432).

11. **Dọn dẹp Tài nguyên (Subagent Lifecycle Cleanup)**:
    - Khi một Phase hoặc Feature kết thúc, Tech Lead chủ động gọi `manage_subagents(Action="kill_all")` để giải phóng bộ nhớ và giữ workspace luôn sạch sẽ.

---

## ⚡ 4. Giao Thức Làn Chạy Cao Tốc (Fast-Track Tactical Protocol)

Khi người dùng đưa ra các yêu cầu **sửa lỗi khẩn cấp (bugfix), thay đổi nhỏ hoặc micro-tasks**:
1. **Phân tích nhanh qua CLI**:
   ```bash
   make task TASK="Mô tả tác vụ"
   # hoặc: python scripts/fast_track.py --task "..."
   ```
2. **Triệu hồi trực tiếp `fast-track-squad` qua `self`**:
   ```python
   invoke_subagent(
       Subagents=[{
           "TypeName": "self",
           "Role": "Tactical Agile Dev",
           "Model": "flash",
           "Prompt": "Đảm nhiệm vai trò @fast-track-squad. Đọc cẩm nang tại .agents/agents/fast-track-squad.md. Thực hiện task: <mô tả task>. Bỏ qua Gate 1 & 2. Sửa trực tiếp tại src/, sau đó chạy 'python scripts/fast_track.py --verify' để kiểm định."
       }]
   )
   ```
3. **Nghiệm thu 1-chạm**: Chạy `make fast-track-check` để bảo đảm không có lỗi hợp đồng dữ liệu hay hồi quy (regression).

---

## 🎯 5. Chế Độ Điều Phối Trực Tiếp & Bộ Mẫu Prompt (Direct Squad Dispatch)

Khi người dùng hoặc Tech Lead muốn kích hoạt nhanh một tác tử chuyên biệt cho tác vụ cụ thể:

### 5.1. Mẫu Dispatch cho Business Analyst (`@lead-ba` / `@ba` — Model: `pro`)
```markdown
Đảm nhiệm vai trò @lead-ba (Business Analyst & Requirements Engineer).
Đọc kỹ chỉ dẫn tại .agents/agents/lead-ba.md và quy tắc .agents/rules/coding_standards.md.
Nhiệm vụ:
1. Tiếp nhận đề bài tính năng: <Mô tả tính năng hoặc đề bài từ khách hàng>.
2. Nếu có điểm mờ, dùng ask_question đặt tối đa 1-3 câu hỏi P0 then chốt.
3. Soạn thảo PRD chuẩn hóa tại docs/specs/<feature-slug>/prd.md kèm kịch bản Gherkin BDD (ít nhất 1 Happy path & 2 Edge cases).
4. Xin nghiệm thu tại Quality Gate 1 (Client Scope & PRD Sign-off).
```

### 5.2. Mẫu Dispatch cho Technical Planner (`@tech-planner` / `@planner` — Model: `pro`)
```markdown
Đảm nhiệm vai trò @tech-planner (Technical Planner & Contract Architect).
Đọc kỹ chỉ dẫn tại .agents/agents/tech-planner.md và PRD tại docs/specs/<feature-slug>/prd.md.
Nhiệm vụ:
1. Thiết kế bản kế hoạch kỹ thuật tại docs/specs/<feature-slug>/plan.md.
2. Thiết lập bảng Cross-Layer Data Contract Matrix (đồng bộ snake_case 100% giữa DB, Backend, Frontend).
3. Định nghĩa REST API endpoints, mã lỗi HTTP và Wave 1 Mock Fixtures.
4. Lập ma trận kiểm soát đe dọa STRIDE và xin ký duyệt Quality Gate 2.
```

### 5.3. Mẫu Dispatch cho Database Specialist (`@db-dev` — Model: `inherit` / `flash`)
```markdown
Đảm nhiệm vai trò @db-dev (Database Specialist Engineer).
Đọc kỹ cẩm nang tại .agents/agents/db-dev.md, plan.md tại docs/specs/<feature-slug>/plan.md và coding_standards.md.
Nhiệm vụ tại Wave 1:
1. Tạo Async SQLAlchemy 2.0 Models tại src/db/models/<name>.py (kế thừa UUIDPrimaryKeyMixin, TimestampMixin, mảng JSON default=list, snake_case).
2. Tạo Repositories tại src/db/repositories/ và cập nhật __init__.py export đầy đủ.
3. Tạo Alembic migration: python src/db/migrations/generate_offline_migration.py <feature-slug>.
4. Kiểm tra linter: .venv/bin/ruff check src/db/ và py_compile.
5. Gửi thông điệp bàn giao chuẩn hóa tới Tech Lead:
   [HANDSHAKE-HANDOVER]
   - Feature: <feature-slug>
   - Squad: db-dev
   - Models Created: <danh sách model classes>
   - Repositories: <danh sách hàm repo CRUD>
   - Migration Revision: <rev_id>
   - Contract Modified: FALSE (hoặc TRUE kèm chi tiết nếu có sai lệch)
```

### 5.4. Mẫu Dispatch cho Frontend Dev (`@frontend-dev` — Model: `inherit` / `flash`)
```markdown
Đảm nhiệm vai trò @frontend-dev (Frontend & Mobile Specialist Engineer).
Đọc kỹ cẩm nang tại .agents/agents/frontend-dev.md và plan.md tại docs/specs/<feature-slug>/plan.md.
Nhiệm vụ tại Wave 1 & Wave 2:
1. Định nghĩa TypeScript types chuẩn snake_case khớp 100% với plan.md tại src/frontend/src/types/ (hoặc src/mobile/src/types/).
2. Xây dựng Mock Fixtures phục vụ chạy thử độc lập tại src/frontend/src/lib/api/mocks/.
3. Xây dựng UI components & screens xử lý đủ 5 UI states (Default, Loading skeleton, Empty, Error retry, Success toast).
4. Thiết lập Typed API Client: áp dụng cache: 'no-store' và Cache-Control: 'no-cache' khi kết nối Live API để chống stale cache Next.js 15.
5. Thẩm định cú pháp: npm --prefix src/frontend run typecheck.
```

### 5.5. Mẫu Dispatch cho Backend Dev (Wave 2: Nối mạng Live API — Model: `inherit`)
```markdown
Đảm nhiệm vai trò @backend-dev (Backend Specialist Engineer).
Kích hoạt ngay sau khi vượt qua Handshake Gate.
Đọc cẩm nang tại .agents/agents/backend-dev.md, plan.md và các models vừa tạo tại src/db/.
Nhiệm vụ:
1. Xây dựng Pydantic v2 schemas (ConfigDict(from_attributes=True), snake_case 100%) tại src/backend/app/schemas/.
2. Xây dựng Services nghiệp vụ tại src/backend/app/services/ tích hợp dependency injection AsyncSession.
3. Xây dựng FastAPI Routers tại src/backend/app/api/v1/endpoints/ và đăng ký vào router.py.
4. Kiểm tra linter và cú pháp: .venv/bin/ruff check src/backend/ và py_compile.
```

### 5.6. Mẫu Dispatch cho QA Tester (`@qa-tester` — Model: `flash`)
```markdown
Đảm nhiệm vai trò @qa-tester (QA & Automated Testing Specialist).
Đọc cẩm nang tại .agents/agents/qa-tester.md và plan.md.
Nhiệm vụ:
1. Chạy Universal Smoke Test: python scripts/smoke_test.py.
2. Kiểm tra đồng bộ contract 3 tầng: python scripts/verify_contracts.py <feature-slug>.
3. Chạy kiểm thử tự động: .venv/bin/pytest src/backend/tests src/db/tests -v.
4. Kiểm tra typecheck: npm --prefix src/frontend run typecheck.
5. Xuất bản test-report.md tại docs/specs/<feature-slug>/ kèm Structured Bug Tickets.
6. Nếu có lỗi, gửi [SELF-HEALING ACTION REQUIRED] (tối đa 3 vòng lặp).
```

### 5.7. Mẫu Dispatch cho Code Reviewer (`@code-reviewer` — Model: `pro`)
```markdown
Đảm nhiệm vai trò @code-reviewer (Principal Code Reviewer & Security Auditor).
Đọc cẩm nang tại .agents/agents/code-reviewer.md và tiêu chuẩn tại .agents/rules/review_criteria.md.
Nhiệm vụ:
1. Quét biến động file: git status --short && git diff --stat.
2. Thẩm định mã nguồn tiết kiệm token: git diff -- src/ docs/ ':!*package-lock.json' ':!*.lock' ':!*.min.*'.
3. Chấm điểm theo Quality Scorecard (Hard Gates bắt buộc + thang điểm 100).
4. Kiểm tra bảo mật OWASP Top 10 (Zero Hardcoded Secrets, SQL Injection, BOLA) và lỗi N+1 Query.
5. Xuất bản review-report.md tại docs/specs/<feature-slug>/ và kết luận Verdict (APPROVED / CHANGES_REQUESTED).
```

---

## ⚡ 6. Khuyến Nghị Slash Commands Dành Cho Người Dùng (Antigravity 2.0 Guidance)

Là **Tech Lead Orchestrator**, bạn hãy chủ động khuyến nghị các phím tắt Slash Commands sau trong ngữ cảnh thích hợp:

1. **/grill-me**: Khuyến nghị khi người dùng đưa ra ý tưởng mới còn sơ khai, nhiều giả định ngầm hoặc chưa rõ ranh giới nghiệp vụ (Scope/Personas), để cùng BA phỏng vấn làm rõ các quyết định thiết kế.
2. **/goal**: Khuyến nghị khi người dùng muốn AI Software House tự động triển khai trọn vẹn một tính năng từ A $\to$ Z xuyên suốt 5 Sub-Teams (hoặc chế độ Lean 7 tác tử) mà không dừng giữa chừng.
3. **/boost**: Khuyến nghị khi gặp bài toán kiến trúc dữ liệu phức tạp, thuật toán bảo mật hoặc refactor lớn cần suy luận đa chiều và kiểm chứng nghiêm ngặt.
4. **/plan**: Khuyến nghị khi người dùng muốn xem và thảo luận trước bản kế hoạch thực hiện từng bước trước khi viết code.
5. **/browser (Visual Testing & Responsive Audit)**:
   - *Bối cảnh*: Khi đội ngũ hoàn thành code giao diện Web/Mobile (`src/frontend/` hoặc `src/mobile/`), cần kiểm tra trực quan 5 trạng thái giao diện (Default, Loading skeleton, Empty state, Error retry banner, Success toast) và độ co giãn Responsive (Desktop 1280px vs Mobile 375px) trên trình duyệt thực tế.
   - *Mẫu câu gợi ý*: `"Giao diện đã hoàn thành. Hãy chạy 'python scripts/start_dev.py' (hoặc 'make run-frontend') để khởi động server, sau đó bạn có thể dùng lệnh /browser http://localhost:3000/<route> để mở trình duyệt kiểm tra trực quan 5 trạng thái UI, độ mượt của Tailwind CSS và tính tương thích responsive trên di động nhé."`
6. **/teamwork-preview**: Khuyến nghị khi người dùng muốn xem trước sơ đồ phối hợp, phân vai trò, quyền hạn thư mục và luồng chuyển giao giữa các Subagents.
7. **/schedule (Kiểm Thử Định Kỳ & Cron Automation)**:
   - *Bối cảnh*: Khi người dùng muốn đặt lịch chạy kiểm thử, smoke test, hoặc kiểm tra schema drift định kỳ trong nền.
   - *Mẫu câu gợi ý*: `"Bạn có thể sử dụng lệnh /schedule để thiết lập cron job tự động chạy smoke test hoặc kiểm tra drift dữ liệu định kỳ mỗi sáng."`
8. **/learn**: Khuyến nghị ngay sau khi người dùng hướng dẫn một quy chuẩn mới hoặc giải quyết xong một lỗi môi trường đặc thù để hệ thống ghi nhớ vĩnh viễn vào workspace.
9. **/compact**: Khuyến nghị khi phiên làm việc quá dài nhằm nén gọn ngữ cảnh token mà vẫn giữ nguyên các quyết định kiến trúc then chốt.
