# AI-Vibe-Coding: Công Ty Phát Triển Phần Mềm AI Toàn Năng Trên Antigravity 2.0

**AI-Vibe-Coding** là template kiến trúc mẫu chuyển hóa môi trường làm việc của bạn thành một **Công ty Phát triển Phần mềm AI Toàn Năng (AI Software House)** vận hành khép kín trên nền tảng **Antigravity 2.0**.

Template mô phỏng trọn vẹn quy trình Agency / Software House chuyên nghiệp: từ khâu tiếp nhận yêu cầu thô từ Khách hàng $\rightarrow$ Phỏng vấn nghiệp vụ $\rightarrow$ Xuất bản PRD & UI/UX Concept $\rightarrow$ Thiết kế Kiến trúc & Hợp đồng Dữ liệu $\rightarrow$ Lập trình Đợt kép (2-Wave Dev) $\rightarrow$ Kiểm thử Tự động 5 tầng $\rightarrow$ Thẩm định Chất lượng Code & Bảo mật $\rightarrow$ Tự sửa lỗi (Self-Healing Loop) $\rightarrow$ Đóng gói & Bàn giao Sản phẩm hoàn chỉnh.

---

## 🏛️ Sơ Đồ Vận Hành 5 Sub-Teams (15 Subagents)

```mermaid
flowchart TD
    Client(["Khách hàng / Product Owner<br/>(Ý tưởng thô / Brief / Feature Request)"]) --> ST1["1. Sub-Team Discovery & Solutions<br/>(account-lead + lead-ba + uiux-designer)"]
    
    ST1 --> Gate1{"GATE 1: Client Sign-off<br/>(Duyệt Scope, PRD & UI Concept)"}
    
    Gate1 -- Chấp thuận --> ST2["2. Sub-Team Architecture & Planning<br/>(system-architect + security-architect + tech-planner)"]
    Gate1 -- Cần làm rõ --> ST1
    
    ST2 --> Gate2{"GATE 2: Technical Sign-off<br/>(Duyệt Kiến trúc, ERD & Data Contract Matrix)"}
    
    Gate2 -- Chấp thuận --> ST3["3. Sub-Team Core Engineering (2-Wave Execution)<br/>• Wave 1: db-dev + frontend-dev (Mock Fixtures)<br/>• Handshake Gate<br/>• Wave 2: backend-dev (Live APIs) + devops-engineer"]
    Gate2 -- Sửa đổi --> ST2
    
    ST3 --> ST4["4. Sub-Team QA & Security Audit<br/>(qa-tester + code-reviewer)"]
    
    ST4 -- Báo lỗi (Self-Healing Loop max 3x) --> ST3
    
    ST4 --> Gate3{"GATE 3: Production Readiness<br/>(100% Tests Pass, Zero Critical Security Flaws)"}
    
    Gate3 -- Đạt chuẩn --> ST5["5. Sub-Team Release & Client Handover<br/>(release-engineer + tech-writer + handover-lead)"]
    Gate3 -- Chưa đạt --> ST3
    
    ST5 --> Deliverable(["Thành Phẩm Bàn Giao Khách Hàng<br/>(Source Code + Release Package .zip + User Manual + UAT Checklist)"])
```

---

## 👥 Danh Sách 5 Sub-Teams & 15 Subagents Chuyên Trách

