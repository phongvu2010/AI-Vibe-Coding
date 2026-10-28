# Cẩm Nang Hướng Dẫn Sử Dụng AI-Vibe-Coding (USER_GUIDE.md)

Chào mừng bạn đến với **AI-Vibe-Coding** — Template AI Software House vận hành trên nền tảng **Antigravity 2.0**. Cẩm nang này giúp bạn nắm vững cách khởi chạy một dự án mới từ con số 0 (Day-0) và phát triển các tính năng tiếp theo (Day-N).

---

## 🧭 0. Triết Lý "Disciplined Vibe Coding" & 5 Trụ Cột Kỷ Luật Kỹ Thuật

**Vibe Coding** là phương thức phát triển phần mềm mà bạn giao tiếp với AI bằng ngôn ngữ tự nhiên để hiện thực hóa ý tưởng với tốc độ tối đa.

Tuy nhiên, nếu không có kỷ luật kỹ thuật, Vibe Coding sẽ tạo ra "mã nguồn rác" khó bảo trì, lệch chuẩn dữ liệu và tiềm ẩn lỗ hổng bảo mật nghiêm trọng. Hệ thống **AI-Vibe-Coding** khắc phục triệt để điều này bằng **5 trụ cột kỷ luật kỹ thuật (Disciplined Vibe Coding)** kế thừa từ `Multi-Agents-Dev` và `AI-Team-Dev`:

1. **Phân vai chuyên trách (Specialized Sub-Teams):** 15 AI Agents được chia thành 5 Sub-Teams chuyên sâu theo chuẩn SDLC khép kín (Discovery ➔ Architecture ➔ Engineering ➔ QA ➔ Release).
2. **Quyền kiểm soát tối cao của con người (HITL Quality Gates):** 3 Chốt chặn đảm bảo Product Owner và Tech Lead phê duyệt Scope & PRD (Gate 1), duyệt Kiến trúc & API Contract (Gate 2), và cấp phép Production Readiness (Gate 3) trước khi bàn giao.
3. **Mã nguồn chuẩn Clean Architecture:** Phân tầng triệt để (`models` ➔ `schemas` ➔ `repositories` ➔ `services` ➔ `routers`), chuẩn hóa 100% `snake_case` xuyên suốt Database, Backend và Client.
4. **Kiểm thử thực tế Zero Hallucination:** Toàn bộ test case chạy qua subprocess thật (Ruff Linter, Alembic Zero Drift, PyTest Coverage $\ge 80\%$, TypeScript Strict Typecheck, và Headless E2E User Journeys).
5. **Định tuyến mô hình tối ưu chi phí (Model Routing Matrix):** Phân bổ hợp lý Pro (cho Architecture/Review), Flash (cho Dev/QA), và Flash-Lite (cho Release/Docs), tiết kiệm 60% – 75% chi phí token.

---

## 🚀 1. Khởi Động Dự Án Mới (Day-0 Quickstart)

### Bước 1: Chuẩn Bị Môi Trường
```bash
cd AI-Vibe-Coding
cp .env.example .env
make contracts   # Xác nhận hệ thống hợp đồng dữ liệu sẵn sàng
```

### Bước 2: Nhập Đề Bài Khách Hàng Vào Chat Canvas
Trong Chat Canvas của Antigravity 2.0, bạn (với vai trò Product Owner / Client) gửi yêu cầu dự án:
```markdown
Tôi muốn xây dựng nền tảng theo bản đề bài tại @examples/cliniccare_sample_brief.md (hoặc @examples/sample_client_brief.md). 
Nhờ Tech Lead khởi động Sub-Team 1 (Discovery Squad) để tiếp nhận và làm rõ yêu cầu!
```

---

## 🏢 1a. Hai Chế Độ Vận Hành Linh Hoạt (Dual-Mode Architecture)

Template **AI-Vibe-Coding** cung cấp 2 chế độ làm việc tùy theo nhu cầu thực tế của bạn:

1. **Chế Độ 1: In-Place Development (`src/`) — Dành cho Dự Án Độc Lập / Khởi Nghiệp**:
   - Mã nguồn nằm cố định tại `src/` (`src/backend/`, `src/db/`, `src/frontend/`, `src/mobile/`).
   - Phù hợp nhất khi bạn tập trung xây dựng **1 sản phẩm phần mềm duy nhất**. Bạn có thể code trực tiếp, hot-reload, chạy `make dev` / `.\run.ps1 dev` và kiểm thử tức thì.

2. **Chế Độ 2: Multi-Project Agency Mode (`workspaces/output_project/`) — Dành cho Software House / Đa Dự Án**:
   - Mỗi đề bài brief từ khách hàng (như `MotoCare`, `ClinicCare`) sẽ được động cơ sinh mã tách biệt vào `workspaces/output_project/<project_name>/`.
   - Mỗi dự án sở hữu trọn vẹn: mã nguồn Backend, Frontend Web, Mobile App, Dockerfile, bộ tài liệu `artifacts/`, và checkpoints lưu trữ riêng trong `data.db`.
   - Bạn có thể nhận và bàn giao hàng chục dự án khác nhau trên cùng một workspace mà không sợ đè chồng mã nguồn.

