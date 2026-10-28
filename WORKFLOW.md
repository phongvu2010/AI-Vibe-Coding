# Quy Trình Vận Hành Chuẩn Công Ty Phần Mềm AI (SOP - WORKFLOW.md)
### Chu trình Phát triển Phần mềm Toàn diện từ Ý tưởng đến Bàn giao trên Antigravity 2.0

Tài liệu này là **Quy trình Vận hành Chuẩn (Standard Operating Procedure - SOP)** quy định chi tiết 7 giai đoạn khép kín mà **Tech Lead (Main Agent)** cùng **5 Sub-Teams (15 Subagents)** thực thi để hoàn thành một dự án hoặc tính năng cho Khách hàng.

---

## 🗺️ 1. Sơ Đồ Quy Trình Vận Hành 7 Giai Đoạn

```text
[Khách Hàng / Product Owner]
              │ (1. Ý tưởng thô / Brief / RFP)
              ▼
┌────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 0: Tiếp Nhận Khách Hàng, Bóc Tách Scope & PRD                │
│ • account-lead : Đánh giá Scope, T-shirt sizing, phân rã Epic          │
│ • lead-ba      : Phỏng vấn 1-3 câu P0 (ask_question), Gherkin stories  │
│ • uiux-designer: Sơ đồ luồng màn hình (Mermaid), Design Tokens, UI Spec│
│ ➔ Xuất bản: docs/specs/<slug>/prd.md & ui_ux_spec.md                   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ [QUALITY GATE 1: Client Sign-off]
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 1: Thiết Kế Kiến Trúc, Bảo Mật & Hợp Đồng Kỹ Thuật           │
│ • system-architect  : C4 diagrams, ERD quan hệ, Lựa chọn công nghệ     │
│ • security-architect: STRIDE Threat Model, RBAC/ABAC Matrix, OWASP     │
│ • tech-planner      : plan.md, Cross-Layer Data Contract Matrix, OpenAPI│
│ ➔ Xuất bản: docs/specs/<slug>/plan.md                                  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ [QUALITY GATE 2: Architecture Sign-off]
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 2: Thiết Lập Rào Chắn An Toàn & Chuẩn Bị Môi Trường          │
│ • Tech Lead rà soát Whitelist/Blacklist, kiểm tra .env và dependencies │
│ • Kiểm tra smoke test Day-0: ruff check, npm typecheck                 │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 3: Triển Khai Lập Trình Đợt Kép (2-Wave Pipelined Dev)       │
│                                                                        │
│  [Wave 1 - Chạy Song Song]                                             │
│  ├── db-dev       ──► src/db/ (SQLAlchemy 2.0 Models, Alembic, Seeds)  │
│  └── frontend-dev ──► src/frontend/, src/mobile/ (UI 5 states & Mocks) │
│                                                                        │
│  [Handshake Gate: Model & Types Compilation Check]                     │
│  │                                                                     │
│  ▼                                                                     │
│  [Wave 2 - Kết Nối Live API & Hạ Tầng]                                 │
│  ├── backend-dev     ──► src/backend/ (FastAPI Services & Endpoints)   │
│  └── devops-engineer ──► docker-compose.yml, Dockerfile, scripts       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 4: Kiểm Thử Tự Động & Vòng Lặp Sửa Lỗi (QA Squad)            │
│ • qa-tester chạy bộ kiểm thử 5 tầng:                                   │
│   1. Linter (ruff check src/)                                          │
│   2. Contract Sync (python scripts/verify_contracts.py <slug>)         │
│   3. Migration DAG (python scripts/verify_migrations.py)               │
│   4. Pytest (SQLite async in-memory fallback)                          │
│   5. Client Typecheck (npm run typecheck)                              │
│ ➔ Xuất bản: docs/specs/<slug>/test-report.md                           │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ [Self-Healing Loop: Max 3x]                                      │  │
│  │ Bắt lỗi -> Cắt tỉa traceback (15-25 dòng qua parse_traceback.py) │  │
│  │ Gửi Dev Squad sửa lỗi -> QA test lại                             │  │
│  │ Nếu vượt quá 3 lần: Kích hoạt CIRCUIT BREAKER báo Tech Lead      │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 5: Thẩm Định Code, Tối Ưu & Bảo Mật (Review Squad)           │
│ • code-reviewer audit `git diff` tối ưu token                          │
│ • Thẩm định: Clean Architecture, N+1 query, Injection, A11y            │
│ ➔ Xuất bản: docs/specs/<slug>/review-report.md                         │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ [Review-Fix Loop: Max 3x]                                        │  │
│  │ Nếu CHANGES_REQUESTED -> Dev Squad khắc phục -> Reviewer thẩm định│  │
│  └──────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ [QUALITY GATE 3: Production Readiness]
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ GIAI ĐOẠN 6: Đóng Gói Phát Hành, Soạn Tài Liệu & Bàn Giao Khách Hàng   │
│ • release-engineer: Build production check, git commit, bundle .zip    │
│ • tech-writer     : USER_MANUAL.md, API_GUIDE.md, DEPLOYMENT.md        │
│ • handover-lead   : UAT_CHECKLIST.md, Hướng dẫn 1-chạm cho khách hàng  │
│ • Tech Lead dọn dẹp subagents qua `manage_subagents(Action="kill_all")`│
└────────────────────────────────────────────────────────────────────────┘
```

---

## 👥 1b. Bảng Phân Công Trách Nhiệm, Model Tiering & Rào Chắn Lệnh (RACI Matrix & CLI Whitelist)

| Vai trò / Tác tử | Subagent ID | Model Tier | Thư mục sở hữu (Ownership) | Lệnh được phép (Whitelist) | Rào chắn cấm tuyệt đối (Blacklist) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Product Owner** | User (Con người) | - | Toàn dự án | Mọi lệnh hệ thống | - |
| **Tech Lead Orchestrator** | Main Agent | `inherit` | Toàn dự án | Điều phối subagents, `manage_subagents`, cập nhật dependencies manifest (`pyproject.toml`, `package.json`), chạy smoke/contracts/migrations, quản lý git commits | Cấm `git reset --hard`, `git push --force` |
| **Business Analyst Lead** | `lead-ba` / `ba` | `pro` | `docs/specs/<slug>/` | Phỏng vấn tối ưu 1-3 câu P0 (`ask_question`), chỉ đọc/ghi file tài liệu (`view_file`, `write_to_file`, `replace_file_content`) | Cấm chạy shell commands làm thay đổi code hoặc file manifest |
| **System & Tech Planner** | `system-architect` / `tech-planner` | `pro` | `docs/specs/<slug>/` | Chỉ đọc/ghi file tài liệu thiết kế kiến trúc, ERD, OpenAPI và Contract Matrix | Cấm chạy shell commands sửa code mã nguồn |
| **DB Specialist** | `db-dev` | `inherit` | `src/db/` | `python -m ruff check src/db/`, `python -m py_compile src/db/...`, `alembic check`, `alembic current`, `generate_offline_migration.py`, `runner.py` | Cấm `rm -rf`, `drop database`, cấm `pip install` trần, cấm sửa file ngoài `src/db/` |
| **Frontend & Mobile Dev** | `frontend-dev` | `inherit` / `flash` | `src/frontend/`, `src/mobile/` | Web: `npm --prefix src/frontend run typecheck`, `run lint`, `run build`; Mobile: `npm --prefix src/mobile run typecheck`, `run lint`, `node scripts/run_tests.cjs` | Cấm `npm install` trần, cấm tự ý sửa `package.json`, cấm remote fonts, cấm sửa ngoài `src/frontend/` và `src/mobile/` |
| **Backend Specialist** | `backend-dev` | `inherit` | `src/backend/` | `python -m ruff check src/backend/`, `python -m py_compile src/backend/...` | Cấm `pip install` trần, cấm sửa `pyproject.toml`, cấm sửa ngoài `src/backend/` |
| **QA Automated Tester** | `qa-tester` | `flash` | `docs/specs/`, `tests/` | 1-Click `python scripts/smoke_test.py`, `python -m pytest src/backend/tests src/db/tests`, `python scripts/verify_contracts.py`, `python scripts/verify_migrations.py`, `npm run typecheck` | Cấm tự ý sửa đổi logic nghiệp vụ trong `src/` |
| **Principal Code Reviewer**| `code-reviewer` | `pro` | `docs/specs/` | `git status --short`, `git diff --stat`, `git diff -- src/ docs/ ':!*package-lock.json' ':!*.lock'`, `git diff` | Cấm chạy lệnh sửa code, cấm tự commit hoặc đổi file cấu hình |
| **Release & Devops** | `release-engineer` / `devops-engineer` | `flash_lite` / `flash` | `dist/`, `scripts/`, `docker-compose.yml` | `python scripts/bundle_release.py`, `docker compose build`, `docker compose config` | Cấm sửa logic nghiệp vụ trong `src/` |
| **Tactical Agile Squad** | `fast-track-squad` | `flash` | `src/` (Trọng tâm) | `python scripts/verify_contracts.py`, `pytest`, `npm run typecheck`, `python scripts/snapshot.py` | Cấm xóa database, cấm phá vỡ Clean Architecture |