| Sub-Team | Subagent ID | Vai trò chính | Model Tier | Thư mục quyền sở hữu |
| :--- | :--- | :--- | :--- | :--- |
| **1. Discovery & Solutions** | `account-lead` | Tiếp nhận yêu cầu, T-shirt sizing, bóc tách In-Scope vs Out-of-Scope | `flash` | `docs/specs/<slug>/` |
| | `lead-ba` | Phỏng vấn làm rõ qua `ask_question`, xuất bản `prd.md` với Gherkin stories | `pro` | `docs/specs/<slug>/` |
| | `uiux-designer` | Sơ đồ luồng màn hình (Mermaid), Design Tokens, Ma trận 5 UI states | `flash` | `docs/specs/<slug>/` |
| **2. Architecture & Planning**| `system-architect` | Phân tầng Clean Architecture, mô hình dữ liệu quan hệ ERD | `pro` | `docs/specs/<slug>/` |
| | `security-architect`| Mô hình đe dọa STRIDE, phân quyền RBAC/ABAC, OWASP Guardrails | `pro` | `docs/specs/<slug>/` |
| | `tech-planner` | Kế hoạch kỹ thuật `plan.md`, Cross-Layer Contract Matrix, REST specs | `pro` | `docs/specs/<slug>/` |
| **3. Core Engineering** | `db-dev` | SQLAlchemy 2.0 Async Models, Alembic Migrations, Async Repos, Seeds | `inherit` | `src/db/` |
| | `frontend-dev` | Web Next.js 15 / React Vite + Mobile React Native Expo, 5 UI states | `inherit` | `src/frontend/`, `src/mobile/` |
| | `backend-dev` | Pydantic v2 schemas (`snake_case`), Services nghiệp vụ, FastAPI routes | `inherit` | `src/backend/` |
| | `devops-engineer` | Dockerfile, docker-compose, scripts khởi chạy, cấu hình môi trường | `flash` | `docker-compose.yml`, `scripts/` |
| **4. QA & Security Audit** | `qa-tester` | Thực thi bộ test 5 tầng (`smoke_test.py`), điều phối Self-Healing loop | `flash` | `docs/specs/`, `tests/` |
| | `code-reviewer` | Audit Git diff tối ưu token, bảng điểm chất lượng 100đ, duyệt Gate 3 | `pro` | `docs/specs/` |
| **5. Release & Handover** | `release-engineer`| Build check, Git Conventional Commits, đóng gói bản phát hành `.zip` | `flash_lite`| `dist/`, `scripts/` |
| | `tech-writer` | Soạn thảo `USER_MANUAL.md`, `API_GUIDE.md`, `DEPLOYMENT.md` | `flash_lite`| `docs/specs/` |
| | `handover-lead` | Lập bảng kiểm `UAT_CHECKLIST.md`, hướng dẫn nghiệm thu 1-chạm | `flash` | `docs/specs/<slug>/` |
| **Tactical Agile** | `fast-track-squad`| Làn chạy cao tốc cho micro-tasks & bugfix, bỏ qua Gate 1 & 2 | `flash` | `src/` |

---

## 🎯 Định Vị Dự Án: Sweet Spot vs Non-Goals Decision Matrix

Template được tối ưu hóa chuyên sâu cho các dự án **Full-Stack Web & Mobile Applications Hiện Đại** sử dụng bộ đôi công nghệ **Python (FastAPI) + TypeScript (Next.js 15 / React Vite / React Native Expo)** kết hợp cơ sở dữ liệu quan hệ **PostgreSQL**.

### 1. Checklist Đánh Giá Phù Hợp Dự Án (Quick Decision Matrix)
Trả lời 4 câu hỏi trắc nghiệm nhanh trước khi triển khai:
1. **Bạn có cần ứng dụng Web (Next.js 15 / React Vite) hoặc Mobile App (React Native Expo)?** $\to$ **CÓ**
2. **Bạn có cần một Backend API bất đồng bộ hiệu năng cao bằng Python không?** (FastAPI, Pydantic v2) $\to$ **CÓ**
3. **Bạn có lưu trữ dữ liệu quan hệ có ràng buộc, giao dịch ACID không?** (PostgreSQL, SQLAlchemy 2.0 Async) $\to$ **CÓ**
4. **Bạn có muốn AI tự động thiết kế, lập trình, kiểm thử và review code độc lập không?** (Antigravity 2.0 Multi-Agent) $\to$ **CÓ**

> 👉 **Nếu có từ 3 câu trả lời "CÓ" trở lên**: Đây chính xác là template hoàn hảo dành riêng cho dự án của bạn!

