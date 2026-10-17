# Cẩm Nang Tùy Biến & Vận Hành Template (TEMPLATE_GUIDE.md)
### Hướng Dẫn Tận Dụng Sức Mạnh Của AI-Vibe-Coding Cho Mọi Dự Án

Tài liệu này cung cấp hướng dẫn chuyên sâu cho **Tech Lead, Product Owner và AI Developers** về cách tùy biến, mở rộng và khai thác template **AI-Vibe-Coding** từ ngày đầu tiên (Day-0) đến chu kỳ mở rộng lâu dài (Day-N).

---

## 🚀 1. Lộ Trình Vận Hành 2 Chu Kỳ (Day-0 vs Day-N)

### Chu Kỳ Day-0: Khởi Tạo Dự Án Mới Từ Ý Tưởng Ban Đầu
1. **Chuẩn bị cấu hình**:
   ```bash
   cp .env.example .env
   ```
2. **Nạp Đề bài thô vào Antigravity Chat Canvas**:
   - Bạn chỉ cần dán yêu cầu hoặc trỏ tới file brief (như `@examples/sample_client_brief.md`).
3. **Kích hoạt Sub-Team 1**:
   - Tech Lead sẽ gọi `@account-lead` để phân rã phạm vi và `@lead-ba` để phỏng vấn 1-3 câu hỏi then chốt qua `ask_question`.
4. **Phê duyệt Gate 1 & Gate 2**:
   - Duyệt PRD và Plan trên tab Artifacts.
5. **Chạy 2-Wave Dev & Nghiệm thu Gate 3**:
   - Dev Squad hoàn thiện code, QA kiểm thử 5 tầng, Reviewer cấp phép và Release Squad xuất bản gói `.zip`.

### Chu Kỳ Day-N: Bổ Sung Tính Năng Mới Vào Dự Án Đang Chạy
Khi dự án đã có sẵn code và bạn muốn thêm tính năng mới (ví dụ: `payment-gateway`, `notification-center`):
1. **Tạo Feature Slug Mới**:
   - Quy định slug rõ ràng (ví dụ: `vibe-payment`). Mọi hồ sơ của tính năng mới sẽ lưu độc lập tại `docs/specs/vibe-payment/`.
2. **Bảo toàn Mã Nguồn Hiện Hữu (Overwrite Protection)**:
   - Các Subagents đọc `docs/specs/<slug>/plan.md` và kế thừa các models hiện có trong `src/db/models/`, tạo thêm migration mới (vd: `0002_payment.py`) thay vì ghi đè file cũ.
3. **Chạy Lệnh Kiểm Tra Hợp Đồng**:
   ```bash
   make contracts
   make migrations
   make smoke
   ```
4. **Đóng Gói Tính Năng Mới**:
   ```bash
   python scripts/bundle_release.py vibe-payment 1.1.0
   ```

---

## ⚙️ 2. Tùy Biến Công Nghệ (Tech Stack Customization)

Mặc định, template cung cấp **Golden Stack** chuẩn mực:
- **Backend**: Python 3.11+ / FastAPI / Pydantic v2 / Clean Architecture.
- **ORM / DB**: SQLAlchemy 2.0 Async / PostgreSQL 16 / Alembic / SQLite in-memory isolated tests.
- **Frontend**: Next.js 15 (React 19) & React Native Expo (NativeWind Tailwind).

Nếu bài toán của bạn yêu cầu stack khác (ví dụ: Web SPA thuần React Vite, hoặc chỉ Backend API không cần Mobile):
1. **Điều chỉnh `config/company_profile.yaml`**: Cập nhật mục `engineering_standards` tương ứng.
2. **Bật/Tắt thư mục Client**:
   - Nếu dự án chỉ là Web: Bạn có thể bỏ qua thư mục `src/mobile/`. Script `verify_contracts.py` sẽ tự động phát hiện và chỉ quét `src/frontend/`.
   - Nếu dự án là Mobile-First: Bạn tập trung vào `src/mobile/`.

---

## 🧠 3. Tinh Chỉnh Định Tuyến Mô Hình (Model Router Tuning)

File `config/model_router.yaml` phân bổ mô hình AI tối ưu:
- Nếu bạn có tài khoản **Gemini 2.5 Pro** với hạn ngạch lớn: Bạn có thể nâng `tier: "pro"` cho cả Dev Squad để sinh code phức tạp sâu hơn.
- Nếu bạn muốn **tiết kiệm tối đa chi phí (Budget Mode)**:
  - Giữ `lead-ba`, `system-architect`, và `code-reviewer` ở mức `pro`.
  - Toàn bộ các tác tử còn lại chuyển sang `flash` hoặc `flash_lite`. Giúp giảm đến 80% chi phí token.

---

## 🔒 4. Tích Hợp CI/CD & Triển Khai Cloud

Dự án đã tích hợp sẵn GitHub Actions workflow tại [`.github/workflows/ci.yml`](.github/workflows/ci.yml):
- Mọi Pull Request hoặc Push vào `main` sẽ tự động kích hoạt 5 tầng kiểm tra.
- Khi triển khai lên Cloud (AWS ECS, Google Cloud Run, hoặc DigitalOcean):
  - Khởi chạy nhanh bằng Docker: `docker compose up --build -d`.
  - Backend API sẽ phục vụ tại port 8000 kèm Swagger UI tại `/api/v1/docs`.