### 📁 Quy Ước Phân Vùng Lưu Trữ Hồ Sơ & Giao Phẩm (Artifacts Storage Mapping)

| Phân Vùng | Chế Độ 1: In-Place Monorepo (`src/`) | Chế Độ 2: Multi-Project Agency (`workspaces/`) |
| :--- | :--- | :--- |
| **Vị trí Mã Nguồn** | `src/backend/`, `src/frontend/`, `src/mobile/`, `src/db/` | `workspaces/output_project/<project>/` |
| **Hồ sơ Phân tích (Phase 1)** | `docs/specs/<feature-slug>/prd.md` | `workspaces/artifacts/01_discovery/` (`PRD.md`, `user_stories.json`, `clarification_qna.md`) |
| **Thiết kế & Hợp đồng (Phase 2)** | `docs/specs/<feature-slug>/plan.md` | `workspaces/artifacts/02_architecture/` (`architecture_design.md`, `openapi.yaml`, `erd.mermaid`) |
| **Biên bản Duyệt Gate 1 & 2** | Duyệt trực tiếp qua chat / `ask_question` | `workspaces/artifacts/review_gate_1_prd.md`, `review_gate_2_architecture.md` |
| **Báo cáo Kiểm thử & Audit (Phase 4)** | `docs/specs/<feature-slug>/test-report.md`, `review-report.md` | `workspaces/artifacts/04_quality/` (`test_summary.json`, `code_review_report.md`, `coverage.json`) |
| **Giao phẩm Bàn giao (Phase 5)** | `docs/specs/<feature-slug>/handover.md` | `workspaces/artifacts/05_handover/` (`RELEASE_MANIFEST.json`, `UAT_CHECKLIST.md`, `USER_MANUAL.md`) |
| **Bản Phát Hành Hoàn Chỉnh** | `dist/releases/<slug>-v1.0.0.zip` | `workspaces/artifacts/05_handover/<slug>-v1.0.0.zip` |

---

## 📋 1b. Hướng Dẫn Thực Chiến Toàn Trình Với Đề Bài Mẫu (End-to-End Walkthrough: ClinicCare)

Hệ thống cung cấp sẵn 2 kịch bản bài toán thực tế đã được chuẩn hóa để bạn thử nghiệm ngay:
1. **MotoCare (`examples/sample_client_brief.md`)**: Nền tảng đặt lịch bảo dưỡng xe máy thông minh (FastAPI + Next.js / React Native Expo).
2. **ClinicCare (`examples/cliniccare_sample_brief.md`)**: Nền tảng y tế đặt khám bệnh trực tuyến với ràng buộc nghiệp vụ giới hạn ca khám (BR-01: tối đa 2 bệnh nhân/slot 30 phút), phân quyền RBAC và thanh toán VietQR.

### 🧪 Kịch Bản Thực Hành Nhanh: Triển Khai Dự Án ClinicCare Từ A đến Z

#### Bước 1: Chuẩn Bị Đề Bài (Toàn Văn Đề Bài Mẫu Chuẩn ClinicCare)
Bạn có thể sao chép trực tiếp nội dung dưới đây vào `workspaces/cliniccare_brief.md` (hoặc sử dụng tệp có sẵn tại `examples/cliniccare_sample_brief.md`):

```markdown
# ĐẶC TẢ DỰ ÁN MẪU: CLINICCARE - ĐẶT KHÁM BỆNH TRỰC TUYẾN
## 1. Mục Tiêu Sản Phẩm (Product Vision)
Số hóa toàn diện quy trình tiếp nhận, tra cứu chuyên khoa và đặt lịch khám cho chuỗi phòng khám y tế ClinicCare. Giúp bệnh nhân chủ động thời gian, giảm thiểu 90% thời gian chờ đợi tại quầy lễ tân và tối ưu công suất phòng khám.

## 2. Đối Tượng Người Dùng & Vai Trò (User Roles)
- **Bệnh nhân (Patient)**: Tra cứu chuyên khoa, bác sĩ, khung giờ khám; Đặt lịch hẹn, nhận mã xác nhận, theo dõi lịch sử khám; Hủy hoặc dời lịch khám trước giờ hẹn tối thiểu 2 tiếng.
- **Bác sĩ & Lễ tân (Doctor & Staff / Admin)**: Theo dõi danh sách ca khám trong ngày; Đánh dấu trạng thái khám: CONFIRMED -> IN_PROGRESS -> COMPLETED hoặc NO_SHOW; Cập nhật ghi chú tóm tắt sau khám.

## 3. Các Tính Năng Cốt Lõi MVP (In-Scope)
- **Xác thực & Người dùng**: Đăng ký/đăng nhập bằng SĐT/Email + Mật khẩu mã hóa (JWT Bearer Token); Phân quyền RBAC: patient, staff, admin.
- **Danh mục Chuyên khoa & Dịch vụ**: Danh mục chuyên khoa (Nội, Tim mạch, Tai Mũi Họng, Nhi, Da liễu...); Bảng giá niêm yết theo dịch vụ.
- **Đặt lịch theo Khung giờ (Slot Booking)**:
  - Chọn bác sĩ và khung giờ khám (mỗi ca khám kéo dài 30 phút).
  - Quy tắc Nghiệp vụ Cốt lõi (BR-01): Mỗi khung giờ 30 phút chỉ tiếp nhận tối đa 2 bệnh nhân. Quá tải tự động khóa và gợi ý slot lân cận.
  - Chống xung đột: Bệnh nhân không thể đặt 2 lịch khám trùng giờ.
- **Quản lý Đơn Đặt Khám (Appointments)**: Theo dõi trạng thái (PENDING, CONFIRMED, CANCELLED, COMPLETED); Bệnh nhân có thể tự hủy đơn có lý do.
- **Thanh toán & Mã Phiếu**: Sinh mã QR chuyển khoản VietQR động; Tự động sinh mã phiếu khám CC-YYYYMMDD-XXXX.

## 4. Tính Năng Dành Cho Tương Lai (Out-of-Scope v2.0)
- Tích hợp cổng thẻ quốc tế Visa/Mastercard (Stripe/OnePay).
- Khám bệnh từ xa trực tuyến qua video (Telemedicine WebRTC).
- Kết nối bệnh án điện tử quốc gia và BHYT.
```

