# Cẩm Nang Hướng Dẫn Sử Dụng AI-Vibe-Coding (USER_GUIDE.md)

Chào mừng bạn đến với **AI-Vibe-Coding** — Template AI Software House vận hành trên nền tảng **Antigravity 2.0**. Cẩm nang này giúp bạn nắm vững cách khởi chạy một dự án mới từ con số 0 (Day-0) và phát triển các tính năng tiếp theo (Day-N).

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
Tôi muốn xây dựng nền tảng MotoCare theo bản đề bài tại @examples/sample_client_brief.md. 
Nhờ Tech Lead khởi động Sub-Team 1 (Discovery Squad) để tiếp nhận và làm rõ yêu cầu!
```

---

## 👥 2. Điều Phối 5 Sub-Teams Trong Quá Trình Phát Triển

### Giai đoạn 0: Tiếp Nhận & Thiết Lập PRD (Sub-Team 1)
- Tech Lead sẽ triệu hồi `@account-lead` để bóc tách phạm vi và `@lead-ba` để phỏng vấn bạn.
- Bạn sẽ nhận được 1-3 câu hỏi trắc nghiệm qua công cụ `ask_question`. Sau khi chọn đáp án, `@lead-ba` xuất bản `docs/specs/<feature-slug>/prd.md` và `@uiux-designer` xuất bản `ui_ux_spec.md`.
- 👉 **Quality Gate 1**: Bạn xem tài liệu tóm tắt trên tab Artifacts của Antigravity. Nếu đồng ý, phê duyệt `APPROVED`. Hệ thống tự động lưu checkpoint:
  ```bash
  make checkpoint PHASE=gate_1_prd NOTE="Client duyệt PRD"
  ```

### Giai đoạn 1: Thiết Kế Kỹ Thuật & Hợp Đồng Dữ Liệu (Sub-Team 2)
- `@system-architect` thiết kế ERD và sơ đồ phân tầng.
- `@security-architect` phân tích nguy cơ STRIDE.
- `@tech-planner` xuất bản `docs/specs/<feature-slug>/plan.md` với **Cross-Layer Contract Matrix**.
- 👉 **Quality Gate 2**: Tech Lead kiểm tra tính nhất quán và phê duyệt chuyển sang coding:
  ```bash
  make checkpoint PHASE=gate_2_architecture NOTE="Duyệt ERD & Contract Matrix"
  ```

### Giai đoạn 2 & 3: Lập Trình Đợt Kép (Sub-Team 3 - Dev Squad)
- **Wave 1**: `@db-dev` sinh Models và Migrations; `@frontend-dev` sinh giao diện với Mock Fixtures.
- **Handshake Gate**: Tech Lead kiểm tra cú pháp models và types.
- **Wave 2**: `@backend-dev` sinh Pydantic schemas, Services và REST APIs; `@devops-engineer` cấu hình Docker.
- 👉 Lưu checkpoint sau khi code xong:
  ```bash
  make checkpoint PHASE=engineering NOTE="Hoàn thành Wave 1 & 2"
  ```

### Giai đoạn 4 & 5: Kiểm Thử Tự Động & Thẩm Định Code (Sub-Team 4)
- `@qa-tester` chạy bộ kiểm thử 5 tầng (`make smoke`).
- Nếu có lỗi, vòng lặp **Self-Healing** tự động kích hoạt (tối đa 3 lần với log được cắt tỉa 15-25 dòng qua `scripts/parse_traceback.py`).
- `@code-reviewer` audit diff và chấm điểm trên thang 100 (`make contracts`).
- 👉 **Quality Gate 3**: Khi điểm $\ge 85/100$ và 100% tests pass, cấp phép phát hành:
  ```bash
  make checkpoint PHASE=gate_3_deploy NOTE="Pass 5 tầng tests & điểm review >= 85"
  ```

### Giai đoạn 6: Đóng Gói & Bàn Giao Khách Hàng (Sub-Team 5)
- `@release-engineer` chạy `make release` để tạo gói `.zip` và `RELEASE_MANIFEST.json` trong `dist/releases/`.
- `@tech-writer` soạn thảo `USER_MANUAL.md` và `DEPLOYMENT.md`.
- `@handover-lead` cung cấp `UAT_CHECKLIST.md` và hướng dẫn bạn chạy thử ứng dụng một chạm (`make docker-up` hoặc `make dev`).
- 👉 Lưu checkpoint hoàn tất:
  ```bash
  make checkpoint PHASE=completed NOTE="Bàn giao sản phẩm hoàn tất"
  ```

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

---

## 🛠️ 5. Bảng Phím Tắt Lệnh 1-Chạm (Makefile Cheatsheet)

| Lệnh | Ý nghĩa |
| :--- | :--- |
| `make dev` | Khởi chạy FastAPI Backend với chế độ hot-reload trên cổng 8000. |
| `make test` | Chạy toàn bộ unit tests trên SQLite in-memory cô lập. |
| `make smoke` | Chạy trọn vẹn bộ kiểm thử 5 tầng (Linter, Contract, Migration, Pytest, Typecheck). |
| `make contracts` | Quét kiểm tra đồng bộ trường dữ liệu (`snake_case`) giữa 3 tầng. |
| `make migrations`| Kiểm tra đồ thị phân nhánh Alembic Migration DAG. |
| `make seed` | Nạp dữ liệu mẫu ban đầu vào database. |
| `make release` | Đóng gói bản phát hành `.zip` kèm checksum manifest. |
| `make docker-up` | Khởi chạy toàn bộ hệ thống bằng Docker Compose. |
| `make clean` | Dọn dẹp sạch cache và bytecode rác. |
| **`make frontend-status`** | Kiểm tra trạng thái framework Web & Mobile hiện tại. |
| **`make preset-vite`** | Chuyển đổi Web Frontend sang React + Vite. |
| **`make preset-nextjs`** | Chuyển đổi Web Frontend sang Next.js 15 SSR. |
| **`make add-mobile`** | Khởi tạo ứng dụng Mobile React Native Expo trong `src/mobile/`. |
| **`make checkpoint`** | Lưu Checkpoint trạng thái kèm snapshot mã nguồn. |
| **`make checkpoints`** | Hiển thị bảng danh sách các checkpoint đã lưu. |
| **`make resume`** | Hiển thị vị trí dừng và chỉ dẫn bước kế tiếp cho Tech Lead. |
| **`make restore ID=...`**| Rollback mã nguồn về checkpoint đã lưu. |