---

## 📝 2. Chi Tiết Thực Thi Từng Giai Đoạn

---

### Giai Đoạn 0: Tiếp Nhận Khách Hàng, Bóc Tách Scope & PRD
- **Tác tử thực thi**: `account-lead` (Model: `flash`), `lead-ba` (Model: `pro`), `uiux-designer` (Model: `flash`).
- **Nội dung thực hiện**:
  1. **Tiếp nhận prompt, Đặt Feature Slug & Định cỡ Tác vụ (Granular Feature Slicing)**:
     - Định danh ngắn gọn kebab-case (vd: `auth-flow`, `product-catalog`). Thư mục hồ sơ: `docs/specs/<feature-slug>/`.
     - **Định cỡ (T-Shirt Sizing)**:
       - *Atomic Feature (Size S/M)*: 1-3 user stories, tối đa 3-5 FRs, 1-2 DB models. Giữ nguyên làm 1 `<feature-slug>` duy nhất để phát triển ngay.
       - *Epic / Compound Feature (Size L/XL)*: Phân hệ lớn (> 5 FRs, nhiều domain aggregates như E-commerce, Quản lý kho, Thanh toán).
     - **Giao thức Bóc tách Epic (Epic Slicing Protocol)**:
       - **TUYỆT ĐỐI KHÔNG** dồn toàn bộ Epic vào 1 PRD duy nhất (gây phình token context và kéo dài vòng lặp phát triển).
       - `account-lead` và `lead-ba` chủ động phân rã Epic thành chuỗi các Feature Slugs nguyên tử độc lập (ví dụ: `order-checkout` -> `order-payment` -> `order-fulfillment`), thiết lập bảng **Ma Trận Bóc Tách Epic (Epic Decomposition Matrix)**, và ưu tiên lát cắt MVP (Phase 1 / P0) cho chu trình hiện tại:
         ```markdown
         | Lát cắt Feature Slug | Phạm vi & User Stories | Độ ưu tiên | Trạng thái triển khai |
         | :--- | :--- | :---: | :--- |
         | `<feature>-phase1-mvp` | Luồng nghiệp vụ cốt lõi P0 (Happy path) | P0 (MVP) | Đang thực hiện (Current Sprint) |
         | `<feature>-phase2-advanced` | Tính năng nâng cao, bộ lọc, phân quyền P1 | P1 | Backlog đợt tiếp theo |
         | `<feature>-phase3-analytics` | Báo cáo số liệu, xuất file, tích hợp ngoài P2 | P2 | v2.0 Roadmap |
         ```
  2. **Phỏng vấn Làm rõ (High-Leverage Requirements Elicitation)**:
     - `lead-ba` dùng `ask_question` đặt tối đa **1 đến 3 câu hỏi cốt lõi P0** mang tính sống còn đối với kiến trúc hoặc phạm vi (MVP Scope / Lát cắt bóc tách ưu tiên, Personas & Quyền hạn, Quy tắc nghiệp vụ rẽ nhánh chính).
     - Gom câu hỏi thành các phương án trắc nghiệm rõ ràng, luôn đánh dấu tiền tố `(Recommended)` ở phương án khuyến nghị tối ưu nhất.
     - **Nguyên tắc Phân tách Nghiệp vụ vs Tiểu tiết**: TUYỆT ĐỐI KHÔNG làm phiền người dùng bằng các câu hỏi vụn vặt (UI styling, tên cột DB, các edge cases kỹ thuật thứ yếu). Thay vào đó, BA chủ động đề xuất giải pháp tối ưu trực tiếp vào bản thảo PRD.
  3. **Thiết kế UI/UX Concept**:
     - `uiux-designer` vẽ sơ đồ điều hướng màn hình (Mermaid Navigation Flow), quy định Design Tokens (Primary, Secondary, Neutral), và ma trận 5 trạng thái giao diện (Default, Loading, Empty, Error, Success) tại `docs/specs/<feature-slug>/ui_ux_spec.md`.
  4. **Xuất bản PRD**:
     - `lead-ba` xuất bản `docs/specs/<feature-slug>/prd.md` đầy đủ: Mục tiêu SMART, Personas, Functional Requirements (FR), Business Rules (BR), Edge Cases, và Gherkin Acceptance Criteria.
- **🛡️ QUALITY GATE 1 (Client Sign-off)**:
  - Tech Lead xuất bản bản tóm tắt nghiệm thu. Người dùng duyệt (`APPROVED`), tiến trình tự động bước sang Giai đoạn 1.

---

