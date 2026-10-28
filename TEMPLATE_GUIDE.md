# Cẩm Nang Tùy Biến, Khởi Tạo & Vận Hành Template (TEMPLATE_GUIDE.md)
### Hướng Dẫn Vận Hành AI-Vibe-Coding Cho Mọi Dự Án Phần Mềm Trên Antigravity 2.0

Tài liệu này là cẩm nang hướng dẫn chuyên sâu cho **Tech Lead, Product Owner và AI Developers** về cách sử dụng repository này làm **Template Chuẩn (Starter Template)** để khởi tạo, tùy biến và phát triển các sản phẩm phần mềm từ ngày đầu tiên (Day-0) đến chu kỳ mở rộng liên tục (Day-N) cùng **AI-Vibe-Coding (Antigravity 2.0)**.

Template đã được thiết kế và kiểm chứng chuyên sâu nhằm giải quyết triệt để 4 trụ cột kỹ thuật cốt lõi:
1. **Cơ chế Phản hồi Tự động (Feedback Loop & Circuit Breaker)**: Vòng lặp sửa lỗi 2 chiều cho cả Testing và Code Review với giới hạn tối đa 3 lần lặp và cơ chế ngắt mạch an toàn.
2. **Đồng bộ Hợp đồng Dữ liệu & API (Data & API Contract Synchronization)**: Loại bỏ rủi ro lệch chuẩn qua Ma trận ánh xạ 3 tầng (Database $\leftrightarrow$ Backend $\leftrightarrow$ Frontend/Mobile) và chuẩn hóa casing `snake_case`.
3. **Rào chắn An toàn Thực thi Lệnh (CLI Execution Guardrails)**: Phân quyền thực thi lệnh theo vai trò (Role-based Whitelist & Blacklist) và bảo vệ nghiêm ngặt phân vùng file.
4. **Tiêu chuẩn hóa Hồ sơ Bàn giao (Artifact Handover Schema)**: Chuẩn hóa toàn diện định dạng Metadata Header và phiếu báo lỗi/thẩm định có cấu trúc tại `docs/specs/<feature-slug>/`.

---

## 🎯 1. Tiêu Chí Lựa Chọn: Dự Án Nào Phù Hợp Với Template Này?

### 1.1. Bảng Khảo Sát Nhanh (Checklist Đánh Giá)
Trước khi khởi tạo repo mới, hãy trả lời nhanh 5 câu hỏi sau:
- [ ] Dự án có cần Backend REST API viết bằng **Python (FastAPI)** hiệu năng cao, tài liệu Swagger tự động?
- [ ] Cơ sở dữ liệu chính có phải là quan hệ (**PostgreSQL / SQLite**) với ORM hiện đại (**SQLAlchemy 2.0 Async + Alembic**)?
- [ ] Bạn cần giao diện **Web (Next.js 15 App Router hoặc React Vite SPA)** và/hoặc ứng dụng di động **Mobile App (React Native Expo)**?
- [ ] Dự án yêu cầu ma trận hợp đồng dữ liệu chuẩn hóa 100% `snake_case` giữa Database, API Schemas và TypeScript Interfaces?
- [ ] Bạn muốn quy trình phát triển có kiểm thử tự động nhiều tầng (Pytest, TypeScript Typecheck, Smoke Test, Contract Checker)?

> 👉 **Nếu có từ 3 câu trả lời "CÓ" trở lên**: Đây chính xác là template hoàn hảo dành cho dự án của bạn!

