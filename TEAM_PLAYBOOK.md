# 📘 DEVELOPER TEAM PLAYBOOK — HƯỚNG DẪN THỰC CHIẾN AI SOFTWARE HOUSE
### Nền tảng: Google Antigravity 2.0 | Mô hình: Disciplined Vibe Coding (Dual-Track SDLC)

Chào mừng toàn thể Tech Lead, Product Owner (PO), Kỹ sư phần mềm và QA gia nhập không gian làm việc **AI-Vibe-Coding**.

Tài liệu này là cẩm nang thực chiến giúp đội ngũ lập trình phối hợp nhịp nhàng với **15 AI Agents thuộc 5 Sub-Teams** theo chu trình SDLC khép kín, kết hợp tối đa sức mạnh của **Slash Commands** trên nền tảng Antigravity 2.0.

---

## 🧭 1. Triết Lý "Disciplined Vibe Coding"

**Vibe Coding** là phương thức phát triển phần mềm mà lập trình viên tương tác với AI bằng ngôn ngữ tự nhiên để hiện thực hóa ý tưởng với tốc độ tối đa.

Tuy nhiên, nếu không có kỷ luật, Vibe Coding sẽ tạo ra "mã nguồn rác" (unmaintainable code). Tại **AI-Vibe-Coding**, chúng ta áp dụng 4 nguyên tắc sắt:
1. **AI làm việc theo Phân vai & SDLC:** Không dùng 1 prompt dài để sinh toàn bộ dự án. Dự án được phân rã qua 5 Sub-Teams chuyên môn hóa.
2. **Kiểm soát bằng 3 Chốt chặn Con người (Quality Gates):** Con người giữ quyền duyệt PRD, duyệt kiến trúc và cấp phép phát hành; AI tự chủ viết code và test.
3. **Mã nguồn in-place chuẩn Clean Architecture:** Phân tầng triệt để trong `src/` (`models` -> `schemas` -> `repositories` -> `services` -> `routers`), casing đồng bộ `snake_case` 100%.
4. **Kiểm thử thực tế 5 tầng (Zero Hallucination):** Toàn bộ test case phải chạy qua lệnh thật (`pytest`, `verify_contracts.py`, `verify_migrations.py`, và `run_e2e_tests.cjs`).

---

## 🏛️ 2. Phân Vai 5 Sub-Teams & Cách Triệu Hồi Kết Hợp Slash Commands

Bạn có thể triệu hồi trực tiếp các Sub-Teams qua **Chat Canvas** của Antigravity 2.0:

```text
[Khách hàng / PO: Brief yêu cầu]
         │
         ▼
1. @discovery-squad (hoặc @discovery_team)  ➔ Bóc tách PRD, Gherkin Stories, UI/UX Concept
         ▼
   [GATE 1: Phê duyệt PRD trên review_gate_1_prd.md]
         │
         ▼
2. @architecture-squad (hoặc @architecture_team) ➔ OpenAPI, ERD, STRIDE Threat Model, Plan
         ▼
   [GATE 2: Ký duyệt API & Kiến trúc trên review_gate_2_architecture.md]
         │
         ▼
3. @dev-squad (hoặc @engineering_team) ➔ 2-Wave Dev: DB (SQLAlchemy) + Frontend (Web/Mobile) -> Backend (FastAPI)
         ▼
4. @qa-squad (hoặc @qa_team) ➔ PyTest, Contract Sync, Headless E2E, Self-Healing Loop
         ▼
   [GATE 3: Cấp phép Triển khai trên review_gate_3_deploy.md]
         │
         ▼
5. @release-squad (hoặc @release_team) ➔ Đóng gói Release ZIP, Manifest, UAT Checklist, User Manual
```

### Cú pháp gọi Sub-Teams & Gắn kết Slash Commands trong Chat Canvas:

