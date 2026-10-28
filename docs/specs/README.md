# Thư Mục Hồ Sơ Đặc Tả Kỹ Thuật & Bàn Giao Tính Năng (`docs/specs/`)

Mỗi tính năng mới được phát triển trong **AI-Vibe-Coding (Antigravity 2.0)** được quản lý trong một thư mục chuyên biệt `docs/specs/<feature-slug>/` theo chuẩn **Artifact Handover Schema**. Bộ hồ sơ này là hợp đồng giao tiếp kỹ thuật và bằng chứng nghiệm thu chất lượng giữa các Sub-Teams:

```text
docs/specs/<feature-slug>/
├── prd.md             # [Giai đoạn 0 - Sub-Team 1] Bản đặc tả yêu cầu người dùng, User Stories (Gherkin format)
├── ui_ux_spec.md      # [Giai đoạn 0 - Sub-Team 1] Thiết kế luồng màn hình Mermaid, Design Tokens & 5 UI States
├── plan.md            # [Giai đoạn 1 - Sub-Team 2] Thiết kế kiến trúc, Cross-Layer Contract Matrix & Kịch bản AC
├── test-report.md     # [Giai đoạn 4 - Sub-Team 4] Kết quả kiểm thử tự động 5 tầng & Phiếu báo lỗi Self-Healing
└── review-report.md   # [Giai đoạn 4 - Sub-Team 4] Thẩm định kiến trúc qua git diff, an toàn bảo mật & Điểm chất lượng
```

---

## 1. Chi Tiết Các Tài Liệu Chuyển Giao Chuẩn Hóa

### 1. `prd.md` & `ui_ux_spec.md` — Hồ Sơ Nghiệp Vụ & Trải Nghiệm (Sub-Team 1: Discovery)
- **Tác tử khởi tạo**: `@lead-ba` & `@uiux-designer`.
- **Mẫu tham chiếu**: `templates/specs/prd-template.md`.
- **Mục tiêu**:
  - Ghi nhận kết quả phỏng vấn làm rõ nghiệp vụ qua `ask_question`.
  - Phân tách phạm vi rõ ràng: **In-Scope (MVP)** vs **Out-of-Scope (v2.0)**.
  - User Stories tuân thủ 100% cú pháp Gherkin (`Given - When - Then`).
  - Đặc tả đầy đủ 5 trạng thái giao diện UI: `Default`, `Loading`, `Empty`, `Error`, `Success`.

### 2. `plan.md` — Hợp Đồng Kỹ Thuật Cốt Lõi (Sub-Team 2: Architecture)
- **Tác tử khởi tạo**: `@tech-planner` & `@system-architect`.
- **Mẫu tham chiếu**: `templates/specs/plan-template.md`.
- **Mục tiêu**:
  - **Cross-Layer Data Contract Matrix**: Khóa chặt schema 3 tầng (Database SQLAlchemy $\leftrightarrow$ Backend Pydantic $\leftrightarrow$ Frontend TypeScript) đồng bộ `snake_case`.
  - Đặc tả REST API Endpoints (Path, Method, Request Schema, Response 200/400/500).
  - Phân rã công việc 2-Wave Dev cho Sub-Team 3 (`db-dev`, `frontend-dev` trước, `backend-dev` sau).
  - Ma trận truy xuất nguồn gốc (`AC-ID` $\rightarrow$ `TC-ID`).

### 3. `test-report.md` — Báo Cáo Kiểm Thử Tự Động 5 Tầng (Sub-Team 4: QA)
- **Tác tử khởi tạo**: `@qa-tester`.
- **Mẫu tham chiếu**: `templates/specs/test-report-template.md`.
- **Mục tiêu**:
  - Ghi nhận chỉ số kiểm thử tự động qua `make smoke`: Pytest (FastAPI), Database schema check, Frontend Typecheck, E2E journeys.
  - **Phiếu Báo Lỗi Có Cấu Trúc (Structured Bug Tickets)**: Cung cấp `BUG-ID`, độ nghiêm trọng (`CRITICAL`, `MAJOR`, `MINOR`), file và dòng code vi phạm, traceback thu gọn phục vụ vòng lặp **Self-Healing Loop** (tối đa 3 lần).

### 4. `review-report.md` — Thẩm Định Kiến Trúc & An Toàn Bảo Mật (Sub-Team 4: Review)
- **Tác tử khởi tạo**: `@code-reviewer`.
- **Mẫu tham chiếu**: `templates/specs/review-report-template.md`.
- **Mục tiêu**:
  - Thẩm định `git diff` tập trung vào những thay đổi mới trong `src/` nhằm tối ưu hóa token.
  - Chấm điểm **Quality Scorecard** (Thang điểm 100, yêu cầu tối thiểu $\ge 85/100$).
  - Ra quyết định cuối cùng (**Final Verdict**):
    - `APPROVED`: Cấp phép cho Sub-Team 5 đóng gói bản phát hành `make release`.
    - `CHANGES_REQUESTED`: Yêu cầu kích hoạt vòng sửa lỗi nội bộ.

---

## 2. Tiêu Chuẩn Metadata Header (YAML Frontmatter)

Tất cả tài liệu bàn giao tại `docs/specs/<feature-slug>/` bắt buộc phải có Metadata Header:

```yaml
---
feature_slug: "<feature-slug>"
version: "1.0.0"
artifact_type: "plan" # prd | ui_ux_spec | plan | test-report | review-report
author: "tech-planner" # lead-ba | uiux-designer | tech-planner | qa-tester | code-reviewer
created_at: "YYYY-MM-DDTHH:MM:SSZ"
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
status: "READY_FOR_DEV" # DRAFT | APPROVED_BY_USER | READY_FOR_DEV | IN_DEV | TESTING | REVIEWING | APPROVED | REJECTED
iteration: 1 # Số lần lặp sửa lỗi (tối đa 3)
---
```

---

## 3. Vòng Lặp Phản Hồi Tự Động & Ngắt Mạch (Circuit Breaker Protocol)

1. **Khi test thất bại**:
   - QA xuất bản `test-report.md` với flag `[SELF-HEALING ACTION REQUIRED]`.
   - Dev Squad nhận traceback rút gọn (15-25 dòng qua `scripts/parse_traceback.py`), khắc phục code và gửi `[FIX-COMPLETED]`.
   - `qa-tester` chạy lại bài test. `iteration` tăng thêm 1.
2. **Cơ chế Ngắt Mạch An Toàn**:
   - Giới hạn lặp tối đa: **3 lần** (`MAX_HEALING_LOOPS = 3`).
   - Nếu sau 3 lần sửa vẫn không đạt, hệ thống kích hoạt Circuit Breaker, dừng tiến trình và thông báo cho Tech Lead can thiệp để tránh lãng phí token LLM.