### Giai Đoạn 1: Thiết Kế Kiến Trúc, Bảo Mật & Hợp Đồng Kỹ Thuật
- **Tác tử thực thi**: `system-architect` (Model: `pro`), `security-architect` (Model: `pro`), `tech-planner` (Model: `pro`).
- **Nội dung thực hiện**:
  1. **Thiết kế Hệ thống & Dữ liệu**:
     - `system-architect` phân tích PRD, xuất bản sơ đồ kiến trúc tổng thể, mô hình ERD cơ sở dữ liệu quan hệ (Entity-Relationship Mermaid).
  2. **Phân tích An toàn & Bảo mật (STRIDE Threat Model)**:
     - `security-architect` rà soát 6 nguy cơ STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) và định nghĩa ma trận RBAC/ABAC.
  3. **Thiết lập Kế hoạch & Hợp đồng Dữ liệu (Cross-Layer Contract Matrix & Uniform Casing)**:
     - `tech-planner` xuất bản `docs/specs/<feature-slug>/plan.md` chứa:
       - **Quy tắc Uniform Casing Convention**: 100% tên trường trong DB Column, Pydantic Schema và TypeScript Interface bắt buộc dùng `snake_case`. Cấm tuyệt đối camelCase trong API responses để triệt tiêu lỗi `undefined` tại runtime.
       - **Bảng Ánh Xạ Dữ Liệu 3 Tầng Chuẩn Hóa**: Bắt buộc định nghĩa tại Mục 2 của `plan.md` theo cấu trúc:
         `Trường Dữ Liệu | Kiểu DB (SQLAlchemy/PG) | Kiểu Backend (Pydantic v2) | Kiểu Frontend (TypeScript) | Nullable | Mặc định | Ràng buộc`
       - **Quy Chuẩn 4 Kiểu Dữ Liệu Xuyên Tầng Cốt Lõi**:
         - **UUID**: DB `Uuid(default=uuid.uuid4)` $\leftrightarrow$ Backend `UUID`/`str` $\leftrightarrow$ Frontend `string` (chuẩn RFC 4122).
         - **Timestamp**: DB `DateTime(timezone=True)` $\leftrightarrow$ Backend `datetime` (UTC) $\leftrightarrow$ Frontend `string` (ISO 8601 kết thúc bằng `Z`).
         - **Array**: DB `JSON(default=list)` $\leftrightarrow$ Backend `list[T]` $\leftrightarrow$ Frontend `T[]`.
         - **Enum**: Backend `StrEnum` $\leftrightarrow$ Frontend TypeScript `string literal union type` (ví dụ: `'PENDING' | 'CONFIRMED' | 'CANCELLED'`).
       - **REST API Specs**: HTTP Methods, Endpoints, Request Body, Response JSON, Error Schema `{"detail": "..."}`.
       - **Wave 1 Mock Fixtures**: Định nghĩa file mock data cho Frontend chạy độc lập trước khi có Live API.
- **🛡️ QUALITY GATE 2 (Architecture Sign-off)**:
  - Tech Lead và Reviewer thẩm định `plan.md`. Khi hợp đồng kỹ thuật nhất quán, chuyển sang Giai đoạn 2.

---

### Giai Đoạn 2: Rào Chắn An Toàn & Chuẩn Bị Môi Trường
- **Tác tử thực thi**: Tech Lead (Main Agent).
- **Nội dung thực hiện**:
  1. Kiểm tra biến môi trường `.env`.
  2. Kiểm tra thư viện và môi trường ảo Python (`.venv`) và Node.js (`node_modules`).
  3. Chạy smoke check nền tảng: `python -m ruff check src/` và kiểm tra cấu trúc thư mục.

---

### Giai Đoạn 3: Triển Khai Lập Trình Đợt Kép (2-Wave Pipelined Dev)
- **Tác tử thực thi**: Dev Squad (`db-dev`, `frontend-dev`, `backend-dev`, `devops-engineer`).
- **Quản lý Định danh Hội thoại (Squad Conversation Registry)**:
  - Tech Lead Orchestrator **BẮT BUỘC lưu lại Conversation ID** của từng squad:
    `SQUAD_REGISTRY = {"db-dev": conv_id_db, "frontend-dev": conv_id_fe, "backend-dev": conv_id_be, "devops-engineer": conv_id_do}`
  - Registry này được duy trì để định tuyến thông điệp sửa lỗi qua `send_message`, bảo toàn 100% ngữ cảnh hội thoại.
- **Nội dung thực hiện**:
  - **Wave 1 (Chạy song song)**:
    - `db-dev`: Tạo SQLAlchemy 2.0 Async Models tại `src/db/models/`, tạo migration revision Alembic tại `src/db/migrations/versions/`, repositories tại `src/db/repositories/`, và async seed data. Khi dùng mảng dữ liệu, dùng `from sqlalchemy import JSON` kèm variant PG để SQLite test không bị lỗi.
    - `frontend-dev`: Tạo TypeScript interfaces (chuẩn `snake_case` khớp 100% với `plan.md`), UI components, 5 trạng thái màn hình (Default, Loading, Empty, Error, Success), kết nối mock fixtures.
      - **Universal Typed API Client**: Tự động nhận diện SSR Server Component (`INTERNAL_API_URL`), Browser Web (`NEXT_PUBLIC_API_URL` / `VITE_API_URL`) và Mobile Android emulator loopback (`http://10.0.2.2:8000`). Hàm `clearClientApiCache()` dọn sạch cache an toàn khi thiếu Web Storage API trên Mobile.
  - **Wave Handshake Gate, Cảnh Báo Lệch Schema Sớm & Tối Ưu Tiến Độ Pipelined**:
    1. **Báo cáo Bàn giao Chuẩn hóa từ `db-dev` (`[HANDSHAKE-HANDOVER]`)**:
       Ngay khi hoàn tất models, repositories và migrations trong `src/db/`, `db-dev` bắt buộc gửi báo cáo bàn giao chuẩn hóa cho Tech Lead:
       ```text
       [HANDSHAKE-HANDOVER]
       - Feature: <feature-slug>
       - Squad: db-dev
       - Models Created: <danh sách các models đã tạo trong src/db/models/>
       - Contract Modified: TRUE | FALSE
       - Contract Changes: <chi tiết các trường/cột thay đổi so với plan.md, hoặc NONE>
       - Status: READY_FOR_HANDSHAKE
       ```
    2. **Kiểm tra Kỹ thuật Khách quan (Objective Smoke Check)**:
       Tech Lead Orchestrator thực hiện kiểm tra nhanh:
       ```bash
       python3 -m py_compile src/db/models/*.py
       .venv/bin/ruff check src/db/
       ```
       - Xác nhận `src/db/models/__init__.py` đã export các models mới sạch sẽ.
       - *Nếu phát hiện lỗi cú pháp hoặc import*: DỪNG LẠI, KHÔNG kích hoạt `backend-dev` mà gửi ngay `[SELF-HEALING ACTION REQUIRED]` qua `send_message` tới `SQUAD_REGISTRY["db-dev"]`.
    3. **Cơ Chế Phân Luồng & Cảnh Báo Lệch Schema Sớm (Early Drift Protocol)**:
       - **Trường hợp A: `Contract Modified: FALSE`**: Khớp 100% hợp đồng ban đầu. Tech Lead **KÍCH HOẠT NGAY `backend-dev` (Wave 2)** mà không cần chờ `frontend-dev` xong 100%. Backend chạy gối đầu song song với Frontend giúp rút ngắn 25-40% tổng thời gian phát triển.
       - **Trường hợp B: `Contract Modified: TRUE`**: Có sự thay đổi schema ở tầng DB.
         - Tech Lead cập nhật ngay `docs/specs/<feature-slug>/plan.md` (nâng version e.g. `1.1.0`, cập nhật Contract Matrix).
         - Tech Lead gửi ngay thông điệp `[CONTRACT-UPDATE NOTICE]` qua `send_message` tới `SQUAD_REGISTRY["frontend-dev"]` (đang chạy song song) để điều chỉnh giao diện tức thì.
         - *Tiếp nhận Bất đồng bộ*: `frontend-dev` hoàn tất thao tác nguyên tử dở dang, cập nhật TypeScript types và mock fixtures theo `plan.md v1.1.0`, rồi gửi phản hồi `[CONTRACT-ALIGNED]`.
         - *Pipelined Overlap*: Tech Lead không cần chờ Frontend xong mới bật Backend; Tech Lead kích hoạt ngay `backend-dev` (Wave 2) bám sát `plan.md v1.1.0`. Cả Backend và Frontend cùng tiến hành song song.
  - **Wave 2 (Kết nối Live API & Hạ tầng)**:
    - `backend-dev`: Tạo Pydantic v2 schemas (`snake_case`), Services xử lý logic nghiệp vụ, REST API routes tại `src/backend/app/api/v1/` kết nối trực tiếp với DB repositories. Cắm các endpoints vào `api_router` tập trung tại `src/backend/app/api/v1/router.py`. Expose cả `/health` và `/api/v1/health`.
    - `devops-engineer`: Cập nhật Dockerfile, `docker-compose.yml`, scripts khởi chạy.

  - **Bước Chốt Hội Tụ Đợt Kép Trước QA (Pre-QA Wave Convergence Gate & Cache Purge)**:
    *Áp dụng bắt buộc cho cả 2 trường hợp (Contract Modified TRUE hoặc FALSE) trước khi mở cổng Giai đoạn 4:*
    1. **Chốt Hội Tụ Tiến Độ (Dual-Squad Completion Sign-off)**:
       - Tech Lead CHỈ kích hoạt `qa-tester` khi **CẢ HAI** squad đều gửi báo cáo hoàn thành: `backend-dev` xong Live API endpoints và `frontend-dev` đã gửi token `[CONTRACT-ALIGNED]` kèm xác nhận typed API client đã kết nối Live routes.
    2. **Quy Trình Chuyển Đổi Mock $\to$ Live & Dọn Sạch Stale Cache Client**:
       - Cập nhật biến môi trường: Đặt `NEXT_PUBLIC_USE_MOCKS=false` trong file `.env`.
       - Xóa sạch Stale Cache: Typed API Client (`src/frontend/src/lib/api/client.ts`) áp dụng `cache: 'no-store'`, header `Cache-Control: 'no-cache'`, và gọi hàm `clearClientApiCache()` để xóa sạch toàn bộ storage/cache trên trình duyệt và thiết bị di động.
       - Kiểm tra mạng nhanh: Chạy `.venv/bin/python scripts/verify_network.py` để xác nhận Backend port 8000 và Frontend port 3000/5173 đã thông suốt.
    3. **Bảo toàn 100% Đồng bộ 3 Tầng**:
       - Toàn bộ 3 tầng Database $\leftrightarrow$ Backend $\leftrightarrow$ Frontend/Mobile được đồng bộ tuyệt đối trước khi bước vào kiểm thử tự động, triệt tiêu 100% rủi ro lỗi do lệch hợp đồng API hay stale cache.

