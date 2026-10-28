---
feature_slug: "<feature-slug>"
version: "1.0.0"
artifact_type: "review-report"
reviewer: "Principal Code Reviewer (code-reviewer)"
created_at: "YYYY-MM-DDTHH:MM:SSZ"
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
verdict: "APPROVED | CHANGES_REQUESTED"
score: "<Total-Score>/100" # Yêu cầu >= 85/100 để APPROVED
iteration: 1 # Vòng lặp review (1 -> 3)
findings_summary:
  critical: 0
  major: 0
  minor: 0
  nit: 0
---

# Principal Code Review & Security Audit Report: `<Feature Name>`

> **Báo cáo Thẩm định Kiến trúc & Bảo mật Độc lập**: Đánh giá toàn diện các thay đổi mã nguồn mới trong `src/` qua phân tích `git diff`, đối chiếu trực tiếp với `plan.md` và `test-report.md`.

---

## 1. Bảng Điểm Chất Lượng Chi Tiết (100-Point Quality Gate Scorecard)

| Tiêu chí Kiểm định | Trọng số | Điểm đạt | Nhận xét chi tiết & Đối chiếu |
| :--- | :---: | :---: | :--- |
| **1. Contract Synchronization** | 20đ | .../20 | 100% khớp snake_case giữa DB ↔ Backend ↔ Frontend/Mobile, zero drift |
| **2. Clean Architecture & Modularity** | 20đ | .../20 | Phân tầng rõ ràng, Service độc lập framework, Repository chuẩn |
| **3. Performance & N+1 Queries** | 20đ | .../20 | Dùng `selectinload`/`joinedload`, đánh index foreign keys đầy đủ |
| **4. Security, STRIDE & Error Handling** | 20đ | .../20 | Zero hardcoded secrets, Pydantic v2 length limits, HTTP error chuẩn `{"detail": "..."}` |
| **5. Frontend/Mobile Quality & UI States** | 10đ | .../10 | Xử lý trọn vẹn 5 trạng thái (Default, Loading, Empty, Error, Success), strict TS (0 `any`) |
| **6. Testing Integrity & Maintainability** | 10đ | .../10 | 100% test cases PASSED, độ phủ $\ge 80\%$, test Happy Path + 2 Edge Cases |
| **TỔNG ĐIỂM** | **100đ** | **.../100** | **Xếp loại: APPROVED ($\ge 85$đ) hoặc CHANGES_REQUESTED ($< 85$đ)** |

---

## 2. Phạm Vi Mã Nguồn Được Audit (Git Diff Scope)

```text
# Git Status & Diff Summary (Token-Optimized Audit):
src/db/...                |  +X -Y
src/backend/...           |  +X -Y
src/frontend/...          |  +X -Y
src/mobile/...            |  +X -Y
X files changed, Y insertions(+), Z deletions(-)
```

---

## 3. Danh Sách Phát Hiện Chi Tiết (Structured Finding Tickets)

> 💡 **Phân loại mức độ nghiêm trọng**:
> - `[CRITICAL]`: Lỗ hổng bảo mật nghiêm trọng (OWASP Top 10), nguy cơ mất dữ liệu, lộ secrets, hoặc phá vỡ Hợp đồng API Contract (Bắt buộc sửa trước khi cấp phép Gate 3).
> - `[MAJOR]`: Lỗi N+1 query tiềm ẩn, thiếu transaction rollback, dùng ép kiểu `any` trong TypeScript, thiếu validation giới hạn độ dài Pydantic (Bắt buộc sửa).
> - `[MINOR]`: Code smell, cú pháp chưa tối ưu, thiếu comment giải thích logic phức tạp (Khuyến nghị sửa).
> - `[NIT]`: Đề xuất cải thiện phong cách code hoặc đặt tên biến rõ ràng hơn (Tùy chọn).

### [REV-01] `<Tiêu đề phát hiện ngắn gọn>`
- **Mã Phát hiện**: `REV-01`
- **Mức độ (Severity)**: `CRITICAL` | `MAJOR` | `MINOR` | `NIT`
- **Phân loại (Category)**: `Contract Alignment` | `Security / OWASP` | `Performance & N+1` | `Type Safety` | `Clean Architecture`
- **Tác tử Phụ trách (Target Agent)**: `db-dev` (`src/db/`) | `backend-dev` (`src/backend/`) | `frontend-dev` (`src/frontend/`, `src/mobile/`)
- **Vị trí Phát hiện (Target File & Line)**: `src/.../file.py#L42-L55`
- **Đoạn Code Vi phạm (Diff Evidence)**:
  ```python
  # Trích xuất 5-10 dòng code vi phạm
  ```
- **Lý do Vi phạm (Violation Rationale)**:
  - <Mô tả chi tiết nguyên nhân vi phạm tiêu chuẩn kỹ thuật>
- **Hướng dẫn Khắc phục (Actionable Remediation)**:
  - <Chỉ dẫn cụ thể cho Dev Squad sửa đúng dòng vi phạm bằng replace_file_content>

---

## 4. Quyết Định Nghiệm Thu (Quality Gate 3 Verdict)

- **Quyết định Cuối cùng (Final Verdict)**: `APPROVED` | `CHANGES_REQUESTED`
- **Tổng Điểm Đạt Được**: `.../100`

### Quy trình Xử lý Tiếp theo:
- **Nếu `APPROVED` ($\ge 85$ điểm, 0 lỗi CRITICAL/MAJOR)**: Cấp phép chuyển sang Pha 5 (Release, Đóng gói Bundle ZIP & Bàn giao).
- **Nếu `CHANGES_REQUESTED` ($< 85$ điểm hoặc có lỗi CRITICAL/MAJOR)**:
  - Kích hoạt vòng lặp **Review-Fix Action** (tối đa 3 vòng lặp).
  - Dev Squad khắc phục theo hướng dẫn tại Mục 3 và gửi lại để `code-reviewer` tái thẩm định.