- **Khởi tạo yêu cầu (@discovery-squad / @discovery_team):**
  - `@discovery-squad: /grill-me Phỏng vấn tôi để làm rõ các điểm mù và mâu thuẫn nghiệp vụ trong file @examples/sample_client_brief.md.`
  - `@discovery-squad: /plan Bóc tách phạm vi In-Scope MVP và tạo User Stories chuẩn Gherkin.`
- **Thiết kế kiến trúc (@architecture-squad / @architecture_team):**
  - `@architecture-squad: /plan Thiết kế OpenAPI 3.0 và Mermaid ERD bám sát Tech Lead Profile.`
  - `@architecture-squad: /boost Thực hiện phân tích mô hình an ninh bảo mật STRIDE và phân quyền RBAC/ABAC.`
- **Phát triển tính năng (@dev-squad / @engineering_team):**
  - `@dev-squad: /plan Lập trình phân tầng Clean Architecture theo kế hoạch 2-Wave Execution.`
  - `@dev-squad: /goal Hoàn thiện mã nguồn Database Models, Web/Mobile UI và Backend FastAPI endpoints.`
- **Kiểm định chất lượng (@qa-squad / @qa_team):**
  - `@qa-squad: /boost Chạy bộ kiểm thử 5 tầng: Pytest, Contract Synchronizer, Alembic DAG và Headless E2E.`
  - `@qa-squad: Tự động kích hoạt Self-Healing Loop cắt tỉa traceback nếu phát hiện test case thất bại.`
- **Bàn giao phát hành (@release-squad / @release_team):**
  - `@release-squad: /goal Đóng gói bản release v1.0.0 kèm UAT Checklist và RELEASE_MANIFEST.json.`
- **Thực thi nhanh Micro-Tasks (@fast-track-squad / @fast_track_team):**
  - `@fast-track-squad: /plan Bổ sung endpoint GET /api/v1/orders/filter theo status và viết unit test tương ứng.`
  - `@fast-track-squad: /goal Sửa lỗi format số điện thoại và cập nhật TypeScript types đồng bộ.`

### 💬 2b. Cẩm Nang Gọi Trực Tiếp 7 Tác Tử Hạt Nhân (1-Line Direct Dispatch — Kế thừa AI-Team-Dev)

Khi cần thực hiện tác vụ nguyên tử, tinh gọn trên từng tầng mà không cần kích hoạt cả Sub-Team, bạn có thể gọi trực tiếp 7 tác tử chuyên trách:

| Tác Tử Hạt Nhân | Model | Thư Mục Phân Quyền | Mẫu Câu Lệnh Vibe Coding 1-Dòng (Direct Invocation) |
| :--- | :---: | :--- | :--- |
| **`@ba`** | `pro` | `docs/specs/<slug>/` | *"Nhờ `@ba` phỏng vấn (`/grill-me`) và soạn thảo PRD cho phân hệ Giỏ hàng."* |
| **`@planner`** | `pro` | `docs/specs/<slug>/` | *"Nhờ `@planner` (`/plan`) thiết kế Cross-Layer Contract Matrix và REST API cho phân hệ Sản phẩm."* |
| **`@db-dev`** | `inherit`| `src/db/` | *"Nhờ `@db-dev` thêm trường `thumbnail_url` vào bảng `categories` và tạo Alembic migration."* |
| **`@backend-dev`** | `inherit`| `src/backend/` | *"Nhờ `@backend-dev` viết service và endpoint lọc danh mục sản phẩm theo status."* |
| **`@frontend-dev`**| `inherit`| `src/frontend/`, `src/mobile/` | *"Nhờ `@frontend-dev` hoàn thiện component CategoryCard xử lý trọn vẹn 5 trạng thái UI."* |
| **`@qa-tester`** | `flash` | `tests/`, `docs/specs/` | *"Nhờ `@qa-tester` kiểm tra lint (`ruff`) và chạy bộ kiểm thử Pytest trên SQLite in-memory."* |
| **`@code-reviewer`**| `pro` | `docs/specs/` | *"Nhờ `@code-reviewer` audit bảo mật và chấm điểm chất lượng mã nguồn qua `git diff`."* |

