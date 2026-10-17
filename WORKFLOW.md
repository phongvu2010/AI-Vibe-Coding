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

## 📝 2. Chi Tiết Thực Thi Từng Giai Đoạn

---

### Giai Đoạn 0: Tiếp Nhận Khách Hàng, Bóc Tách Scope & PRD
- **Tác tử thực thi**: `account-lead` (Model: `flash`), `lead-ba` (Model: `pro`), `uiux-designer` (Model: `flash`).
- **Nội dung thực hiện**:
  1. **Đặt Feature Slug & Đánh giá quy mô**:
     - Định danh ngắn gọn kebab-case (vd: `auth-flow`, `product-catalog`). Thư mục hồ sơ: `docs/specs/<feature-slug>/`.
     - Phân loại: *Atomic Feature* (Size S/M, 1-3 stories) triển khai ngay; *Epic Feature* (Size L/XL) bóc tách thành chuỗi các feature slugs cuốn chiếu, chọn lát cắt MVP (P0) cho chu kỳ hiện tại.
  2. **Phỏng vấn Làm rõ (High-Leverage Requirements Elicitation)**:
     - `lead-ba` dùng `ask_question` đặt tối đa **1 đến 3 câu hỏi cốt lõi P0** (về phạm vi MVP, đối tượng phân quyền, quy tắc nghiệp vụ rẽ nhánh). Gom câu hỏi thành các phương án trắc nghiệm có đề xuất `(Recommended)`.
     - Không hỏi các tiểu tiết kỹ thuật (tên cột DB, màu nút bấm).
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
  3. **Thiết lập Kế hoạch & Hợp đồng Dữ liệu (Cross-Layer Contract Matrix)**:
     - `tech-planner` xuất bản `docs/specs/<feature-slug>/plan.md` chứa:
       - **Bảng Ánh Xạ Dữ Liệu 3 Tầng**: Tên trường (`snake_case`), kiểu dữ liệu DB (SQLAlchemy) $\leftrightarrow$ Backend (Pydantic v2) $\leftrightarrow$ Frontend/Mobile (TypeScript).
       - **REST API Specs**: HTTP Methods, Endpoints, Request Body, Response JSON, Error Schema `{"detail": "..."}`.
       - **Wave 1 Mock Fixtures**: Định nghĩa file mock data cho Frontend.
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
- **Nội dung thực hiện**:
  - **Wave 1 (Chạy song song)**:
    - `db-dev`: Tạo SQLAlchemy 2.0 Async Models tại `src/db/models/`, tạo migration revision Alembic tại `src/db/migrations/versions/`, repositories tại `src/db/repositories/`, và async seed data.
    - `frontend-dev`: Tạo TypeScript interfaces (chuẩn `snake_case` khớp 100% với `plan.md`), UI components, 5 trạng thái màn hình (Default, Loading, Empty, Error, Success), kết nối mock fixtures.
  - **Handshake Gate**:
    - Tech Lead kiểm tra biên dịch cú pháp Python models: `python -m py_compile src/db/models/*.py`.
    - Kiểm tra typecheck TypeScript: `npm --prefix src/frontend run typecheck`.
  - **Wave 2 (Kết nối Live API & Hạ tầng)**:
    - `backend-dev`: Tạo Pydantic v2 schemas (`snake_case`), Services xử lý logic nghiệp vụ, REST API routes tại `src/backend/app/api/v1/` kết nối trực tiếp với DB repositories. Chuyển Frontend từ Mock sang Live API.
    - `devops-engineer`: Cập nhật Dockerfile, `docker-compose.yml`, scripts khởi chạy.

---

### Giai Đoạn 4: Kiểm Thử Tự Động & Vòng Lặp Sửa Lỗi (QA Squad)
- **Tác tử thực thi**: `qa-tester` (Model: `flash`).
- **Nội dung thực hiện**:
  1. Thực thi quy trình kiểm thử 5 tầng:
     - **Tầng 1 - Linter**: `python -m ruff check src/`.
     - **Tầng 2 - Contract Synchronization**: `python scripts/verify_contracts.py <feature-slug>`.
     - **Tầng 3 - Migration DAG Integrity**: `python scripts/verify_migrations.py`.
     - **Tầng 4 - Backend & DB Tests**: `pytest src/backend/tests src/db/tests` (chạy trên SQLite in-memory async isolated fallback).
     - **Tầng 5 - Client Typecheck**: `npm --prefix src/frontend run typecheck` & `npm --prefix src/mobile run typecheck`.
  2. Xuất bản `docs/specs/<feature-slug>/test-report.md`.
  3. **Vòng lặp Self-Healing**:
     - Nếu bất kỳ tầng nào FAILED: Script `scripts/parse_traceback.py` cắt tỉa stacktrace còn 15-25 dòng trọng tâm.
     - Tech Lead gửi chỉ thị sửa lỗi cho Dev Squad. Dev sửa -> `qa-tester` chạy lại.
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