### 1.2. Các Trường Hợp Sử Dụng Điển Hình (Sweet Spot)
* **SaaS Web Platforms**: Các ứng dụng SaaS quản lý thuê bao, xác thực JWT, phân quyền (RBAC), thanh toán và dashboard báo cáo số liệu.
* **Mobile Apps (iOS & Android)**: Ứng dụng di động kết nối trực tiếp với FastAPI backend, styling siêu tốc qua NativeWind Tailwind CSS.
* **Fullstack Web & Mobile Song hành**: Hệ sinh thái hoàn chỉnh gồm cả Web Portal (Next.js/Vite) và App điện thoại (React Native Expo) dùng chung API backend.
* **Internal Tools & Dashboards**: Hệ thống CRM nội bộ, quản trị bán hàng, theo dõi đơn hàng, quản lý kho bãi, nhân sự.
* **Startup MVP $\to$ Production**: Dự án khởi nghiệp cần đưa tính năng ra thị trường thần tốc bằng AI nhưng kiến trúc vẫn sạch và mở rộng được.

### 1.3. Các Trường Hợp KHÔNG Phù Hợp (Non-Goals)
* ❌ **Hệ sinh thái Microservices đa ngôn ngữ phân tán** (Java Spring, Go, Rust, .NET kết hợp): Template tối ưu cho mô hình Modular Monolith hoặc 2-Tier/3-Tier.
* ❌ **Khoa học Dữ liệu / AI Training thuần túy**: Nếu dự án chỉ chạy Jupyter Notebook huấn luyện model PyTorch/TensorFlow lớn mà không cần web/mobile/API.
* ❌ **Website tĩnh đơn giản không cần cơ sở dữ liệu** (Static Blog, Landing Page một trang): Nên dùng Astro, Hugo hoặc HTML tĩnh.

---

## 💻 2. Ba Kiến Trúc Client Linh Hoạt: Web SSR, Web SPA & Mobile App

Template cung cấp sẵn 3 kiến trúc Client đã cấu hình chuẩn Tailwind CSS và typed API client:

| Nền tảng | Công nghệ | Thư mục | Khi nào nên dùng? | Lệnh chuyển đổi / kích hoạt |
| :--- | :--- | :--- | :--- | :--- |
| **Web SSR (Mặc định)** | **Next.js 15 + React 19** | `src/frontend/` | Cần tối ưu SEO, Server Components, Streaming, trang landing / SaaS công khai. | `make preset-nextjs`<br/>*(hoặc `python scripts/setup_frontend.py --preset nextjs`)* |
| **Web SPA** | **React + Vite** | `src/frontend/` | B2B Dashboards, CRM nội bộ, ứng dụng tải siêu nhanh không cần SEO SSR. | `make preset-vite`<br/>*(hoặc `python scripts/setup_frontend.py --preset vite`)* |
| **Mobile App** | **React Native + Expo** | `src/mobile/` | Ứng dụng di động iOS & Android, sử dụng NativeWind (Tailwind CSS cho Mobile). | `make add-mobile`<br/>*(hoặc `python scripts/setup_frontend.py --add-mobile`)* |

> 💡 **Khả năng Chạy Song Song**: Bạn hoàn toàn có thể duy trì đồng thời cả **Web Client** (`src/frontend/`) và **Mobile App** (`src/mobile/`) trong cùng một repo. Cả hai cùng dùng chung Backend FastAPI (`src/backend/`) và Ma trận hợp đồng `snake_case`.

---

## 🛠️ 3. Thiết Lập Môi Trường Phát Triển Day-0 (Chỉ Mất 2 Phút)

### 3.1. Khởi Tạo Repository Mới

#### Cách A: Sử dụng tính năng GitHub Template (Khuyên dùng)
1. Truy cập repo template trên GitHub.
2. Bấm nút xanh lá cây **"Use this template"** $\rightarrow$ chọn **"Create a new repository"**.
3. Đặt tên repository mới (ví dụ: `client-ecom-platform`), chọn quyền Private hoặc Public.
4. Clone repo mới vừa tạo về máy làm việc:
   ```bash
   git clone https://github.com/<your-org>/<your-new-repo>.git
   cd <your-new-repo>
   ```