#### Bước 2: Khởi Chạy Chu Trình
Bạn có thể lựa chọn các phương thức thực thi linh hoạt:
- **Cách 1 (Khuyên dùng - Antigravity Chat Canvas)**:
  ```markdown
  Tôi muốn phát triển hệ thống theo đề bài tại @workspaces/cliniccare_brief.md (hoặc @examples/cliniccare_sample_brief.md).
  Nhờ Tech Lead điều phối Discovery Squad tiếp nhận yêu cầu và làm rõ nghiệp vụ!
  ```
- **Cách 2 (CLI Multi-Project Agency Mode)**:
  ```bash
  # Khởi chạy dự án Web Portal (React Vite / Next.js) có chốt chặn HITL:
  make dev-orchestrator PROJECT="ClinicCare" FILE="workspaces/cliniccare_brief.md" PLATFORM="web"

  # Hoặc khởi chạy ứng dụng Mobile App (React Native Expo):
  make dev-orchestrator PROJECT="ClinicCare" FILE="workspaces/cliniccare_brief.md" PLATFORM="mobile"

  # Chạy tự động hóa toàn trình không dừng cho CI/CD (Bỏ qua HITL):
  make dev-quick PROJECT="ClinicCare" FILE="workspaces/cliniccare_brief.md" PLATFORM="web"
  ```
  > **Giải thích tham số dòng lệnh:**
  > - `PROJECT="Tên_Dự_Án"`: Định danh dự án (dùng để đặt tên database, package, models và thư mục `workspaces/output_project/<project>/`).
  > - `FILE="đường_dẫn_brief"`: File Markdown chứa yêu cầu ban đầu của khách hàng.
  > - `PLATFORM="web" | "mobile"`: Chỉ định rõ nền tảng giao diện frontend mong muốn (Web React Vite/Next.js hoặc Mobile Expo NativeWind).

- **Cách 3 (Interactive TUI Terminal)**:
  ```bash
  make sdlc    # Khởi chạy giao diện Terminal User Interface (TUI) tương tác từng phase
  ```

#### Bước 3: Phê Duyệt Tại 3 Chốt Chặn Human-in-the-Loop (HITL)

Trong suốt chu trình SDLC, hệ thống tự động tạm dừng tại 3 chốt chặn chất lượng để Tech Lead / Product Owner kiểm tra trực tiếp:

1. **🚦 Gate 1 - Duyệt PRD & Scope (`review_gate_1_prd.md`)**:
   - Sub-Team 1 bóc tách yêu cầu và gửi 1-3 câu hỏi làm rõ qua `ask_question`.
   - Mở file `review_gate_1_prd.md` trên tab **Artifacts / Auxiliary Pane** (khung bên phải Antigravity 2.0).
   - Đọc đối chiếu các tiêu chí then chốt:
     - Mục tiêu SMART và phạm vi rõ ràng: **In-Scope (MVP)** vs **Out-of-Scope (v2.0)**.
     - User Stories tuân thủ 100% cú pháp Gherkin (`Given - When - Then`).
     - Sơ đồ luồng màn hình UI/UX (Mermaid) và Ma trận 5 trạng thái giao diện.
   - Trên Terminal hoặc Chat Canvas, bạn có thể:
     - Chọn `[1] Approve`: Cấp phép chuyển sang Sub-Team 2 thiết kế kiến trúc.
     - Chọn `[2] Request Revision`: Nhập phản hồi chỉnh sửa (ví dụ: *"Thêm xác thực OTP qua SMS"*), AI sẽ tự động điều chỉnh.
     - Hoặc lưu checkpoint: `make checkpoint PHASE=gate_1_prd NOTE="Duyệt PRD ClinicCare"`.