> 💡 **Quản Lý Hội Thoại Dài Hạn (Squad Registry & Conversation ID Tracking)**:
> Khi kích hoạt các tác tử, Tech Lead Orchestrator lưu lại `conversationId` vào `SQUAD_REGISTRY = {"db-dev": conv_id_db, "frontend-dev": conv_id_fe, "backend-dev": conv_id_be, ...}`. Trong các vòng lặp phản hồi sửa lỗi hoặc bổ sung tính năng, Tech Lead gửi chỉ thị qua `send_message(Recipient=conv_id)` để tác tử tái sử dụng 100% ngữ cảnh hội thoại và lịch sử file cũ, tránh gọi lại `invoke_subagent` làm mất memory.

### 💻 2c. Triệu Hồi Native Sub-Team Qua Terminal Dispatcher (CLI Dispatcher)

Ngoài Chat Canvas, bạn có thể gọi trực tiếp từng Sub-Team độc lập từ dòng lệnh hoặc script tự động hóa:

```bash
# Xem danh sách tất cả Sub-Teams kèm Model Tier và kỹ năng:
python -m orchestrator.agent_factory --list

# Xem ma trận phân bổ mô hình AI & hệ số chi phí token:
python -m orchestrator.agent_factory --models

# Triệu hồi trực tiếp 1 Sub-Team bằng CLI với prompt cụ thể:
python -m orchestrator.agent_factory --subteam discovery_team --prompt "Phân tích brief @examples/sample_client_brief.md" --project "MotoCare"
python -m orchestrator.agent_factory --subteam engineering_team --role backend_dev --prompt "Viết CRUD User và Auth middleware" --project "MotoCare"
```

---

## ⚡ 3. Bảng Tra Cứu Lệnh Nhanh (Developer Command Cheat Sheet)

| Lệnh | Ý Nghĩa & Mục Đích |
| :--- | :--- |
| `make help` | Hiển thị menu hướng dẫn tất cả các lệnh khả dụng |
| `make setup` | **Khởi tạo virtualenv `.venv` và cài đặt dependencies tự động** |
| `make dev` | Khởi chạy Backend FastAPI (Uvicorn live-reload tại `http://localhost:8000`) |
| `make dev-backend` | Chạy Backend kèm các biến môi trường phát triển |
| `make dev-mock` | Chạy Mock API Server phục vụ phát triển Frontend độc lập |
| `make task TASK="Mô tả"` | **[Track 2] Thực thi tác vụ nhanh bằng Fast-Track Squad (Bỏ qua Gate 1 & 2)** |
| `make fast-track` | Alias của lệnh `make task` |
| `make checkpoint PHASE=...` | **Lưu Checkpoint trạng thái SDLC kèm bản chụp mã nguồn sạch (< 1s)** |
| `make resume` | Khôi phục và tiếp tục phiên làm việc SDLC từ Checkpoint gần nhất |
| `make restore ID=...` | Khôi phục mã nguồn về một Checkpoint lịch sử cụ thể |
| `make test` | Chạy toàn bộ Pytest trên SQLite async in-memory cô lập |
| `make test-cov` | Chạy Pytest kèm đo độ phủ mã nguồn (Coverage $\ge 80\%$) |
| `make test-db` | **Chạy kiểm thử Database & tính toàn vẹn Alembic Migrations DAG** |
| `make test-frontend-e2e` | **Chạy kiểm thử Frontend Headless E2E Simulation (`run_e2e_tests.cjs`)** |
| `make test-all` | Thực thi toàn bộ kiểm thử (Backend Pytest, DB, Frontend E2E, Contract Sync) |
| `make smoke` | Chạy bộ kiểm thử tự động 5 tầng chẩn đoán hệ thống (`smoke_test.py`) |
| `make contracts` | **Thẩm định tính đồng bộ hợp đồng dữ liệu 3 chiều (DB $\leftrightarrow$ Backend $\leftrightarrow$ Frontend)** |
| `make migrations` | Kiểm tra toàn vẹn cú pháp AST và đồ thị Alembic Migrations |
| `make typecheck` | Kiểm tra kiểu dữ liệu TypeScript Web Frontend (Strict mode) |
| `make typecheck-mobile`| Kiểm tra kiểu dữ liệu TypeScript Mobile React Native Expo |
| `make preset-vite` | **Chuyển đổi Web Client sang React + Vite (SPA / Dashboard siêu nhanh)** |
| `make preset-nextjs` | **Chuyển đổi Web Client sang Next.js 15 (App Router / SSR / SEO)** |
| `make add-mobile` | **Khởi tạo ứng dụng Mobile React Native Expo (NativeWind v4 Tailwind)** |
| `make release` | Đóng gói bản phát hành (.zip, checksum, manifest, UAT checklist) |
| `make docker-up` | Khởi chạy hạ tầng qua Docker Compose (Web, FastAPI, PostgreSQL) |