#### Cách B: Sao chép thủ công & Tẩy sạch lịch sử Git (Day-0 Clean Local Copy)
Khi sao chép từ thư mục template cục bộ sang một dự án khách hàng mới, hãy thực hiện tẩy sạch lịch sử commit và cache cũ để bắt đầu với một Day-0 git tree tinh gọn:
```bash
# 1. Sao chép template sang thư mục dự án mới
cp -r AI-Vibe-Coding /path/to/my-new-project
cd /path/to/my-new-project

# 2. Xóa toàn bộ lịch sử Git cũ và các tệp cache/snapshot tạm
rm -rf .git .snapshots dist/snapshots/* dist/releases/* .ruff_cache .pytest_cache

# 3. Khởi tạo lại lịch sử Git sạch Day-0
git init
git checkout -b main
git add .
git commit -m "chore(day-0): initial project bootstrap from AI-Vibe-Coding template"

# 4. (Tùy chọn) Liên kết với GitHub remote của khách hàng
git remote add origin https://github.com/<your-org>/<client-repo>.git
git push -u origin main
```

### 3.2. Cấu hình biến môi trường
Tạo file `.env` từ file mẫu `.env.example`:
```bash
cp .env.example .env
```
> [!TIP]
> **Kinh nghiệm cấu hình Cloud PostgreSQL (Supabase)**:
> - **FastAPI App Runtime (`DATABASE_URL`)**: Kết nối qua Supavisor Transaction Pooler (`port 6543`) với `prepared_statement_cache_size=0`:
>   `postgresql+asyncpg://postgres.[REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres?ssl=require&prepared_statement_cache_size=0`
> - **Alembic DDL Migrations (`DIRECT_DATABASE_URL`)**: Bắt buộc kết nối Session Mode hoặc Direct Connection (`port 5432`) để hỗ trợ table locks:
>   `postgresql+asyncpg://postgres.[REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres?ssl=require`

### 3.3. Thiết lập Python Virtualenv (Backend & Database)
```bash
# 1. Tạo môi trường ảo .venv
python3 -m venv .venv

# 2. Kích hoạt môi trường ảo
source .venv/bin/activate       # Trên macOS / Linux
# hoặc: .venv\Scripts\activate trên Windows

# 3. Nâng cấp pip và cài đặt dependencies ở chế độ editable
pip install --upgrade pip
pip install -e ".[dev]"
```

### 3.4. Cài đặt dependencies Frontend
```bash
npm --prefix src/frontend install
```

### 3.5. Khởi chạy Bằng Docker (Tuỳ chọn)
Hệ thống cung cấp sẵn 2 chế độ Docker linh hoạt:
* **Chế độ 1 — Chạy Full-Stack 1-Click (Demo / Staging)**:
  Khởi chạy trọn vẹn cả 3 tầng (PostgreSQL 16, FastAPI Backend và Next.js 15 Frontend) trong cùng mạng nội bộ:
  ```bash
  make docker-fullstack
  # hoặc: docker compose up --build -d
  ```
  - Frontend Web UI: `http://localhost:3000`
  - FastAPI Swagger Docs: `http://localhost:8000/api/v1/docs`
  - Backend Health Check: `http://localhost:8000/api/v1/health`
  - PostgreSQL Port: `localhost:5432`

* **Chế độ 2 — Chỉ chạy PostgreSQL Container (Lập trình trên máy host)**:
  Khi bạn muốn dev trực tiếp qua Python virtualenv và npm trên máy host:
  ```bash
  make docker-up
  # hoặc: docker compose up -d postgres
  ```
  *(Lưu ý: Bộ test tự động mặc định sử dụng SQLite async in-memory, do đó bạn không nhất thiết phải bật Docker PostgreSQL chỉ để chạy test).*

### 3.6. Nạp Dữ Liệu Mẫu Khởi Đầu (Seed Data — Tuỳ chọn)
Khi đã khởi chạy PostgreSQL hoặc cần nạp dữ liệu mẫu ban đầu:
- Trên Linux / macOS: `.venv/bin/python src/db/seeds/runner.py`
- Trên Windows: `python src/db/seeds/runner.py`
- Qua lệnh Make: `make seed`
*(Script tự động nạp thư mục `src` mà không cần tiền tố `PYTHONPATH=src`)*.