2. **🚦 Gate 2 - Ký Duyệt Kiến Trúc & Contract Matrix (`review_gate_2_architecture.md`)**:
   - Sub-Team 2 thiết kế ERD quan hệ, mô hình đe dọa STRIDE và ma trận dữ liệu `snake_case`.
   - Mở file `review_gate_2_architecture.md` đối chiếu:
     - Tech Stack chuẩn: FastAPI + SQLAlchemy 2.0 Async + React/Next.js hoặc Expo Mobile.
     - Đặc tả API: Kiểm tra file `openapi.yaml` và ma trận dữ liệu xuyên tầng trong `plan.md`.
     - Phân tích an ninh: Mô hình đe dọa STRIDE và ma trận phân quyền RBAC/ABAC.
   - Trên Terminal hoặc Chat Canvas:
     - Chọn `[1] Approve`: Cấp phép cho Dev Squads bắt đầu lập trình Đợt kép (Wave 1: DB + Mock UI).
     - Chọn `[2] Request Revision`: Nhập chỉ dẫn điều chỉnh kỹ thuật (ví dụ: *"Bổ sung trường phone_number VARCHAR(15), thêm quan hệ One-to-Many giữa Clinic và Doctor, và cập nhật index cho booking_date"*), Sub-Team 2 sẽ tự động tái thiết kế ERD và OpenAPI contract.

3. **🚦 Gate 3 - Cấp Phép Triển Khai & Đóng Gói (`review_gate_3_deploy.md`)**:
   - Sub-Team 3 viết mã theo 2 đợt (Wave 1: DB + FE Mocks $\rightarrow$ Wave 2: Live APIs).
   - Sub-Team 4 chạy kiểm định toàn diện. Mở file `review_gate_3_deploy.md` đối chiếu 4 chỉ số:
     - **Backend PyTest Coverage**: Đạt $\ge 80\%$ (ví dụ: $90\%$).
     - **Database Schema Drift**: Báo cáo `Zero Drift` (Models khớp 100% với DB qua `alembic check`).
     - **Frontend Type Safety**: TypeScript Strict và E2E User Journeys đều báo `PASSED`.
     - **Security Audit**: 0 rò rỉ hardcoded secrets; tuân thủ OWASP API Security Top 10.
   - Trên Terminal hoặc Chat Canvas:
     - Chọn `[1] Approve`: Cấp phép cho Sub-Team 5 đóng gói bản phát hành `make release`.
     - Chọn `[2] Request Revision`: Nhập yêu cầu khắc phục (ví dụ: *"Coverage đang 75%, yêu cầu bổ sung test case cho Auth Service và kích hoạt Self-Healing sửa lỗi validate email"*), Sub-Team 4 sẽ điều phối Dev Squad khắc phục trước khi đóng gói.

#### Bước 4: Vận Hành & Kiểm Định Cục Bộ (Local Verification)
```bash
# 1. Chạy toàn bộ kiểm thử tự động 5 tầng
make test-all

# 2. Xuất báo cáo độ phủ mã nguồn HTML vào thư mục Quality Artifacts
make cov-html
# -> Mở báo cáo tại: workspaces/artifacts/04_quality/htmlcov/index.html

# 3. Khởi chạy Backend FastAPI (Swagger UI tại http://localhost:8000/api/v1/docs)
make dev

# 4. Khởi chạy ứng dụng Web Frontend (http://localhost:3000 hoặc http://localhost:5173)
make dev-mock    # Chạy giao diện với mock fixtures
# hoặc chuyển đổi preset linh hoạt:
make preset-vite     # SPA Dashboard siêu tốc
make preset-nextjs   # Next.js 15 App Router SSR / SEO
make add-mobile      # Khởi tạo React Native Expo trong src/mobile/

# 5. Khởi chạy toàn bộ hệ sinh thái qua Docker Compose
make docker-fullstack
```

#### Bước 5: Đóng Gói Bản Phát Hành & Bàn Giao
```bash
make release VERSION=1.0.0
```
Hệ thống sẽ tạo gói `.zip` hoàn chỉnh tại `dist/releases/` kèm mã băm SHA-256, `RELEASE_MANIFEST.json`, `USER_MANUAL.md` và `UAT_CHECKLIST.md` để khách hàng nghiệm thu 1-chạm.

---

## 👥 2. Điều Phối 5 Sub-Teams & 3 Chốt Chặn Human-in-the-Loop (HITL)

Quá trình vận hành đi qua 5 Sub-Teams và 3 Chốt chặn phê duyệt tương tác hiển thị trực tiếp trên tab **Artifacts / Auxiliary Pane** của Antigravity 2.0:

### Giai đoạn 0: Tiếp Nhận & Thiết Lập PRD (Sub-Team 1)
- Tech Lead sẽ triệu hồi `@account-lead` để bóc tách phạm vi và `@lead-ba` để phỏng vấn bạn.
- Bạn sẽ nhận được 1-3 câu hỏi trắc nghiệm qua công cụ `ask_question`. Sau khi chọn đáp án, `@lead-ba` xuất bản `docs/specs/<feature-slug>/prd.md` và `@uiux-designer` xuất bản `ui_ux_spec.md`.
- 👉 **Quality Gate 1 (`review_gate_1_prd.md`)**:
  - Mở file tóm tắt trên tab **Artifacts**.
  - Kiểm tra mục tiêu SMART, User Stories chuẩn định dạng Gherkin (`Given - When - Then`), và luồng màn hình UI.
  - Phê duyệt `APPROVED` để chuyển sang Giai đoạn 1:
    ```bash
    make checkpoint PHASE=gate_1_prd NOTE="Client duyệt PRD"
    ```