---

### Giai Đoạn 4: Kiểm Thử Tự Động & Vòng Lặp Sửa Lỗi (QA Squad)
- **Tác tử thực thi**: `qa-tester` (Model: `flash`).
- **Nội dung thực hiện**:
  1. Thực thi quy trình kiểm thử 5 tầng:
     - **Tầng 1 - Linter**: `python -m ruff check src/`.
     - **Tầng 2 - Contract Synchronization**: `python scripts/verify_contracts.py <feature-slug>`.
     - **Tầng 3 - Migration DAG Integrity**: `python scripts/verify_migrations.py`.
     - **Tầng 4 - Backend & DB Tests**: `pytest src/backend/tests src/db/tests` (chạy trên SQLite in-memory async isolated fallback).
     - **Tầng 5 - Client Typecheck & E2E**: `npm --prefix src/frontend run typecheck` & `make test-e2e` (`run_e2e_tests.cjs`).
  2. **Kiểm thử trực quan giao diện & Slash Command `/browser`**:
     - Khởi động dev server: `python scripts/start_dev.py` (hoặc `python scripts/start_dev.py --check`).
     - Khuyến nghị Tech Lead/User kích hoạt phím tắt `/browser <URL_tính_năng>` trên khung chat Antigravity 2.0.
     - Thẩm định trực tiếp trên giao diện: kiểm tra đủ 5 trạng thái UI (`default`, `loading`, `empty`, `error`, `success`), tính responsive trên Mobile (375px) và Desktop (1280px).
     - Ghi nhận kết quả vào Mục 2.2 của `docs/specs/<feature-slug>/test-report.md`.
  3. Xuất bản `docs/specs/<feature-slug>/test-report.md`.
  4. **Vòng lặp Self-Healing & Quy Chuẩn Micro-Patch Ticket**:
     - Nếu bất kỳ tầng nào FAILED: Script `scripts/parse_traceback.py` cắt tỉa stacktrace còn 15-25 dòng trọng tâm.
     - QA Tester bóc tách phiếu lỗi thành **Micro-Patch Ticket**: chỉ rõ file và line range cụ thể (`file.py#L42-L55`), trích xuất 5-10 dòng code ngữ cảnh có đánh dấu `>>`, và **bắt buộc Dev Squad CHỈ dùng công cụ `replace_file_content`** để sửa đúng dòng vi phạm (tuyệt đối không viết lại toàn bộ file để tránh regression và giữ comments).
     - Dev sửa -> `qa-tester` chạy lại.
     - **Circuit Breaker**: Giới hạn tối đa 3 vòng lặp. Nếu quá 3 lần, dừng tiến trình và xin chỉ dẫn từ Tech Lead/User.

---

### Giai Đoạn 5: Thẩm Định Code, Tối Ưu & Bảo Mật (Review Squad)
- **Tác tử thực thi**: `code-reviewer` (Model: `pro`).
- **Nội dung thực hiện**:
  1. Kiểm tra diff tinh gọn qua `git status --short` và `git diff -- src/ docs/`.
  2. Đánh giá chất lượng dựa trên Scorecard chuẩn:
     - Tuân thủ Clean Architecture & phân tầng.
     - Nguy cơ N+1 queries (kiểm tra `selectinload`).
     - Lỗ hổng bảo mật OWASP (SQL injection, XSS, thiếu auth/RBAC).
     - Khả năng tiếp cận Accessibility (A11y) trên Frontend.
  3. Xuất bản `docs/specs/<feature-slug>/review-report.md`.
  4. Nếu `CHANGES_REQUESTED`: Dev Squad khắc phục -> QA kiểm thử lại -> Reviewer thẩm định lại (tối đa 3 vòng lặp).
- **🛡️ QUALITY GATE 3 (Production Readiness Sign-off)**:
  - Khi Verdict là `APPROVED` (Điểm $\ge 85/100$, 100% test pass), chuyển sang Giai đoạn 6.

---

### Giai Đoạn 6: Đóng Gói Phát Hành, Soạn Tài Liệu & Bàn Giao Khách Hàng
- **Tác tử thực thi**: `release-engineer` (Model: `flash_lite`), `tech-writer` (Model: `flash_lite`), `handover-lead` (Model: `flash`), Tech Lead.
- **Nội dung thực hiện**:
  1. `release-engineer`: Chạy `python scripts/bundle_release.py <feature-slug>`. Script tự động tạo gói `.zip` trong `dist/releases/`, xuất `RELEASE_MANIFEST.json` ghi nhận git SHA, danh sách file, dependencies.
  2. `tech-writer`: Soạn thảo `USER_MANUAL.md` (hướng dẫn sử dụng cho người dùng), `API_GUIDE.md` (cho lập trình viên đối tác), và `DEPLOYMENT.md` (hướng dẫn triển khai Docker/Cloud).
  3. `handover-lead`: Biên soạn `UAT_CHECKLIST.md` (danh sách kịch bản nghiệm thu cho khách hàng), hướng dẫn khách hàng kiểm tra sản phẩm với các lệnh 1-chạm (`make run`, `docker compose up`).
  4. Tech Lead tạo Git Conventional Commit (`feat(<slug>): complete implementation`), tạo git tag phiên bản (vd: `v1.0.0`), và gọi `manage_subagents(Action="kill_all")` để dọn dẹp sạch sẽ tài nguyên.