> ⚠️ **Lưu ý Quan Trọng khi dùng Supabase**:
> BẮT BUỘC dùng **Direct Connection URL (Session Mode port 5432)** với `ssl=require` để chạy Alembic migrations (`alembic upgrade head`). **KHÔNG** dùng Transaction Pooler port 6543 vì không hỗ trợ session locks và prepared statements cho migration DDL.

---

## 🔍 4. Kiểm Chứng Môi Trường Day-0 (Smoke Verification)

Trước khi bắt đầu bất kỳ câu lệnh AI nào, hãy chạy lệnh kiểm tra toàn diện để đảm bảo chuỗi công cụ đã sẵn sàng 100%:

```bash
make smoke
# hoặc: python scripts/smoke_test.py
```
*(Tự động phát hiện OS, kích hoạt virtualenv tương ứng và chạy đủ 5 tầng kiểm tra: Ruff linter, Contract verification, Migration DAG, Isolated Pytest với Coverage, và Frontend Typecheck/E2E).*

---

## 🔄 5. Lộ Trình Vận Hành 2 Chu Kỳ (Day-0 vs Day-N)

### Chu Kỳ Day-0: Khởi Tạo Dự Án Mới Từ Ý Tưởng Ban Đầu
1. **Tiếp nhận yêu cầu**: Nạp đề bài thô vào Antigravity Chat hoặc chạy qua file brief (`examples/sample_client_brief.md`).
2. **Kích hoạt Sub-Team 1 (Discovery & Solutions)**:
   - `@account-lead` phân rã In-Scope vs Out-of-Scope và T-shirt sizing.
   - `@lead-ba` phỏng vấn tối đa 1-3 câu hỏi P0 bằng công cụ `ask_question`.
   - Xuất bản `docs/specs/<slug>/prd.md` kèm User Stories định dạng Gherkin.
3. **Phê duyệt Gate 1**: Client / PO duyệt Scope và PRD.
4. **Kích hoạt Sub-Team 2 (Architecture & Planning)**:
   - `@system-architect` thiết kế Clean Architecture và ERD.
   - `@security-architect` xây dựng ma trận STRIDE và RBAC.
   - `@tech-planner` xuất bản `plan.md` kèm Cross-Layer Data Contract Matrix.
5. **Phê duyệt Gate 2**: Tech Lead ký duyệt Kiến trúc và Hợp đồng dữ liệu.
6. **Kích hoạt Sub-Team 3 (Core Engineering - 2-Wave Dev)**:
   - Wave 1: `db-dev` + `frontend-dev` (Mock Fixtures) song song.
   - Handshake Gate: Kiểm tra đồng bộ contract trước khi dispatch `backend-dev`.
   - Wave 2: `backend-dev` hoàn thiện live APIs và đồng bộ store.
7. **Kích hoạt Sub-Team 4 (QA & Security Audit)**:
   - Thực thi smoke test 5 tầng, Pytest coverage $\ge 80\%$, và rà soát bảo mật.
   - Vòng lặp Self-Healing tự động sửa lỗi (tối đa 3 lần).
8. **Phê duyệt Gate 3**: Tech Lead xác nhận Production Readiness.
9. **Kích hoạt Sub-Team 5 (Release & Handover)**:
   - Đóng gói bản phát hành `.zip`, mã băm SHA-256, `RELEASE_MANIFEST.json`, `USER_MANUAL.md` và `UAT_CHECKLIST.md`.

### Chu Kỳ Day-N: Bổ Sung Tính Năng Mới Vào Dự Án Đang Chạy
Khi dự án đã có sẵn code và bạn muốn thêm tính năng mới (ví dụ: `payment-gateway`, `notification-center`):
1. **Tạo Feature Slug Mới**:
   - Quy định slug rõ ràng (ví dụ: `vibe-payment`). Mọi hồ sơ của tính năng mới sẽ lưu độc lập tại `docs/specs/vibe-payment/`.