### Giai đoạn 1: Thiết Kế Kỹ Thuật & Hợp Đồng Dữ Liệu (Sub-Team 2)
- `@system-architect` thiết kế ERD và sơ đồ phân tầng Clean Architecture.
- `@security-architect` phân tích mô hình đe dọa STRIDE và ma trận phân quyền RBAC.
- `@tech-planner` xuất bản `docs/specs/<feature-slug>/plan.md` với **Cross-Layer Contract Matrix** (chuẩn hóa 100% `snake_case`).
- 👉 **Quality Gate 2 (`review_gate_2_architecture.md`)**:
  - Kiểm tra Tech Stack, OpenAPI specification (`openapi.yaml`), và sơ đồ `erd.mermaid`.
  - Phê duyệt cấp phép cho Dev Squads bắt đầu viết mã:
    ```bash
    make checkpoint PHASE=gate_2_architecture NOTE="Duyệt ERD & Contract Matrix"
    ```

### Giai đoạn 2 & 3: Lập Trình Đợt Kép (Sub-Team 3 - Dev Squad)
- **Wave 1 (Triển khai song song)**:
  - `@db-dev`: Sinh SQLAlchemy 2.0 Async Models và Alembic Migrations trong `src/db/`.
  - `@frontend-dev`: Dựng cấu trúc màn hình UI (Next.js/Vite/Expo) và TypeScript interfaces theo Mock Fixtures.
- **Handshake Gate**: Tech Lead kiểm tra models và contracts khớp nhau trước khi kích hoạt Wave 2.
- **Wave 2 (Kết nối Live API)**:
  - `@backend-dev`: Sinh Pydantic v2 schemas, business services và FastAPI routers trong `src/backend/` kết nối trực tiếp `src/db/`.
  - `@devops-engineer`: Cấu hình Dockerfile và docker-compose.
- 👉 Lưu checkpoint sau khi lập trình xong:
  ```bash
  make checkpoint PHASE=engineering NOTE="Hoàn thành Wave 1 & 2"
  ```

### Giai đoạn 4 & 5: Kiểm Thử Tự Động & Thẩm Định Code (Sub-Team 4)
- `@qa-tester` chạy bộ kiểm thử 5 tầng (`make smoke` hoặc `python scripts/smoke_test.py`).
- **Self-Healing Loop**: Nếu có test fail, tự động kích hoạt sửa lỗi (tối đa 3 vòng lặp với traceback cắt tỉa 15-25 dòng qua `scripts/parse_traceback.py`).
- `@code-reviewer` audit git diff và lập bảng điểm chất lượng 100đ (`make contracts`).
- 👉 **Quality Gate 3 (`review_gate_3_deploy.md`)**:
  - Tiêu chí bắt buộc: **PyTest Coverage $\ge 80\%$**, **Zero Schema Drift** (`alembic check`), **0 Secret Leaks**, và điểm đánh giá review $\ge 85/100$.
  - Cấp phép phát hành và đóng gói:
    ```bash
    make checkpoint PHASE=gate_3_deploy NOTE="Pass 5 tầng tests & điểm review >= 85"
    ```

### Giai đoạn 6: Đóng Gói & Bàn Giao Khách Hàng (Sub-Team 5)
- `@release-engineer` chạy `make release` để tạo gói `.zip` và `RELEASE_MANIFEST.json` trong `dist/releases/`.
- `@tech-writer` soạn thảo `USER_MANUAL.md` và `DEPLOYMENT.md`.
- `@handover-lead` cung cấp `UAT_CHECKLIST.md` và hướng dẫn bạn nghiệm thu ứng dụng một chạm (`docker compose up` hoặc `make dev`).
- 👉 Lưu checkpoint hoàn tất:
  ```bash
  make checkpoint PHASE=completed NOTE="Bàn giao sản phẩm hoàn tất"
  ```

---

## 💬 2b. Hướng Dẫn Triệu Hồi Native Sub-Teams Trên Chat Canvas (Prompt Matrix)

Trong quá trình phát triển trên **Antigravity 2.0**, bên cạnh các lệnh dòng lệnh (CLI/Makefile), bạn có thể gọi trực tiếp từng Sub-Team chuyên biệt bằng cú pháp `@<tên_subteam>` kết hợp cùng các Slash Commands trực tiếp trong khung chat:

| Sub-Team / Alias | Ví Dụ Câu Lệnh Tương Tác Trên Chat Canvas | Tác Dụng Cụ Thể |
| :--- | :--- | :--- |
| **`@discovery_team`**<br/>(hoặc `@discovery-squad`) | `@discovery_team: /grill-me Hãy phỏng vấn tôi để làm rõ các điểm mâu thuẫn trong file brief` | Kích hoạt phiên phỏng vấn nghiệp vụ chuyên sâu, phát hiện giả định ngầm trước khi chốt PRD. |
| **`@discovery_team`** | `@discovery_team: /plan Bóc tách phạm vi In-Scope MVP và tạo User Stories chuẩn Gherkin.` | Tạo tài liệu `prd.md` và sơ đồ luồng màn hình UI/UX. |
| **`@architecture_team`**<br/>(hoặc `@architecture-squad`)| `@architecture_team: /plan Thiết kế OpenAPI 3.0 và sơ đồ Mermaid ERD chuẩn theo Tech Lead Profile.` | Lập sơ đồ thực thể quan hệ, ma trận dữ liệu 3 tầng và đặc tả API REST. |
| **`@architecture_team`** | `@architecture_team: /boost Thực hiện phân tích mô hình đe dọa bảo mật STRIDE và phân quyền RBAC.` | Kích hoạt chế độ Deep Thinking phân tích an ninh và mô hình bảo mật OWASP. |
| **`@engineering_team`**<br/>(hoặc `@dev-squad`) | `@engineering_team: /plan Lập trình tính năng phân tầng Clean Architecture 5 tầng.` | Lập kế hoạch phân bổ 2-Wave Dev giữa Database, Frontend và Backend. |
| **`@engineering_team`** | `@engineering_team: /goal Hoàn thiện mã nguồn Backend FastAPI và Frontend TypeScript kèm Jest tests.` | Thực thi lập trình trọn gói và kiên trì hoàn thiện mã nguồn sạch sẽ. |
| **`@qa_team`**<br/>(hoặc `@qa-squad`) | `@qa_team: Chạy PyTest đo độ phủ Code Coverage, kiểm tra alembic check zero drift và scan Secret Leaks.` | Thực thi kiểm định 5 tầng, đo độ phủ $\ge 80\%$ và kiểm toán an ninh. |
| **`@qa_team`** | `@qa_team: Tự động kích hoạt Auto-Healing vá lỗi nếu phát hiện test case thất bại.` | Khởi động vòng lặp tự sửa lỗi có ngắt mạch (tối đa 3 vòng lặp). |
| **`@release_team`**<br/>(hoặc `@release-squad`) | `@release_team: Đóng gói bản phát hành ZIP, tính checksum SHA-256 và lập bảng nghiệm thu UAT_CHECKLIST.md.` | Build check, kiểm tra Conventional Commits và xuất bản gói phần mềm `.zip`. |
| **`@fast_track_team`**<br/>(hoặc `@fast-track-squad`) | `@fast-track_team: Bổ sung endpoint lọc danh sách theo trạng thái và viết pytest kiểm thử.` | Làn chạy cao tốc cho micro-tasks & bugfix, bỏ qua Gate 1 & 2. |
| **`@fast_track_team`** | `@fast-track_team: Sửa lỗi hiển thị datepicker trên Mobile App và kiểm tra typecheck.` | Xử lý trực tiếp lỗi giao diện và bảo đảm type safety. |

### ⚡ Cẩm Nang Triệu Hồi Trực Tiếp 7 Tác Tử Hạt Nhân (1-Line Direct Dispatch Prompts)
Khi lập trình viên muốn "Vibe Code" trực tiếp từng phần việc với từng chuyên gia đơn lẻ mà không cần kích hoạt cả Sub-Team:
- **`@ba`**: `Nhờ @ba phỏng vấn (/grill-me) và xuất bản prd.md cho tính năng <tên_tính_năng>`
- **`@planner`**: `Nhờ @planner (/plan) thiết kế Data Contract Matrix và REST API spec cho <tên_tính_năng>`
- **`@db-dev`**: `Nhờ @db-dev tạo models SQLAlchemy 2.0 và sinh Alembic migration tại src/db/`
- **`@backend-dev`**: `Nhờ @backend-dev triển khai Service nghiệp vụ và FastAPI routes tại src/backend/`
- **`@frontend-dev`**: `Nhờ @frontend-dev hoàn thiện màn hình xử lý đủ 5 UI states tại src/frontend/`
- **`@qa-tester`**: `Nhờ @qa-tester chạy bộ test 5 tầng và kiểm tra đồng bộ hợp đồng dữ liệu`
- **`@code-reviewer`**: `Nhờ @code-reviewer audit git diff tối ưu token và lập review-report.md`

---

## 🎨 3. Quản Trị Kiến Trúc Client (Presets Web & Mobile)

AI-Vibe-Coding tích hợp sẵn bộ presets từ `AI-Team-Dev`, cho phép bạn chuyển đổi linh hoạt công nghệ Frontend:

```bash
# Xem trạng thái client hiện tại
make frontend-status

# Chuyển đổi Web Client sang React + Vite (SPA / Tốc độ cực nhanh cho Dashboards)
make preset-vite

# Chuyển đổi Web Client sang Next.js 15 (App Router + React 19 cho SEO & SSR)
make preset-nextjs

# Khởi tạo App Mobile React Native (Expo SDK 51+ / 52 + NativeWind Tailwind CSS)
make add-mobile

# Khởi chạy Frontend 1-chạm tự động (tự check Node.js, install npm và chạy dev server):
./src/frontend/setup_dev.sh
```

---

## 💾 4. Quản Lý Trạng Thái SDLC & Phục Hồi Phiên (Checkpoints & Rollback)

Kế thừa cơ chế State Persistence từ `Multi-Agents-Dev`:

```bash
# 1. Liệt kê danh sách tất cả checkpoints đã lưu
make checkpoints

# 2. Xem hướng dẫn tiếp tục phiên làm việc khi mở lại dự án
make resume

# 3. Lưu checkpoint thủ công trước khi refactor lớn
make checkpoint PHASE=engineering NOTE="Trước khi refactor bảng users"

# 4. Khôi phục (Rollback) mã nguồn về một checkpoint cũ an toàn
make restore ID=CP_20261017_172129_gate_1_prd
```