---

## 💬 3. Bộ Mẫu Thông Điệp Điều Phối Nội Bộ (Standard Dispatch Protocol)

Để đảm bảo thông tin điều phối giữa **Tech Lead (Main Agent)** và các **Subagents** luôn chính xác, không gây phình token context và tránh hiểu lầm phạm vi file, hệ thống quy chuẩn 4 mẫu thông điệp bắt buộc sau:

### Mẫu 1: Gửi từ Tech Lead khi QA FAILED (`[SELF-HEALING ACTION REQUIRED]`)
```text
[SELF-HEALING ACTION REQUIRED]
- Feature: <feature-slug>
- Iteration: <iteration_number> / 3
- Target Agent: db-dev (src/db/) | backend-dev (src/backend/) | frontend-dev (src/frontend/)
- Target File & Line: <đường_dẫn_file>#L...
- Failed Test ID: <mã test case hoặc tên hàm test>
- Diagnostics & Traceback:
  <dán nội dung traceback hoặc lỗi chi tiết từ Mục 4 test-report.md>
- Reproduction Command: <lệnh chạy lại để tái hiện lỗi>
- Instructions: Phân tích nguyên nhân và khắc phục triệt để. TUYỆT ĐỐI chỉ chỉnh sửa trong thư mục được phân quyền của bạn. Sau khi hoàn tất và smoke test sạch sẽ, gửi báo cáo [FIX-COMPLETED] để tiến hành kiểm thử lại.
```

### Mẫu 2: Gửi từ Tech Lead khi Review CHANGES_REQUESTED (`[REVIEW-FIX ACTION REQUIRED]`)
```text
[REVIEW-FIX ACTION REQUIRED]
- Feature: <feature-slug>
- Iteration: <iteration_number> / 3
- Target Agent: db-dev (src/db/) | backend-dev (src/backend/) | frontend-dev (src/frontend/)
- Finding ID: <REV-01, ...>
- Severity: [CRITICAL] | [MAJOR]
- Target File & Line: <đường_dẫn_file>#L...
- Issue Description & Diff:
  <trích xuất mô tả vi phạm và code diff từ Mục 3 review-report.md>
- Remediation Guidance: <hướng dẫn sửa đổi của reviewer>
- Instructions: Khắc phục đúng các điểm vi phạm trên trong thư mục phân quyền. Chạy smoke test và gửi báo cáo [FIX-COMPLETED] khi hoàn tất.
```

### Mẫu 3: Gửi từ Dev Squad khi Hoàn Tất Sửa Lỗi (`[FIX-COMPLETED]`)
```text
[FIX-COMPLETED]
- Feature: <feature-slug>
- Iteration: <iteration_number>
- Target Agent: <db-dev | backend-dev | frontend-dev>
- Modified Files: <danh sách files đã sửa>
- Contract Modified: TRUE | FALSE
- Contract Changes: <chi tiết thay đổi schema/endpoint nếu TRUE, hoặc NONE>
- Resolved Bug/Finding IDs: <BUG-01, REV-01, ...>
- Summary of Fix: <tóm tắt ngắn gọn giải pháp khắc phục và kết quả smoke test cục bộ>
```
*Lưu ý cho Tech Lead*: Nếu `Contract Modified: TRUE`, Tech Lead bắt buộc cập nhật lại `docs/specs/<feature-slug>/plan.md`, nâng `version` (e.g. `1.1.0`), đồng bộ lại Cross-Layer Data Contract Matrix và thông báo cho squad liên quan trước khi chạy lại QA.

### Mẫu 4: Báo Cáo Leo Thang Khi Kích Hoạt Circuit Breaker (`[CIRCUIT BREAKER ESCALATION]`)
```text
[CIRCUIT BREAKER ESCALATION]
- Feature: <feature-slug>
- Status: PAUSED_FOR_HUMAN_INTERVENTION
- Iterations Executed: 3 / 3
- Root Cause Summary: <tóm tắt lý do hệ thống không tự khắc phục được sau 3 lần lặp>
- Blocking Issues: <danh sách các bài test hoặc findings còn tắc nghẽn>
- Proposed Solutions: <đề xuất giải pháp cho PO / User xem xét can thiệp>
```

### Mẫu 5: Thông Báo Cập Nhật Hợp Đồng Cho Frontend (`[CONTRACT-UPDATE NOTICE]`)
```text
[CONTRACT-UPDATE NOTICE]
- Feature: <feature-slug>
- Schema Version: <new_version, ví dụ: 1.1.0>
- Changed Models: <tên model hoặc bảng bị thay đổi>
- Breaking Fields / Diff:
  • <field_cu>: <loại_cũ> -> <field_moi>: <loại_mới>
  • <field_bo_sung>: <loại_du_lieu>
- Target Layers Affected:
  • TypeScript Interfaces: src/frontend/src/types/<entity>.ts & src/mobile/src/types/<entity>.ts
  • Mock Fixtures: src/frontend/src/lib/api/mocks/<entity>_mock.ts
  • API Client: src/frontend/src/lib/api/client.ts
- Instructions: Tiếp tục thực thi Wave 1 nhưng cập nhật ngay types và mock fixtures theo spec mới. Chạy `npm run typecheck` và phản hồi [CONTRACT-ALIGNED] khi hoàn tất.
```

### Mẫu 6: Phản Hồi Xác Nhận Đồng Bộ Hợp Đồng Từ Frontend (`[CONTRACT-ALIGNED]`)
```text
[CONTRACT-ALIGNED]
- Feature: <feature-slug>
- Version: <phiên_bản_plan_mới>
- Squad: frontend-dev
- Updated Files:
  • src/frontend/src/types/<entity>.ts
  • src/mobile/src/types/<entity>.ts
  • src/frontend/src/lib/api/mocks/<entity>_mock.ts
- Typecheck Status: PASSED (0 errors)
- Status: ALIGNED_WITH_CONTRACT
```

---

## 📋 3b. Bảng Tiêu Chí Kiểm Tra Nhanh Chất Lượng (Quality Checklist)

Dùng bảng kiểm thử 12 tiêu chí này để thẩm định chất lượng mã nguồn và nghiệm thu tính năng trước khi chuyển sang pha Release:

- [ ] **1. Hoàn thiện Hồ sơ Hợp đồng**: `docs/specs/<feature-slug>/plan.md` có đầy đủ Metadata Header, Cross-Layer Data Contract Matrix, REST API Spec và UI Spec.
- [ ] **2. Thống nhất Casing `snake_case`**: Toàn bộ API payload, Pydantic DTOs và TypeScript Interfaces sử dụng thống nhất 100% chuẩn `snake_case`.
- [ ] **3. Kế thừa Mixins Chuẩn CSDL**: Model trong `src/db/models/` kế thừa `UUIDPrimaryKeyMixin` (`default=uuid.uuid4`) và `TimestampMixin` (`DateTime(timezone=True)`).
- [ ] **4. Triệt tiêu Truy vấn N+1**: Mọi truy vấn relationship trong `src/db/repositories/` đều được nạp kèm `selectinload()` hoặc `joinedload()`.
- [ ] **5. Xác thực Dữ liệu Phía Backend**: Endpoints FastAPI có Pydantic v2 validation giới hạn độ dài chuỗi (`min_length`, `max_length`), regex và khoảng giá trị số (`ge`, `le`).
- [ ] **6. Xử lý Trọn vẹn 5 Trạng thái UI**: Giao diện Client (Web / Mobile) xử lý đầy đủ 5 UI states: Default, Loading skeleton (chống CLS), Empty state (CTA thân thiện), Error alert (Retry CTA) và Success state.
- [ ] **7. Strict TypeScript**: Tuyệt đối không có từ khóa `any` trong toàn bộ mã nguồn TypeScript (`src/frontend/` và `src/mobile/`).
- [ ] **8. Linting & Formatting**: `python -m ruff check src/` trả về `All checks passed!` (0 lỗi).
- [ ] **9. Kiểm thử Tự động & Độ phủ**: `PYTHONPATH=src pytest src/backend/tests src/db/tests -v` đạt `100% passed` với tỷ lệ Code Coverage $\ge 80\%$.
- [ ] **10. Typecheck Client Không Lỗi**: `npm --prefix src/frontend run typecheck` (và mobile nếu có) không phát sinh lỗi compile/types.
- [ ] **11. Phê Duyệt Code Review**: `docs/specs/<feature-slug>/review-report.md` đạt Verdict `APPROVED` (điểm chất lượng $\ge 85/100$, 0 lỗi Critical/Major).
- [ ] **12. Chuẩn Hóa Git Commit**: Git commit được tạo theo đúng quy chuẩn Conventional Commits (ví dụ: `feat(booking): implement motorcycle booking flow`).

---

## 🩺 4. Cẩm Nang Xử Lý Sự Cố Kỹ Thuật (Troubleshooting Guide)

### Vấn đề 1: Pytest báo lỗi `aiosqlite is not installed` hoặc không tìm thấy module `backend`
* **Nguyên nhân**: Chạy lệnh pytest trần mà không chỉ định virtualenv hoặc thiếu `PYTHONPATH`.
* **Cách khắc phục**: Luôn chạy bằng lệnh chuẩn hóa:
  ```bash
  PYTHONPATH=src .venv/bin/pytest src/backend/tests -v
  ```
  hoặc gõ phím tắt `make test` / `.\run.ps1 test`.

### Vấn đề 2: Lỗi SQLite `CompileError: Compiler <...> can't render element of type ARRAY`
* **Nguyên nhân**: Model dùng kiểu `ARRAY` trần của PostgreSQL, khiến SQLite in-memory test không thể render bảng.
* **Cách khắc phục**:
  1. *Định nghĩa Model*: Chuyển sang dùng `from sqlalchemy import JSON` với `default=list` hoặc dùng variant:
     ```python
     from sqlalchemy import JSON, String
     from sqlalchemy.dialects.postgresql import ARRAY

     # Tương thích cross-DB tuyệt đối: SQLite dùng JSON, PostgreSQL dùng ARRAY
     tags: Mapped[list[str]] = mapped_column(
         JSON().with_variant(ARRAY(String), "postgresql"),
         default=list,
     )
     ```
  2. *Quy ước Viết Test Case Nâng Cao (Cross-DB Test Edge Cases)*:
     Khi test các tính năng độc quyền của PostgreSQL (`pgvector`, `tsvector` Full-Text Search, PostgreSQL native `ENUM`, `ARRAY` contains/overlap, `JSONB` path operators, Row Level Security - RLS):
     - Đánh dấu test case bằng `@pytest.mark.postgres_only` trong `src/backend/tests/`. Test này sẽ tự động chạy khi kết nối PostgreSQL thật và tự động bỏ qua (skip an toàn) khi chạy bộ test nhanh trên SQLite in-memory (`make test` / `make smoke`).
     - Đánh dấu `@pytest.mark.sqlite_compatible` cho các bài test dùng chung cả hai database.

### Vấn đề 3: Lỗi `MissingGreenlet` khi truy cập relationship trong FastAPI
* **Nguyên nhân**: Trong môi trường bất đồng bộ (`AsyncSession`), truy cập lazy-loading relationship mà không dùng `await`.
* **Cách khắc phục**: Tại tầng repository, luôn thêm `.options(selectinload(Model.relation_name))` vào câu lệnh `select()`.

### Vấn đề 4: Sandbox không có internet khi subagent chạy `npm/pip install`
* **Nguyên nhân**: Môi trường sandbox được cô lập để bảo mật.
* **Cách khắc phục**: Tuyệt đối không cho agent chạy lệnh cài đặt trần. Cập nhật tên thư viện vào `pyproject.toml` hoặc `src/frontend/package.json` và gắn cờ `[DEPENDENCY REQUIRED]`.

### Vấn đề 5: Lỗi Database Migration `Table already exists` khi khởi động hoặc chạy test
* **Nguyên nhân**: Bảng đã tồn tại trong database nhưng revision của Alembic chưa được đánh dấu (chưa stamp head).
* **Cách khắc phục**: Gọi module tự phục hồi `from src.backend.app.core.migration_manager import stamp_head; stamp_head()` hoặc chạy lệnh `make migrations` / `.\run.ps1 migrations`.

### Vấn đề 6: Supabase văng lỗi `prepared statement "__asyncpg_stmt_..." does not exist` khi chạy Alembic
* **Nguyên nhân**: Kết nối Alembic DDL migrations qua Supavisor Transaction Pooler (port `6543`). Transaction mode ngắt kết nối session sau mỗi lệnh và không hỗ trợ prepared statement của asyncpg.
* **Cách khắc phục**: Cấu hình `DIRECT_DATABASE_URL` trỏ trực tiếp vào Session Mode (port `5432`):
  `postgresql+asyncpg://postgres.[REF]:[PASS]@aws-0-[REGION].pooler.supabase.com:5432/postgres?ssl=require`.
  Đối với FastAPI App runtime (port `6543`), engine đã tự động đặt `prepared_statement_cache_size = 0`.

### Vấn đề 7: Next.js 15 Client hiển thị dữ liệu Mock cũ sau khi đã chuyển sang Live API
* **Nguyên nhân**: Router cache hoặc fetch cache của trình duyệt vẫn giữ response mock trước đó.
* **Cách khắc phục**: `src/frontend/src/lib/api/client.ts` đã được thiết lập `cache: 'no-store'` khi `isMockMode() === false`. Ngoài ra, gọi hàm `clearClientApiCache()` để dọn sạch sessionStorage/localStorage.

---

## ⚡ 5. Cẩm Nang Slash Commands Dành Cho Người Dùng (Antigravity 2.0 Shortcuts)

Trên giao diện Antigravity 2.0, **Slash Commands** là các phím tắt trực tiếp trên khung chat giúp người dùng (Product Owner / Developer) kích hoạt các chế độ tư duy và quy trình tự động hóa chuyên sâu. Tác tử AI không thể tự gõ lệnh này, nhưng Tech Lead Orchestrator sẽ chủ động gợi ý cho bạn sử dụng khi phù hợp với bối cảnh tác vụ.

### Bảng Ma Trận Ánh Xạ Slash Commands Theo Giai Đoạn Dự Án