---

## 🔄 4. Quy Trình Vận Hành Hai Làn (Dual-Track SDLC)

### 📌 Làn 1: Enterprise Full-Lifecycle SDLC (Dự án mới & Tính năng lớn)
1. Khách hàng/PO nhập đề bài vào Chat Canvas (hoặc trỏ `@examples/sample_client_brief.md`).
2. `@discovery-squad` phỏng vấn qua `ask_question`, xuất bản `prd.md` và `ui_ux_spec.md`.
3. PO kiểm tra và duyệt **Gate 1** $\rightarrow$ Lưu `make checkpoint PHASE=gate_1_prd`.
4. `@architecture-squad` xuất bản `plan.md` với Data Contract Matrix $\rightarrow$ Duyệt **Gate 2**.
5. `@dev-squad` thực thi 2-Wave: DB & Frontend UI $\rightarrow$ Handshake $\rightarrow$ Backend APIs $\rightarrow$ **Pre-QA Wave Convergence Gate** (Chốt hội tụ cả 2 squads, gạt cờ `NEXT_PUBLIC_USE_MOCKS=false`, kích hoạt `clearClientApiCache()` dọn sạch cache client và chạy `verify_network.py`).
6. `@qa-squad` chạy `make test-all` và thẩm định code diff qua scorecard $\rightarrow$ Duyệt **Gate 3**.
7. `@release-squad` đóng gói bản release `.zip` và cung cấp hướng dẫn nghiệm thu 1-chạm.

### 📌 Làn 2: Tactical Fast-Track SDLC (Bugfixes & Micro-Tasks hàng ngày)
- Dành cho các chỉnh sửa cục bộ, hotfix hoặc thêm 1-2 components nhỏ.
- Chạy trực tiếp qua:
  ```bash
  make task TASK="Thêm trường avatar_url vào User profile và cập nhật giao diện"
  ```
- Hoặc triệu hồi trong chat: `@fast-track-squad: Sửa lỗi validate email trên form đăng ký.`

---

## 💬 4b. Giao Thức Điều Phối Thông Điệp & Ngắt Mạch (Circuit Breaker)

Khi phối hợp giữa Tech Lead và các AI Subagents, bắt buộc sử dụng các định dạng thông điệp có cấu trúc để tránh hiểu lầm và kiểm soát vòng lặp lỗi:

### Mẫu 1: Chỉ thị sửa lỗi khi QA thất bại (`[SELF-HEALING ACTION REQUIRED]`)
```text
[SELF-HEALING ACTION REQUIRED]
- Feature: <feature-slug>
- Iteration: <iteration_number> / 3
- Target Agent: db-dev (src/db/) | backend-dev (src/backend/) | frontend-dev (src/frontend/)
- Target File & Line: <đường_dẫn_file>#L...
- Failed Test ID: <tên hàm test hoặc mã lỗi>
- Diagnostics & Traceback:
  <dán nội dung traceback cắt tỉa 15-25 dòng>
- Instructions: Phân tích nguyên nhân và khắc phục triệt để trong phạm vi quyền hạn.
```