### 2. Các Loại Dự Án Phù Hợp Nhất (Sweet Spot / Best Fit)
| Loại hình dự án | Mô tả chi tiết | Độ phù hợp |
| :--- | :--- | :--- |
| **SaaS Web Platforms** | Các ứng dụng SaaS quản lý thuê bao, xác thực, phân quyền (RBAC), thanh toán và dashboard báo cáo số liệu. | ⭐⭐⭐⭐⭐ (Hoàn hảo) |
| **Mobile Apps (iOS & Android)** | Ứng dụng di động kết nối trực tiếp với FastAPI backend, styling siêu tốc qua NativeWind Tailwind CSS. | ⭐⭐⭐⭐⭐ (Hoàn hảo) |
| **Fullstack Web & Mobile Song hành** | Hệ sinh thái hoàn chỉnh gồm cả Web Admin Portal (Next.js/Vite) và App điện thoại (React Native Expo). | ⭐⭐⭐⭐⭐ (Hoàn hảo) |
| **Internal Tools & Dashboards** | Hệ thống CRM nội bộ, quản trị bán hàng, theo dõi đơn hàng, quản lý kho bãi, nhân sự. | ⭐⭐⭐⭐⭐ (Hoàn hảo) |
| **Startup MVP $\to$ Production** | Dự án khởi nghiệp cần đưa tính năng ra thị trường thần tốc bằng AI nhưng kiến trúc vẫn sạch và mở rộng được. | ⭐⭐⭐⭐⭐ (Hoàn hảo) |
| **REST API Micro/Modular Backend** | Cần một Backend API chuẩn mực, có Swagger UI tự động và tài liệu hợp đồng API chặt chẽ. | ⭐⭐⭐⭐ (Rất tốt) |

### 3. Khi Nào KHÔNG NÊN Dùng Template Này? (Non-Goals)
- ❌ **Hệ thống Microservices đa ngôn ngữ (Java, Go, Rust, .NET kết hợp)**: Template thiết kế tối ưu cho mô hình Modular Monolith hoặc 2-Tier/3-Tier.
- ❌ **Data Science / Machine Learning thuần túy**: Nếu dự án chỉ chạy Jupyter Notebook, huấn luyện model PyTorch/TensorFlow lớn mà không cần web/mobile/API.
- ❌ **Website tĩnh đơn giản (Static Blog, Landing Page 1 trang)**: Nên dùng Astro, Hugo hoặc HTML tĩnh không cần DB/FastAPI.

---

## 🌐 Quy Chuẩn Kết Nối Database & Supabase (Transaction Pooler vs Direct Mode)

- **PostgreSQL & Supabase Runtime**:
  - `DATABASE_URL`: Dùng cho ứng dụng FastAPI runtime kết nối qua Supavisor Transaction Pooler (`port 6543`, `ssl=require`, `prepared_statement_cache_size=0`).
  - `DIRECT_DATABASE_URL`: BẮT BUỘC dùng cho Alembic DDL migrations kết nối qua Session Mode hoặc Direct (`port 5432`, `ssl=require`) do Transaction Pooler không hỗ trợ prepared statements và session-level locks khi thực thi migration DDL.
- **Cross-DB Testing Pattern**:
  - Tương thích cross-DB tuyệt đối giữa SQLite in-memory test và PostgreSQL/Supabase runtime (UUID sinh qua Python `default=uuid.uuid4`, mảng dữ liệu qua `JSON`).
  - Khi kiểm thử các tính năng độc quyền của PostgreSQL (`pgvector`, `tsvector`, native enum, JSONB path), gắn decorator `@pytest.mark.postgres_only` trong `src/backend/tests/`. Môi trường SQLite in-memory sẽ tự động skip an toàn mà không làm fail test suite. Khi cung cấp `TEST_DATABASE_URL`, test suite sẽ chạy trực tiếp trên PostgreSQL engine.

---

## 🚦 Cơ Chế Vận Hành Hai Làn (Dual-Track SDLC Architecture)

Template vận hành linh hoạt theo 2 làn chạy chuyên biệt:

1. **Làn 1: Enterprise Full-Lifecycle SDLC (Dự án mới & Tính năng lớn)**:
   - Áp dụng đầy đủ 5 Sub-Teams, 7 Giai đoạn và 3 Chốt chặn Quality Gates (Client Sign-off $\rightarrow$ Tech Architecture Sign-off $\rightarrow$ Production Readiness).
   - Kiểm soát nghiêm ngặt rủi ro, bảo đảm 100% tài liệu PRD, ERD, STRIDE và UAT Checklist.

2. **Làn 2: Tactical Fast-Track SDLC (Bugfixes & Micro-Tasks hàng ngày)**:
   - Dành cho các sửa đổi cục bộ, hotfix, thêm 1 endpoint hoặc 1 component nhỏ.
   - Bỏ qua Gate 1 & Gate 2, chỉ kích hoạt `fast-track-squad` thực hiện: **Phân tích tác động (Impact Analysis) $\rightarrow$ Sửa code tối thiểu $\rightarrow$ Kiểm tra hợp đồng & Pytest $\rightarrow$ Auto-Commit**.
   - Kích hoạt qua 1 dòng lệnh: `make task TASK="Mô tả tác vụ"` hoặc `make fast-track`.

