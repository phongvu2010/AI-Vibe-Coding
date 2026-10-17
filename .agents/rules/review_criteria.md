# Tiêu Chí Thẩm Định Chất Lượng Mã Nguồn (Code Review Criteria)

Principal Code Reviewer (`code-reviewer`) sử dụng bảng điểm chấm chất lượng (Quality Scorecard) dưới đây để đánh giá mã nguồn trước khi cấp phép Gate 3:

---

## 📊 Bảng Điểm Chất Lượng (Thang Điểm 100)

| Tiêu chí | Trọng số | Yêu cầu đạt chuẩn |
| :--- | :--- | :--- |
| **1. Contract Synchronization** | 20 điểm | Khớp 100% field names (`snake_case`), kiểu dữ liệu giữa DB $\leftrightarrow$ Backend $\leftrightarrow$ Frontend. Không có trường thừa/thiếu. |
| **2. Clean Architecture & Modularity** | 20 điểm | Phân tầng rõ ràng. Service không import FastAPI request trực tiếp. Router mỏng, Service chứa nghiệp vụ, Model chứa schema. |
| **3. Performance & N+1 Queries** | 20 điểm | Truy vấn quan hệ phải sử dụng `selectinload` hoặc `joinedload`. Tránh gọi DB lặp trong vòng lặp `for`. |
| **4. Security & Error Handling** | 20 điểm | Không có hardcoded secrets. Lỗi HTTP trả về định dạng chuẩn `{"detail": "..."}`. Có validation đầy đủ qua Pydantic. |
| **5. Frontend Quality & UI States** | 10 điểm | Xử lý đủ 5 trạng thái (Default, Loading, Empty, Error, Success). Responsive trên thiết bị. Không lỗi typecheck. |
| **6. Testing & Maintainability** | 10 điểm | Có test case Happy Path và Edge Cases. Code có chú thích logic phi trực quan, tên biến rõ nghĩa. |

---

## 🚦 Xếp Loại & Quyết Định (Verdict)

- **APPROVED ($\ge 85$ điểm, 0 lỗi P0/P1)**: Đủ điều kiện sang Pha Release & Bàn giao.
- **CHANGES_REQUESTED ($< 85$ điểm hoặc có lỗi bảo mật/N+1)**: Kích hoạt vòng lặp Review-Fix (tối đa 3 lần). Dev Squad bắt buộc phải khắc phục các mục bị trừ điểm.