### Mẫu 2: Phản hồi hoàn tất sửa lỗi từ Dev Squad (`[FIX-COMPLETED]`)
```text
[FIX-COMPLETED]
- Feature: <feature-slug>
- Iteration: <iteration_number>
- Target Agent: <db-dev | backend-dev | frontend-dev>
- Modified Files: <danh sách files đã sửa>
- Contract Modified: TRUE | FALSE
- Resolved Finding IDs: <BUG-01, REV-01, ...>
- Summary of Fix: <tóm tắt ngắn gọn giải pháp và kết quả test cục bộ>
```

### Mẫu 3: Báo cáo leo thang ngắt mạch khi quá 3 lần lặp (`[CIRCUIT BREAKER ESCALATION]`)
```text
[CIRCUIT BREAKER ESCALATION]
- Feature: <feature-slug>
- Status: PAUSED_FOR_HUMAN_INTERVENTION
- Iterations Executed: 3 / 3
- Root Cause Summary: <tóm tắt lý do hệ thống không tự khắc phục được sau 3 lần lặp>
- Blocking Issues: <danh sách các bài test hoặc findings còn tắc nghẽn>
- Proposed Solutions: <đề xuất giải pháp cụ thể cho Tech Lead / PO xem xét can thiệp>
```
*Quy tắc ngắt mạch*: Khi nhận được thông điệp này, AI lập tức dừng vòng lặp tự sửa, bảo vệ an toàn mã nguồn hiện tại và nhường quyền quyết định cho con người.

---

## 🔄 4c. Quy Trình Đồng Bộ Ngược Hợp Đồng (Reverse Contract Sync Protocol)

Trong chu trình phát triển (đặc biệt tại Wave 1 và Wave 2), nếu kỹ sư phát hiện mô hình dữ liệu thực tế cần bổ sung hoặc điều chỉnh (ví dụ: thêm cột trạng thái, thay đổi kiểu dữ liệu, thêm tham số lọc), **TUYỆT ĐỐI CẤM** tự ý sửa code một mình gây lệch pha (*Schema Drift / Contract Desync*).

**Quy trình 4 bước bắt buộc**:
1. **Báo cáo Lệch Hợp Đồng**: Dev Squad gửi thông điệp `[FIX-COMPLETED]` hoặc `[HANDSHAKE-HANDOVER]` kèm cờ `Contract Modified: TRUE` và chi tiết các trường thay đổi gửi Tech Lead.
2. **Cập nhật Single Source of Truth**: Tech Lead triệu hồi `tech-planner` (hoặc `planner`) cập nhật lại `docs/specs/<feature-slug>/plan.md` (nâng version e.g. `1.0.0` $\to$ `1.1.0`, cập nhật bảng *Cross-Layer Data Contract Matrix* và *REST API Specifications*).
3. **Phát lệnh Cập nhật Xuống Tầng Dưới**: Tech Lead gửi thông điệp `[CONTRACT-UPDATE NOTICE]` tới các squads liên quan (`frontend-dev` cập nhật TypeScript interfaces & mock fixtures; `db-dev` tạo migration revision tương ứng).
4. **Kiểm Định Khách Quan**: Chạy công cụ kiểm tra tự động `make contracts` (`python scripts/verify_contracts.py`) và `make migrations` (`python scripts/verify_migrations.py`) để xác nhận 100% 3 tầng (Database $\leftrightarrow$ Backend $\leftrightarrow$ Frontend/Mobile) đã đồng bộ hoàn toàn trước khi chuyển sang pha QA.

---