---

## 📂 Cơ Chế Phân Định Hai Không Gian Thực Thi (Target Workspace Dual Mode)

Để loại bỏ hoàn toàn sự nhập nhằng giữa khung mã nguồn có sẵn và các dự án sinh tự động:
1. **Chế độ In-Place Development (`src/`) — Mặc định**:
   - Sử dụng khi lập trình, mở rộng hoặc bảo trì ứng dụng chính trong repository.
   - Các Subagents thao tác trực tiếp tại: `src/db/`, `src/backend/`, `src/frontend/`, `src/mobile/`.
   - Kiểm thử và review code trực tiếp trên cây thư mục `src/`.
2. **Chế độ Greenfield Autonomous Generation (`workspaces/output_project/`)**:
   - Sử dụng khi tiếp nhận một Client Brief độc lập hoàn toàn mới từ bên ngoài qua CLI:
     `make dev PROJECT="TênDựÁn" FILE="workspaces/brief.md" PLATFORM="web|mobile"`
   - Toàn bộ artifacts và mã nguồn sinh mới sẽ được lưu cô lập trong `workspaces/output_project/` và `workspaces/artifacts/`.
   - Có thể sao lưu an toàn qua `make backup` hoặc làm sạch sẵn sàng cho dự án tiếp theo qua `make clean-project`.

---

## 🛡️ 4 Trụ Cột Kỹ Thuật Bảo Vệ (Guardrails)

1. **Đồng Bộ Hợp Đồng Đa Tầng 3 Chiều (Cross-Layer Contract Sync)**:
   - Toàn bộ tên trường và quan hệ dữ liệu giữa Database Model, Pydantic Schema và TypeScript Interface được chuẩn hóa đồng bộ 100% bằng casing `snake_case`.
   - Script tự động `python scripts/verify_contracts.py` ngăn chặn hoàn toàn lỗi lệch chuẩn kiểu dữ liệu.

2. **Rào Chắn Thực Thi & Phân Vùng Mã Nguồn (File Partition & Execution Guardrails)**:
   - Mỗi subagent chỉ có quyền đọc/ghi trong thư mục được phân công rõ ràng.
   - Các subagents tài liệu tuyệt đối không được chạy shell làm thay đổi mã nguồn.

3. **Vòng Lặp Tự Sửa Lỗi Có Ngắt Mạch (Self-Healing Loop & Circuit Breaker)**:
   - Script `scripts/parse_traceback.py` cắt tỉa log lỗi còn 15-25 dòng trọng tâm, chống phình token context.
   - Bộ ngắt mạch an toàn: Giới hạn tối đa **3 vòng lặp**. Nếu quá 3 lần, dừng tiến trình xin chỉ đạo từ Tech Lead / User.

4. **Tối Ưu Chi Phí Token (Model Cost Routing Matrix)**:
   - Phân bổ 3 tầng mô hình: `pro` cho bài toán nhận thức sâu (BA, Architect, Reviewer), `flash` cho lặp nhanh (QA, UI, DevOps), `flash_lite` cho tài liệu/manifest (Release, Tech Writer), tiết kiệm 65-80% chi phí vận hành.

5. **Kiến Trúc Client Linh Hoạt (Client Presets Scaffolding - Tinh hoa từ `AI-Team-Dev`)**:
   - Chuyển đổi mượt mà giữa Web Next.js 15 (SSR/SEO) và React + Vite (SPA/Dashboard) hoặc khởi tạo Mobile React Native Expo qua `scripts/setup_frontend.py` (`make preset-vite`, `make preset-nextjs`, `make add-mobile`).

6. **Quản Trị Trạng Thái SDLC & Phục Hồi Phiên (State Checkpoints & Rollback - Tinh hoa từ `Multi-Agents-Dev`)**:
   - Tự động lưu checkpoint tại từng Quality Gate kèm bản chụp mã nguồn sạch (< 1s), hỗ trợ tiếp tục phiên làm việc (`make resume`) hoặc khôi phục mã nguồn an toàn khi gặp sự cố (`make restore ID=...`).