2. **Bảo toàn Mã Nguồn Hiện Hữu (Overwrite Protection)**:
   - Các Subagents đọc `docs/specs/<slug>/plan.md` và kế thừa các models hiện có trong `src/db/models/`, tạo thêm migration mới (vd: `0002_payment.py`) thay vì ghi đè file cũ.
3. **Chạy Lệnh Kiểm Tra Hợp Đồng & Kiểm Thử**:
   ```bash
   make contracts
   make migrations
   make test
   make smoke
   ```
4. **Đóng Gói Bản Phát Hành Tính Năng Mới**:
   ```bash
   python scripts/bundle_release.py vibe-payment 1.1.0
   ```

---

## ⚡ 6. Làn Chạy Cao Tốc (Tactical Fast-Track Cho Bugfix & Micro-Tasks)

Đối với các tác vụ nhỏ, hotfix, sửa 1 endpoint hoặc 1 component trong ngày:
- Kích hoạt qua 1 dòng lệnh duy nhất:
  ```bash
  make task TASK="Sửa lỗi validation số điện thoại trong AuthService"
  # hoặc: make fast-track TASK="..."
  ```
- Fast-Track Squad sẽ:
  1. Phân tích tác động và nhận diện các layer bị ảnh hưởng.
  2. Bỏ qua Gate 1 & 2 để thực hiện sửa đổi cục bộ tối thiểu.
  3. Kiểm tra tính toàn vẹn hợp đồng (`verify_contracts.py`).
  4. Chạy Pytest trọng tâm và tự động lưu checkpoint an toàn.

---

## 🎯 7. Cẩm Nang Bóc Tách Quy Mô Tính Năng (Granular Feature Slicing & Epic Decomposition)

Để kiểm soát token context và giảm thiểu tối đa rủi ro ảo giác, Tech Lead & BA áp dụng giao thức bóc tách quy mô:

### 7.1. Phân Loại T-Shirt Sizing
- **Atomic Feature (Size S / M)**:
  - Quy mô: 3 - 5 Functional Requirements (FRs), 1 - 2 Database Models, 3 - 5 REST endpoints, 1 luồng giao diện chính.
  - Cách xử lý: Thực thi trực tiếp trọn vẹn trong 1 chu trình SDLC (Phase 1 $\to$ 5).
- **Epic / Multi-Domain System (Size L / XL)**:
  - Quy mô: Hệ thống lớn (ví dụ: Toàn bộ E-commerce Platform, Core Banking, Multi-vendor Marketplace).
  - Cách xử lý: **TUYỆT ĐỐI KHÔNG** nhồi nhét vào 1 PRD duy nhất. BA Agent chủ động phân rã thành chuỗi các Feature Slugs nguyên tử độc lập theo Ma trận bóc tách Epic.

### 7.2. Ma Trận Bóc Tách Epic Mẫu
| Thứ tự triển khai | Feature Slug con | Mô tả phạm vi nguyên tử | Độ ưu tiên |
| :--- | :--- | :--- | :--- |
| **Phase 1 (MVP)** | `order-checkout` | Giỏ hàng, đặt hàng cơ bản, bảng orders/items | **P0 (Bắt buộc)** |
| **Phase 2** | `order-payment` | Cổng thanh toán, webhook callback, trạng thái giao dịch | **P1** |
| **Phase 3** | `order-fulfillment` | Điều phối kho, vận chuyển, tracking shipper | **P2** |

---

## 💬 8. Bộ Mẫu Câu Lệnh Thực Chiến Dành Cho Product Owner (PO Prompt Templates)

Khi mở Antigravity 2.0 IDE, người dùng đóng vai trò **Product Owner / Client**, giao tiếp trực tiếp với **Tech Lead Orchestrator**:

### Mẫu Prompt 1: Chạy Full-Flow SDLC (Từ ý tưởng đến bàn giao)
> *"Hãy phát triển tính năng **[Tên tính năng]** (slug: `[feature-slug]`) theo quy trình AI-Vibe-Coding Full-Lifecycle:*
> - *Yêu cầu nghiệp vụ: [Mô tả chi tiết các màn hình, chức năng, user flow]*
> - *Cơ sở dữ liệu: [Các bảng dữ liệu cần tạo, trường chính, quan hệ]*
> - *API: [Các endpoints CRUD hoặc nghiệp vụ cần cung cấp]*
> - *Frontend/Mobile: [Trang giao diện Next.js / Vite hoặc Mobile Expo]*"

### Mẫu Prompt 2: Triệu hồi Trực tiếp Từng Squad Chuyên Biệt (Direct Squad Invocation)
- **Làm rõ yêu cầu / Viết PRD**: *"Nhờ `@lead-ba` phỏng vấn và lập tài liệu PRD cho tính năng mới."*
- **Cần bản thiết kế kỹ thuật**: *"Nhờ `@tech-planner` thiết kế kiến trúc và Cross-Layer Data Contract Matrix."*
- **Sửa Database**: *"Nhờ `@db-dev` thêm index cho cột `sku` bảng `products` và tạo migration Alembic."*
- **Viết thêm API**: *"Nhờ `@backend-dev` thêm endpoint lọc sản phẩm theo khoảng giá."*
- **Làm UI Components**: *"Nhờ `@frontend-dev` làm component ProductFilterBar xử lý đủ 5 trạng thái UI."*
- **Chạy kiểm thử & Audit**: *"Nhờ `@qa-tester` kiểm tra lint và chạy smoke test suite 5 tầng."*
- **Review an ninh & chất lượng**: *"Nhờ `@code-reviewer` audit các thay đổi mới qua git diff theo OWASP Top 10."*
- **Đóng gói phát hành**: *"Nhờ `@release-engineer` đóng gói bản release .zip và tính SHA-256 checksum."*


---

## 🛡️ 9. 11 Nguyên Tắc Sống Còn Cần Nhớ (Best Practices & Guardrails)

1. **Tuyệt đối không xoá thư mục `src/`**:
   - `src/` chứa các điểm neo (Anchor Points) và các file luật cục bộ [src/db/AGENTS.md](src/db/AGENTS.md), [src/backend/AGENTS.md](src/backend/AGENTS.md), [src/frontend/AGENTS.md](src/frontend/AGENTS.md).
2. **Tuân thủ Tuyệt đối Rào Chắn Lệnh & Bảo vệ File Cấu hình Gốc (CLI Guardrails)**:
   - Các tác tử chỉ chạy lệnh trong danh mục Whitelist phân quyền.
   - Subagents tuyệt đối không tự ý sửa đổi file cấu hình gốc (`pyproject.toml`, `docker-compose.yml`, `alembic.ini`, `src/frontend/package.json`). Khi cần thêm thư viện mới, subagent BẮT BUỘC chỉ cắm cờ `[DEPENDENCY REQUIRED]`. Độc quyền Tech Lead Orchestrator chỉnh sửa các file manifest này để tránh race condition trong `Workspace: "inherit"`.
   - Tuyệt đối cấm chạy lệnh cài đặt trần `pip/npm install` trong sandbox.
   - Luôn sử dụng `.venv/bin/pytest` và `.venv/bin/ruff` thay vì gọi lệnh trần.
3. **Phân vùng File Tuyệt đối (File Isolation)**:
   - `db-dev` chỉ ghi `src/db/`.
   - `backend-dev` chỉ ghi `src/backend/`.
   - `frontend-dev` chỉ ghi `src/frontend/` và `src/mobile/`.
   - `qa-tester` & `code-reviewer` không sửa code nghiệp vụ mà báo cáo lại để Dev Squad sửa chữa thông qua vòng lặp phản hồi tự động.