## 🎯 5. Tiêu Chuẩn Hoàn Thành (Definition of Done - DoD)
Trước khi bàn giao thành phẩm cho khách hàng:
- [ ] 100% Quality Gates đã được phê duyệt.
- [ ] `make test-all` vượt qua 100% test cases (Zero failures).
- [ ] `make contracts` xác nhận 100% tên trường và kiểu dữ liệu đồng bộ `snake_case`.
- [ ] Không có hardcoded secrets hoặc credentials trong mã nguồn.
- [ ] Bản phát hành `.zip` và `RELEASE_MANIFEST.json` đã được tạo trong `dist/releases/`.
- [ ] Bảng kiểm `UAT_CHECKLIST.md` đã sẵn sàng để khách hàng nghiệm thu một chạm.

---

## 📐 6. Tiêu Chuẩn Phân Tầng Clean Architecture

### 1. Phân tầng Backend (Python / FastAPI)
Mọi mã nguồn Backend tại `src/backend/` hoặc `workspaces/output_project/` phải tuân thủ nghiêm ngặt 5 tầng độc lập:
- **`core/`**: Cấu hình hệ thống nạp từ `.env` (`config.py`), kết nối DB Engine & Session Provider (`database.py`).
- **`models/`**: SQLAlchemy 2.0 Declarative Mapped models, kế thừa `UUIDPrimaryKeyMixin`, sử dụng `JSON` cho dữ liệu dạng mảng (đảm bảo tương thích chéo SQLite và PostgreSQL).
- **`schemas/`**: Pydantic v2 schemas (`ConfigDict(from_attributes=True)`), toàn bộ trường dùng `snake_case`.
- **`repositories/`**: Truy cập dữ liệu thuần túy qua SQLAlchemy ORM session, không chứa logic nghiệp vụ rẽ nhánh.
- **`services/`**: Chứa toàn bộ Business Rules (ví dụ: giới hạn số lượng đặt lịch, tính tổng tiền, kiểm tra trạng thái).
- **`routers/`**: Định nghĩa REST API endpoints, Dependency Injection DB session, xử lý HTTP Status Codes và bắt `HTTPException`.

### 2. Cấu trúc Client (React Vite Web & React Native Mobile)
- **Store (`src/store/appStore.ts`)**: Quản lý state tập trung, đồng bộ các thực thể danh mục, giỏ hàng/đơn đặt và trạng thái đăng nhập.
- **API Client (`src/api/client.ts`)**: Chuẩn hóa client với baseURL, headers Bearer Token tự động, và các hàm gọi API tương ứng với backend routes.
- **Modular Components & Screens**: Chia tách rõ ràng giữa màn hình và components dùng lại, luôn hỗ trợ ma trận 5 trạng thái (Default, Loading, Empty, Error, Success).

---

## 🛠️ 7. Cẩm Nang Xử Lý Sự Cố Thường Gặp (Troubleshooting & FAQs)

### Q1: PyTest báo lỗi khi chạy kiểm thử?
- **Giải pháp**: Kiểm tra môi trường đã cài `pytest-asyncio` và `aiosqlite` chưa qua `make setup`. Luôn chạy kèm `PYTHONPATH=src` để Python nhận diện đúng module `backend` và `db`.

### Q2: Checkpoint bị lệch trạng thái so với code trên đĩa sau khi sửa thủ công?
- **Giải pháp**: Chạy ngay lệnh `make sync` (hoặc `python scripts/sync_state.py`). Hệ thống sẽ tự động quét toàn bộ mã nguồn `src/`, chạy test ngầm, suy diễn pha SDLC tương ứng và cập nhật Checkpoint đồng bộ tức thì.

### Q3: Làm sao để chuyển từ SQLite sang PostgreSQL trên Production?
- **Giải pháp**:
  1. Cập nhật biến môi trường `DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/dbname` trong file `.env`.
  2. Nếu dùng Supabase, chú ý: Dùng **Session Pooler (port 5432)** cho migrations `DIRECT_DATABASE_URL` và **Transaction Pooler (port 6543)** cho FastAPI runtime.
  3. Chạy `alembic upgrade head` (hoặc `make migrations`) để đồng bộ toàn bộ schema lên PostgreSQL.