| Lệnh Slash | Khi Nào Nên Sử Dụng? | Giai Đoạn Đội Dev Tương Ứng | Tác Dụng Cụ Thể Lên Hệ Thống |
| :--- | :--- | :--- | :--- |
| **`/grill-me`** | Bắt đầu ý tưởng mới, cần làm rõ phạm vi, phân quyền và quy tắc nghiệp vụ rẽ nhánh | **Giai đoạn 0: Discovery (`lead-ba`)** | Kích hoạt phiên phỏng vấn tương tác chuyên sâu. Lead BA sẽ chất vấn có cấu trúc để làm rõ các giả định ngầm, edge cases trước khi chốt `prd.md`. |
| **`/plan`** | Khi tính năng phức tạp, cần phân tích kiến trúc đa tầng trước khi viết mã | **Giai đoạn 1: Planning (`tech-planner`)** | Yêu cầu hệ thống lập kế hoạch chi tiết từng bước, khảo sát mã nguồn hiện hữu và hoàn thiện Ma trận hợp đồng 3 tầng `plan.md`. |
| **`/goal`** | Cần triển khai trọn vẹn một tính năng từ A $\to$ Z (chạy qua đêm / không ngắt quãng) | **Giai đoạn 3 $\to$ 6: Full Pipeline** | Đặt mục tiêu bền bỉ: Đội Dev tự động phối hợp qua 2 Wave, tự sửa lỗi qua QA & Review, không dừng lại cho đến khi đạt 100% test passed & review approved. |
| **`/boost`** | Bài toán thuật toán khó, thiết kế dữ liệu lớn hoặc kiến trúc phân tán | **Giai đoạn 1: Architecture (`system-architect`)** | Kích hoạt chu trình suy luận đa chiều (Deep Thinking & Multi-perspective) thẩm định rủi ro kỹ thuật. |
| **`/compact`** | Phiên làm việc kéo dài, context window bị đầy sau nhiều lượt lặp | **Sau Giai đoạn 4 hoặc 5 (Giữa các Wave)** | Tóm tắt lịch sử thảo luận, lưu lại trạng thái quan trọng vào `docs/specs/<slug>/` và giải phóng bộ nhớ đệm token. |
| **`/learn`** | Khi User điều chỉnh quy chuẩn code hoặc giải quyết một cấu hình đặc thù | **Bất kỳ lúc nào** | Ghi nhận hướng dẫn thành Rule vĩnh viễn trong `.agents/rules/` cho các phiên dev tiếp theo. |
| **`/schedule`** | Chạy kiểm thử định kỳ, sao lưu database hoặc đồng bộ trạng thái tự động | **Vận hành & Bảo trì** | Thiết lập cronjob hoặc timer chạy ngầm độc lập qua nền tảng Antigravity 2.0. |

### 5.2. Kịch Bản Sử Dụng Điển Hình (Practical Scenarios)

1. **Khởi động một Phân hệ Mới với BA & Bóc tách Epic**:
   * *Người dùng gõ*: `/grill-me Hãy cùng tôi thiết lập tính năng Quản lý Đơn hàng (Order Management)`
   * *Hiệu ứng*: Lead BA (`@lead-ba`) lập tức phân tích quy mô Epic, bóc tách thành các lát cắt nguyên tử (e.g. `order-checkout` $\rightarrow$ `order-payment`), đặt các câu hỏi trọng tâm P0 bằng công cụ `ask_question` về luồng trạng thái đơn hàng, phương thức thanh toán và phân quyền, sau đó xuất bản `docs/specs/<slug>/prd.md`.

2. **Chạy Tự Động Xuyên Suốt Tính Năng Đến Khi Bàn Giao**:
   * *Người dùng gõ*: `/goal Triển khai hoàn chỉnh tính năng order-management theo prd.md đã duyệt`
   * *Hiệu ứng*: Tech Lead kích hoạt Tech Planner $\rightarrow$ Wave 1 (DB + Frontend Mock) $\rightarrow$ Wave 2 (Backend Live API + DevOps) $\rightarrow$ QA Tester (5-Layer Smoke & Self-Healing) $\rightarrow$ Code Reviewer $\rightarrow$ Git Commit & Packaging. Đội dev kiên trì tự sửa lỗi cho đến khi hoàn tất 100%.

3. **Ghi Nhớ Quy Chuẩn Dự Án Đặc Thù**:
   * *Người dùng gõ*: `/learn Hãy luôn sử dụng asyncpg pool với Transaction Mode port 6543 cho FastAPI runtime và Session Mode port 5432 cho Alembic migrations`
   * *Hiệu ứng*: Antigravity lưu quy chuẩn này vào cấu hình workspace, đảm bảo mọi subagent trong tương lai luôn tuân thủ chính xác.

4. **Kiểm Tra Trực Quan Giao Diện & 5 Trạng Thái UI**:
   * *Người dùng gõ*: `/browser http://localhost:3000/orders Kiểm tra 5 trạng thái UI Loading, Empty, Error, Success, Default và độ co giãn mobile 375px`
   * *Hiệu ứng*: Antigravity mở trình duyệt truy cập route chỉ định, tương tác với các nút bấm, chụp ảnh màn hình kiểm chứng và hỗ trợ QA Tester đối chiếu trực quan với Acceptance Criteria.

5. **Thiết Kế Module Cốt Lõi, Thuật Toán Phức Tạp & Mô Hình Bảo Mật**:
   * *Người dùng gõ*: `/boost Thiết kế thuật toán phân bổ booking capacity và kiểm toán mô hình đe dọa STRIDE cho phân hệ đơn hàng`
   * *Hiệu ứng*: Kích hoạt chế độ Deep Thinking với mô hình mạnh nhất (`pro`), thẩm định toàn diện từ nhiều góc độ kiến trúc, rà soát vector tấn công OWASP Top 10 và lập ma trận rủi ro chi tiết trước khi sinh code.

6. **Trực Quan Hóa Sơ Đồ Phối Hợp Đội Dev Trước Khi Lập Trình**:
   * *Người dùng gõ*: `/teamwork-preview Cho tôi xem sơ đồ phân vai, quyền hạn thư mục và luồng dữ liệu 2 đợt của các subagent cho tính năng booking-flow`
   * *Hiệu ứng*: Antigravity trực quan hóa sơ đồ tương tác giữa `db-dev` (Wave 1), `frontend-dev` (Wave 1 mock fixtures), `backend-dev` (Wave 2 live API) và `qa-tester`, làm rõ các rào chắn file ownership để bạn duyệt trước khi bắt đầu.

---

## 🚀 6. Quy Trình Làn Chạy Cao Tốc (Track 2: Tactical Fast-Track SOP)

Khi gặp các tác vụ nhỏ, hotfixes, hoặc chỉnh sửa giao diện/endpoint cục bộ, không áp dụng quy trình 7 giai đoạn cồng kềnh mà chuyển sang **Fast-Track SOP**:

```text
[Yêu cầu bugfix / Micro-task]
            │
            ▼
[Bước 1: Phân tích phạm vi (make task TASK="...")]
            │ (Tự động nhận diện file bị ảnh hưởng & snapshot mã nguồn)
            ▼
[Bước 2: Triệu hồi @fast-track-squad]
            │ (Sửa đổi mã nguồn tối thiểu theo Clean Architecture)
            ▼
[Bước 3: Kiểm định trọng tâm (make fast-track-check)]
            │ (verify_contracts.py + PyTest)
            ▼
[Bước 4: Nghiệm thu & Lưu Checkpoint/Commit]
```