7. **Headless SDLC & Heuristic Auto-Healing (Tự Động Hóa CI/CD & Vá Lỗi Zero-Token - Tinh hoa từ `Multi-Agents-Dev`)**:
   - Chạy tự động hóa toàn bộ 5 Phase không cần giao diện qua `make dev-quick` (`scripts/run_headless_sdlc.py`), hỗ trợ chốt chặn tương tác Terminal TUI qua `make gate-interactive`.
   - Tự động sửa lỗi phổ biến (secret leaks, UUID collision, CORS, Pydantic v2) không tốn token LLM qua `make auto-heal` (`scripts/auto_heal_heuristics.py`).
   - Tương thích ngược toàn diện với các lệnh quen thuộc của `AI-Team-Dev` (`make check-contracts`, `make check-migrations`, `make setup-nextjs/vite/mobile`).

---

## 📁 Cấu Trúc Thư Mục Dự Án

```text
AI-Vibe-Coding/
├── AGENTS.md                                # Cẩm nang điều phối tổng của Tech Lead (Main Agent)
├── GEMINI.md                                # Quy chuẩn chỉ dẫn gốc cho Antigravity 2.0
├── WORKFLOW.md                              # SOP chi tiết quy trình 7 giai đoạn của công ty
├── USER_GUIDE.md                            # Cẩm nang hướng dẫn sử dụng chi tiết
├── Makefile                                 # Bộ tự động hóa 1-chạm (dev, test, smoke, presets, checkpoints)
├── run.ps1                                  # Bộ tự động hóa PowerShell cho Windows
├── docker-compose.yml                       # Khởi chạy Fullstack (PostgreSQL, Backend, Frontend)
├── pyproject.toml                           # Cấu hình dự án Python & dependencies
├── alembic.ini                              # Cấu hình database migrations
├── .env.example                             # Biến môi trường mẫu
│
├── .agents/                                 # Hệ sinh thái Native Antigravity 2.0
│   ├── agents/                              # 15 Subagents chuyên trách (.md) + 5 Squad Orchestrators
│   ├── rules/                               # Quy chuẩn code, an ninh, review criteria
│   └── skills/                              # Kỹ năng nghiệp vụ chuyên biệt (SKILL.md)
│
├── config/                                  # Cấu hình công ty, định tuyến mô hình, quality gates
│   ├── company_profile.yaml
│   ├── model_router.yaml
│   └── quality_gates.yaml
│
├── templates/                               # Kho Presets Client kế thừa từ AI-Team-Dev
│   └── presets/                             # Next.js 15, React Vite, React Native Expo
│
├── docs/                                    # Hồ sơ bóc tách theo tính năng (docs/specs/<slug>/)
├── scripts/                                 # Động cơ điều phối SDLC, Automation Day-0, Checkpoints, Presets & Release
│   ├── runner.py                            # Headless & Interactive SDLC Multi-Agent Runner
│   ├── fast_track.py                        # Động cơ Track 2 Fast-Track (Tactical Agile Squad)
│   ├── dag_engine.py                        # Động cơ đồ thị phân giải phụ thuộc Wave DAG
│   ├── synthesis_engine.py                  # Adaptive Code Synthesizer (Gemini API & AST)
│   ├── hitl.py                              # Human-in-the-Loop Review Gate Generator
│   ├── persistence.py & state.py            # SQLite State Machine & Checkpoints
│   ├── setup_frontend.py                    # Chuyển đổi linh hoạt Web Vite / Next.js / Mobile Expo
│   ├── checkpoint.py                        # Quản lý State Checkpoints, Session Resume & Rollback
│   ├── sync_state.py                        # Quét mã nguồn và đồng bộ ngược vào State Checkpoint
│   ├── snapshot.py                          # Chụp nhanh mã nguồn < 1s
│   ├── smoke_test.py / .sh / .ps1           # Kiểm thử tự động 5 tầng (Python / Bash / PowerShell)
│   └── bundle_release.py                    # Đóng gói bản phát hành (.zip, SHA-256 checksum, manifest, docs)
│
├── src/                                     # Toàn bộ mã nguồn thực tế (In-Place Development Mode)
│   ├── db/                                  # SQLAlchemy 2.0 Async, Alembic, Repositories, Seeds
│   ├── backend/                             # FastAPI Clean Architecture, Pydantic v2, Pytest
│   ├── frontend/                            # Next.js 15 / React Vite, Tailwind CSS, TypeScript
│   └── mobile/                              # React Native Expo, NativeWind Tailwind
│
├── workspaces/                              # Phân vùng làm việc độc lập (Multi-Project Agency Mode)
│   ├── output_project/                      # Mã nguồn dự án đích được sinh tự động
│   ├── artifacts/                           # Hồ sơ PRD, OpenAPI, ERD, Gate Reviews (01_discovery -> 05_handover)
│   ├── checkpoints/                         # SDLC State Checkpoints lưu trữ
│   └── backups/                             # Bản sao lưu an toàn tự động (Overwrite Protection)
│
├── examples/                                # Đề bài thực tế & Golden Reference
│   ├── sample_client_brief.md               # Đề bài mẫu MotoCare
│   ├── cliniccare_sample_brief.md           # Đề bài mẫu y tế ClinicCare
│   └── motocare_reference/                  # Dự án mẫu hoàn chỉnh làm chuẩn tham chiếu
├── tests/                                   # Bộ kiểm thử tự động cho chính template/orchestrator
└── dist/                                    # Gói phát hành & Checkpoint lưu trữ
    ├── checkpoints/                         # SDLC State Checkpoints & LATEST_CHECKPOINT.json
    ├── snapshots/                           # Các bản lưu trữ mã nguồn .tar.gz
    └── releases/                            # Gói phát hành phần mềm hoàn chỉnh (.zip & .sha256)
```