### 4.1. Tinh chỉnh Mã nguồn Thủ công & Đồng bộ Checkpoint (`make sync`)
Khi bạn trực tiếp can thiệp chỉnh sửa code hoặc yêu cầu AI sửa code qua Chat Canvas ngoài quy trình CLI:
1. Chỉnh sửa file bất kỳ trong `src/` hoặc `workspaces/output_project/`.
2. **Luôn chạy lệnh đồng bộ sau khi sửa:**
   ```bash
   make sync PROJECT="MotoCare_Upgrade"
   # Hoặc trên Windows:
   .\run.ps1 sync
   ```
3. **Cơ chế hoạt động:**
   - Bộ **State Synchronizer** (`scripts/sync_state.py`) tự động quét lại toàn bộ cây thư mục mã nguồn và artifacts.
   - Tự động chạy lại `pytest` và `alembic check` để đảm bảo code bạn sửa không gây lỗi hoặc Schema Drift.
   - Tự động phát hiện Phase SDLC hiện tại, cập nhật `test_summary.json` và ghi đè trạng thái sạch vào file Checkpoint JSON để lệnh `make resume` tiếp tục phiên mượt mà.

---

## 🛠️ 5. Bảng Phím Tắt Lệnh 1-Chạm (Makefile Cheatsheet)

| Lệnh | Ý nghĩa |
| :--- | :--- |
| `make dev` | Khởi chạy FastAPI Backend với chế độ hot-reload trên cổng 8000. |
| `make sdlc` | Khởi chạy chu trình tương tác 5 Pha kèm Terminal HITL Quality Gates (G1, G2, G3). |
| `make dev-orchestrator` | Khởi chạy chu trình Multi-Agents SDLC toàn diện với Gemini AgentFactory từ Brief. |
| `make dev-quick` | Khởi chạy chu trình Headless Batch SDLC tự động không dừng cho CI/CD. |
| `make test` | Chạy toàn bộ unit tests trên SQLite in-memory cô lập. |
| `make test-frontend-unit` | Chạy unit tests cho Frontend Web & Mobile components. |
| `make test-frontend` | Chạy tổng hợp toàn bộ kiểm thử Frontend (Unit, E2E & Production Build check). |
| `make smoke` | Chạy trọn vẹn bộ kiểm thử 5 tầng (Linter, Contract, Migration, Pytest, Typecheck). |
| `make contracts` | Quét kiểm tra đồng bộ trường dữ liệu (`snake_case`) giữa 3 tầng. |
| `make migrations`| Kiểm tra đồ thị phân nhánh Alembic Migration DAG. |
| `make seed` | Nạp dữ liệu mẫu ban đầu vào database. |
| `make release` | Đóng gói bản phát hành `.zip` kèm checksum manifest. |
| `make docker-up` | Khởi chạy dịch vụ lõi (PostgreSQL + Backend) bằng Docker Compose. |
| `make docker-fullstack` | Khởi chạy toàn bộ hệ thống Fullstack (PostgreSQL + Backend + Frontend). |
| `make clean` | Dọn dẹp sạch cache và bytecode rác. |
| **`make frontend-status`** | Kiểm tra trạng thái framework Web & Mobile hiện tại. |
| **`make preset-vite`** | Chuyển đổi Web Frontend sang React + Vite. |
| **`make preset-nextjs`** | Chuyển đổi Web Frontend sang Next.js 15 SSR. |
| **`make add-mobile`** | Khởi tạo ứng dụng Mobile React Native Expo trong `src/mobile/`. |
| **`make test-cov`** | Chạy Pytest đo độ phủ Code Coverage (ngưỡng tối thiểu $\ge 80\%$). |
| **`make typecheck`** | Kiểm tra kiểu dữ liệu TypeScript Web Frontend (Strict mode). |
| **`make typecheck-mobile`**| Kiểm tra kiểu dữ liệu TypeScript Mobile App (Strict mode). |
| **`make check-frontend-build`**| Thẩm định tính sẵn sàng Production Build của Frontend (package.json, tsconfig). |
| **`make backup`** | Sao lưu an toàn toàn bộ mã nguồn và specs vào `dist/backups/`. |
| **`make clean-project`** | Sao lưu an toàn và dọn sạch dự án cũ để đón nhận brief mới. |
| **`make models`** | Xem ma trận định tuyến mô hình AI & tối ưu chi phí token (Pro, Flash, Flash-Lite). |
| **`make checkpoint`** | Lưu Checkpoint trạng thái kèm snapshot mã nguồn và sinh file `review_gate_*.md`. |
| **`make checkpoints`** | Hiển thị bảng danh sách các checkpoint đã lưu. |
| **`make test-e2e`** | Chạy kiểm thử E2E giả lập hành trình người dùng (`run_e2e_tests.cjs`). |
| **`make test-output`** | Chạy toàn bộ kiểm thử (Backend Pytest, DB drift, Frontend Unit/E2E) trên `workspaces/output_project/`. |
| **`make run-output-backend`** | Khởi chạy server FastAPI độc lập của output_project tại `http://localhost:8000`. |
| **`make run-output-frontend`** | Khởi chạy Web/Mobile Frontend của output_project. |
| **`make docker-output-up`** | Khởi chạy multi-containers Docker Compose cho `workspaces/output_project/infra`. |
| **`make clean-output`** | Tự động sao lưu và dọn sạch `workspaces/output_project/` và `artifacts/`. |
| **`make lean-workspace`** | Kích hoạt chế độ In-Place Vibe Coding siêu tinh gọn (chỉ giữ `src/` và `docs/specs/`). |
| **`make sync`** | Quét mã nguồn thực tế, chạy kiểm thử, kiểm tra migrations và đồng bộ ngược vào Checkpoint. |
| **`make gate-review`** | Phê duyệt hoặc từ chối Gate (`make gate-review GATE=1 STATUS=APPROVED NOTE="..."`). |
| **`make gate-interactive`** | Mở menu dòng lệnh tương tác để Tech Lead duyệt Gate trực quan. |
| **`make resume`** | Hiển thị vị trí dừng và chỉ dẫn bước kế tiếp cho Tech Lead. |
| **`make restore ID=...`**| Rollback mã nguồn về checkpoint đã lưu. |