4. **Đồng bộ Hợp đồng Dữ liệu (Contract Synchronization)**:
   - Toàn bộ payload REST API quy định **thống nhất sử dụng `snake_case`**.
   - Mọi thuộc tính phải ánh xạ 1:1 theo Ma trận dữ liệu 3 tầng trong `plan.md`. Không dùng `any` trong TypeScript.
5. **Cơ chế Vòng Lặp Phản Hồi & Ngắt Mạch (Circuit Breaker)**:
   - Mọi phản hồi sửa lỗi tuân thủ giao thức `[SELF-HEALING ACTION REQUIRED]` / `[REVIEW-FIX ACTION REQUIRED]` và `[FIX-COMPLETED]`.
   - Tối đa 3 vòng lặp cho mỗi tính năng. Nếu vượt quá, hệ thống tự động ngắt mạch và báo cáo cho con người xử lý.
6. **Cross-DB Type Safety (UUID & ARRAY)**:
   - UUID khóa chính luôn dùng `from sqlalchemy import Uuid` kèm `default=uuid.uuid4` ở Python (hoặc kế thừa `UUIDPrimaryKeyMixin` từ `src/db/base.py`). Không dùng `server_default=text("gen_random_uuid()")`.
   - Danh sách mảng dùng `from sqlalchemy import JSON` (`default=list`) hoặc variant thay vì `ARRAY` trần để SQLite test không bị fail `CompileError`.
7. **Đồng bộ Mock → Live API**:
   - Trong Wave 1, Frontend sử dụng mock data thông qua `isMockMode()` (`NEXT_PUBLIC_USE_MOCKS=true`).
   - Khi hoàn thành Wave 2, bắt buộc chuyển `NEXT_PUBLIC_USE_MOCKS=false` để kết nối trực tiếp với FastAPI backend live.
8. **Chiến lược Không gian làm việc (`Workspace: "inherit"`)**:
   - Khi gọi `invoke_subagent` cho các Dev Squads, chỉ định `"Workspace": "inherit"` vì ranh giới thư mục hoàn toàn độc lập (`src/db/` vs `src/frontend/`), giúp Wave 2 và QA nhìn thấy code mới ngay lập tức mà không cần merge branch.
9. **Khởi tạo Migration Offline**:
   - Khi không có PostgreSQL container, chạy `PYTHONPATH=src .venv/bin/python src/db/migrations/generate_offline_migration.py <slug>` để tự động tạo file migration chuẩn có revision ID hợp lệ.
10. **Tối ưu Token cho Code Review**:
    - Dùng lệnh lọc `git diff -- src/ docs/ ':!*package-lock.json' ':!*.lock'` để loại bỏ lockfiles, dồn 100% token budget vào thẩm định kiến trúc, N+1 query và bảo mật.
11. **Xử lý Bất đồng bộ Tin nhắn & Chốt Hội tụ Trước QA (Pre-QA Wave Convergence Gate)**:
    - Khi `db-dev` có Schema Drift tại Handshake Gate (`Contract Modified: TRUE`), Tech Lead gửi `[CONTRACT-UPDATE NOTICE]` cho `frontend-dev` qua `send_message`. Nhờ cơ chế hàng đợi phi chặn (non-blocking) của Antigravity 2.0, `frontend-dev` hoàn thành nốt thao tác nguyên tử dở dang rồi mới cập nhật types/mocks và phản hồi `[CONTRACT-ALIGNED]`.
    - Tech Lead không cần chờ Frontend mà kích hoạt ngay `backend-dev` (Wave 2) theo `plan.md v1.1.0`.
    - Trước khi vào Phase 3 (QA Testing), Tech Lead chốt hội tụ: chỉ chuyển `NEXT_PUBLIC_USE_MOCKS=false` và kích hoạt `qa-tester` khi CẢ HAI squad đều hoàn thành nhiệm vụ (`backend-dev` xong live API và `frontend-dev` đã gửi `[CONTRACT-ALIGNED]`).