- **Lợi ích**: Tiết kiệm thời gian, bỏ qua Gate 1 & 2, giảm thiểu tiêu tốn token nhưng vẫn giữ vững chuẩn mã nguồn và rào chắn an toàn.

---

## ⚖️ 7. Chế Độ Điều Phối Tinh Gọn 7 Tác Tử (Lean Matrix 7-Agent Mode)

Kế thừa kiến trúc cốt lõi từ `AI-Team-Dev`, bên cạnh chế độ **Enterprise 5 Sub-Teams (15 Agents)** và **Tactical Fast-Track Squad**, `AI-Vibe-Coding` hỗ trợ thêm chế độ **Lean Matrix 7-Agent Mode**.

### 7.1. Khi Nào Nên Sử Dụng?
- Phù hợp cho các tính năng quy mô vừa (Medium-sized features): thêm 1 thực thể/nghiệp vụ mới vào codebase hiện hữu.
- Không cần họp duyệt qua 3 cổng HITL Gates cồng kềnh, nhưng vẫn đảm bảo quy trình 2-Wave Dev, Contract Matrix và kiểm thử khép kín.
- Tiết kiệm token và giảm thiểu số lượt chuyển giao (handoff turns) giữa các sub-teams.

### 7.2. Luồng Điều Phối 7 Tác Tử Hạt Nhân
```text
[Tech Lead Orchestrator]
       │
       ├──► Phase 0: BA Agent (`ba`, Model: "pro") -> docs/specs/<slug>/prd.md
       │
       ├──► Phase 1: Planner (`planner`, Model: "pro") -> docs/specs/<slug>/plan.md
       │
       ├──► Phase 2: Dev Squads (2-Wave Execution)
       │      ├── Wave 1 (Song song): `db-dev` (src/db/) + `frontend-dev` (src/frontend/, src/mobile/)
       │      ├── [Wave Handshake Gate]: Tech Lead kiểm tra schema & gửi [CONTRACT-UPDATE NOTICE] nếu có drift
       │      └── Wave 2: `backend-dev` (src/backend/ FastAPI nối DB live)
       │
       ├──► Phase 3: QA Tester (`qa-tester`, Model: "flash")
       │      └── Chạy smoke_test.py + verify_contracts.py (Self-Healing Loop max 3x)
       │
       ├──► Phase 4: Code Reviewer (`code-reviewer`, Model: "pro")
       │      └── Token-optimized Git Diff Audit & OWASP checklist (Review-Fix max 3x)
       │
       └──► Phase 5: Tech Lead Commit & Release
```

### 7.3. Cách Triệu Hồi Trên Chat Canvas (1-Line Direct Dispatch Matrix)
Lập trình viên có thể điều phối trực tiếp với 7 subagents qua Chat Canvas:

| Tác Tử Hạt Nhân | Model | Thư Mục Quyền Sở Hữu | Mẫu Câu Lệnh Vibe Coding 1-Dòng Trên Chat Canvas |
| :--- | :---: | :--- | :--- |
| **`@ba`** | `pro` | `docs/specs/<slug>/` | `@ba: /grill-me Phỏng vấn và xuất bản prd.md cho tính năng <tên_tính_năng>` |
| **`@planner`** | `pro` | `docs/specs/<slug>/` | `@planner: /plan Thiết lập Data Contract Matrix và REST API spec cho <tên_tính_năng>` |
| **`@db-dev`** | `inherit`| `src/db/` | `@db-dev: Tạo models SQLAlchemy 2.0 và sinh Alembic migration theo plan.md` |
| **`@backend-dev`** | `inherit`| `src/backend/` | `@backend-dev: Triển khai Clean Architecture service và FastAPI routes theo plan.md` |
| **`@frontend-dev`**| `inherit`| `src/frontend/`, `src/mobile/` | `@frontend-dev: Hoàn thiện màn hình và components xử lý đủ 5 trạng thái UI` |
| **`@qa-tester`** | `flash` | `tests/`, `docs/specs/` | `@qa-tester: Chạy smoke test, kiểm tra contract sync và xuất test-report.md` |
| **`@code-reviewer`**| `pro` | `docs/specs/` | `@code-reviewer: Thẩm định git diff tối ưu token và chấm điểm review-report.md` |

---

## 🔄 8. Quy Trình Đồng Bộ Hai Chiều Mã Nguồn Sửa Thủ Công & SDLC Checkpoint (`make sync`)

Trong quá trình phát triển, khi lập trình viên trực tiếp can thiệp chỉnh sửa code (Manual Edit) hoặc yêu cầu AI sửa code tự do qua Chat Canvas (`@dev-squad`, `@backend-dev`, `@frontend-dev`), trạng thái thực tế của mã nguồn trên đĩa có thể đi trước hoặc lệch so với trạng thái lưu trong SDLC State Machine / Checkpoints.

Để bảo đảm tính toàn vẹn 100%, quy trình vận hành chuẩn (SOP) quy định:

```text
[Lập trình viên sửa code thủ công trong src/ hoặc workspaces/]
                       │
                       ▼
            [Chạy: make sync PROJECT="..."]
                       │
  ┌────────────────────┴────────────────────┐
  ▼                                         ▼
[1. Quét AST cây mã nguồn]         [2. Chạy PyTest & Alembic Check]
  │                                         │
  └────────────────────┬────────────────────┘
                       ▼
       [3. Tự phát hiện SDLC Phase hiện tại]
                       ▼
       [4. Cập nhật test_summary.json]
                       ▼
[5. Ghi đè trạng thái sạch vào Checkpoint JSON]
                       │
                       ▼
    [Sẵn sàng cho `make resume` tiếp nối an toàn]
```

### Các bước thực hiện:
1. **Sau khi hoàn tất sửa đổi mã nguồn**, chạy ngay:
   ```bash
   make sync PROJECT="MotoCare_Upgrade"
   # Hoặc trên Windows PowerShell:
   .\run.ps1 sync
   ```
2. **Hệ thống State Synchronizer (`scripts/sync_state.py`) tự động thực hiện**:
   - Quét toàn bộ cây thư mục mã nguồn và artifacts.
   - Chạy Pytest backend và kiểm tra tính toàn vẹn của Alembic migrations (Zero Schema Drift Policy).
   - Kiểm tra syntax AST của Frontend và quét rà soát Secret leaks.
   - Tự động nhận diện Phase hiện tại (`DISCOVERY` $\rightarrow$ `ARCHITECTURE` $\rightarrow$ `ENGINEERING` $\rightarrow$ `QA` $\rightarrow$ `RELEASE`).
   - Cập nhật chỉ số vào `test_summary.json` và đồng bộ ngược vào file Checkpoint JSON (`dist/checkpoints/` hoặc `workspaces/checkpoints/`).
3. **Kết quả**: Khi tiếp tục phiên làm việc bằng `make resume` hoặc `python scripts/runner.py --resume`, hệ thống sẽ tiếp nối chính xác từ trạng thái mã nguồn bạn vừa sửa mà không bị ghi đè hay mất dữ liệu.
- `@frontend-dev: Xây dựng UI components và TypeScript types theo plan.md`
- `@backend-dev: Viết FastAPI router, Pydantic schemas và service kết nối db`
- `@qa-tester: Chạy kiểm thử tự động 5 tầng và báo cáo lỗi nếu có`
- `@code-reviewer: Audit git diff tối ưu token và chấm điểm chất lượng mã nguồn`