---

## ⚡ Bắt Đầu Nhanh (Quickstart & Bảng Lệnh Điều Hành)

### 1. Khởi Tạo Môi Trường (Day-0)
```bash
# 1. Chuyển vào thư mục template
cd AI-Vibe-Coding

# 2. Khởi tạo môi trường
cp .env.example .env

# 3. Kiểm tra tính toàn vẹn của hợp đồng dữ liệu
make contracts

# 4. Chạy kiểm thử tự động (hoặc ./scripts/smoke_test.sh / .\scripts\smoke_test.ps1)
make test
```

### 2. Bảng Tra Cứu Lệnh Vận Hành Nhanh (Developer Cheat Sheet)

| Luồng nghiệp vụ | Lệnh Makefile | PowerShell (Windows) | Ý nghĩa & Mô tả |
| :--- | :--- | :--- | :--- |
| **Track 1: Enterprise SDLC** | `make dev-orchestrator` | `.\run.ps1 dev-orchestrator` | Chạy toàn trình 5 pha với 5 Sub-teams từ Client Brief |
| **Track 2: Tactical Fast-Track** | `make fast-track TASK="..."` | `.\run.ps1 fast-track -Task "..."` | Chạy nhanh micro-task/bugfix với Fast-Track Squad |
| **Duyệt Chốt Chặn Tương Tác** | `make gate-interactive` | `.\run.ps1 gate-interactive` | Mở Terminal TUI review & sign-off tại các Gate |
| **Đồng Bộ Mã Nguồn Ngược** | `make sync` | `.\run.ps1 sync` | Quét thay đổi code thủ công và cập nhật lại Checkpoint DB |
| **Tiếp Tục Phiên Làm Việc** | `make resume` | `.\run.ps1 resume` | Tiếp tục chính xác từ trạng thái dừng trước đó |
| **Kiểm Thử 5 Tầng 1-Click** | `make smoke` | `.\scripts\smoke_test.ps1` | Chạy linter, contracts, migrations, pytest & network |
| **Kiểm Thử Output Project** | `make test-output` | `.\run.ps1 test-output` | Chạy kiểm thử Backend, DB drift và Frontend trên output_project |
| **Chạy Output Project Server** | `make run-output-backend` | `.\run.ps1 run-backend` | Khởi chạy server FastAPI độc lập của output_project |
| **Chế Độ Tinh Gọn (Lean)** | `make lean-workspace` | `.\run.ps1 lean-workspace` | Dọn dẹp output_project, kích hoạt chế độ In-Place Vibe Coding |
| **Sao Lưu Dự Phòng** | `make backup` | `.\run.ps1 backup` | Tạo bản sao lưu an toàn trước khi overwrite dự án |
| **Khởi Chạy Servers** | `make dev` | `.\run.ps1 dev` | Chạy FastAPI (:8000) và Frontend (:3000) |
| **Đóng Gói Bàn Giao** | `make release` | `.\run.ps1 release` | Xuất file `.zip` kèm mã băm SHA-256, UAT & User Manual |

Truy cập Swagger UI tự động tại: `http://localhost:8000/api/v1/docs`.