---

## ❓ 6. Cẩm Nang Xử Lý Sự Cố Thường Gặp (FAQs)

### Q1: Làm thế nào để thay đổi mô hình AI sang Gemini 3.8 Series?
Trong file `.env`, bạn chỉ cần khai báo các biến môi trường tương ứng:
```env
GEMINI_PRO_MODEL=gemini-3.8-pro
GEMINI_FLASH_MODEL=gemini-3.8-flash
GEMINI_FLASH_LITE_MODEL=gemini-3.8-flash-lite
```
Hệ thống sẽ tự động định tuyến toàn bộ 15 Subagents và 5 Sub-Teams sang thế hệ mô hình Gemini 3.8 trên Antigravity 2.0.

### Q2: Tôi muốn cấu hình sử dụng PostgreSQL thật / Supabase thay vì SQLite in-memory?
1. Trong file `.env`, cập nhật `DATABASE_URL` và `DIRECT_DATABASE_URL`:
   ```env
   # 1. PostgreSQL cục bộ (Docker compose):
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/vibe_db

   # 2. Hoặc Supabase Cloud (Kiến trúc Dual-Port tối ưu):
   # Port 6543 (Transaction Pooler) cho FastAPI Runtime: chịu tải hàng ngàn kết nối đồng thời:
   DATABASE_URL=postgresql+asyncpg://postgres.[REF]:[PASS]@aws-0-[REGION].pooler.supabase.com:6543/postgres?ssl=require&prepared_statement_cache_size=0

   # Port 5432 (Session Mode / Direct) riêng cho Alembic DDL Migrations:
   # Tránh lỗi kinh điển: prepared statement "__asyncpg_stmt_..." does not exist
   DIRECT_DATABASE_URL=postgresql+asyncpg://postgres.[REF]:[PASS]@aws-0-[REGION].pooler.supabase.com:5432/postgres?ssl=require
   ```
2. Chạy lệnh migrate khởi tạo: `make migrations` (hoặc `alembic upgrade head`). Alembic tự động ưu tiên `DIRECT_DATABASE_URL` khi chạy DDL.

### Q3: Nếu test bị fail khi chạy `make smoke` hoặc `make test`, tôi nên làm gì?
1. Xem thông báo lỗi đã được trích xuất gọn gàng (15-25 dòng) từ `scripts/parse_traceback.py`.
2. Nếu muốn tự sửa mã nguồn trong `src/`: sửa xong chạy `make contracts` và `make smoke`.
3. Nếu muốn AI tự sửa: yêu cầu qua Chat Canvas:
   `@qa-squad: Test bị fail tại test_users.py, hãy phân tích stack trace và kích hoạt Auto-Healing để vá mã nguồn.`

### Q4: Làm thế nào để chạy thử nghiệm API ngay lập tức với cơ sở dữ liệu có sẵn (`data.db`)?
Hệ thống tích hợp sẵn file `data.db` (SQLite pre-populated data) tại thư mục gốc. Khi muốn chạy thử nghiệm tức thì mà không cần cài đặt hoặc khởi động container PostgreSQL:
1. Đặt biến môi trường trong `.env`:
   ```env
   DATABASE_URL=sqlite+aiosqlite:///data.db
   ```
2. Khởi chạy server: `make dev`
3. Truy cập Swagger UI tại [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs) để test ngay các API endpoints với dữ liệu mẫu có sẵn.

---

> 📘 **Tài liệu tham khảo chuyên sâu:**
> - Cẩm nang quy trình SOP: [WORKFLOW.md](./WORKFLOW.md)
> - Quy chuẩn nạp tác tử: [AGENTS.md](./AGENTS.md)
> - Cẩm nang thực chiến nội bộ: [TEAM_PLAYBOOK.md](./TEAM_PLAYBOOK.md)
> - Đề bài mẫu chuẩn: [examples/sample_client_brief.md](./examples/sample_client_brief.md)
> - Dự án tham khảo hoàn chỉnh: [examples/motocare_reference/](./examples/motocare_reference/)
