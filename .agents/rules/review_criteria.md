# Tiêu Chí Thẩm Định Chất Lượng Mã Nguồn (Code Review Criteria)

Principal Code Reviewer (`code-reviewer`) sử dụng hai cấp độ kiểm soát chất lượng dưới đây để đánh giá mã nguồn trước khi cấp phép Gate 3:

---

## 🛑 1. Điều Kiện Tiên Quyết Bắt Buộc (Hard Quality Gates — Pass/Fail)

Bất kỳ vi phạm nào trong bảng này đều dẫn đến **CHANGES_REQUESTED ngay lập tức** (không phụ thuộc vào điểm số tích lũy):

| STT | Tiêu Chí Bắt Buộc | Phân Cấp | Yêu Cầu Tối Thiểu Để Pass | Hậu Quả Nếu Vi Phạm |
| :---: | :--- | :---: | :--- | :--- |
| **1** | **Contract Adherence** | **BẮT BUỘC (Blocker)** | Request/Response payload, kiểu dữ liệu và casing `snake_case` khớp 100% với `plan.md` & `openapi.yaml`. | Tự động REJECT; bắt buộc sửa schema/interface. |
| **2** | **Zero Hardcoded Secrets** | **BẮT BUỘC (Blocker)** | 0 API Keys, Token, Password, Private Key trong source code. Toàn bộ nạp qua `.env` và `pydantic-settings`. | Tự động REJECT; cảnh báo an ninh P0. |
| **3** | **Injection & Auth Safety** | **BẮT BUỘC (Blocker)** | 0 lỗ hổng SQL Injection (100% dùng ORM/Parameterized queries), kiểm tra BOLA ownership (`owner_id == current_user.id`). | Tự động REJECT; vá bảo mật ngay lập tức. |
| **4** | **Test Pass Rate** | **BẮT BUỘC (Blocker)** | 100% test cases trong `pytest` và TypeScript typecheck (`npm run typecheck`) phải PASS, không có regression. | Tự động REJECT; kích hoạt Self-Healing Loop. |

---

## 🎯 1b. Ma Trận Trọng Số Tiêu Chí (Weighted Criteria Matrix — Kế thừa Multi-Agents-Dev)

Phân cấp mức độ ưu tiên và yêu cầu tối thiểu khi thẩm định mã nguồn:

| STT | Tiêu Chí Thẩm Định | Trọng Số | Quy Định Ngưỡng Chấp Thuận | Hướng Xử Lý Khi Vi Phạm |
| :---: | :--- | :---: | :--- | :--- |
| **1** | **Contract Adherence & Casing** | **Bắt buộc** | Request/Response khớp 100% với `plan.md` & `openapi.yaml`. 100% chuẩn `snake_case`. | Blocker: Bắt buộc sửa schema/interfaces trước khi review tiếp. |
| **2** | **Security Guardrails & Secrets** | **Bắt buộc** | 0 hardcoded secrets, 0 SQL Injection, phân quyền RBAC/BOLA đầy đủ. | Blocker: Cảnh báo an ninh P0, yêu cầu vá ngay lập tức. |
| **3** | **Tech Stack & Architecture** | **Trọng số Cao** | Clean Architecture 5 tầng (Backend FastAPI), Next.js 15 / Vite / Expo (Frontend). | Trừ 10 - 20 điểm nếu bypass tầng Service/Repo. |
| **4** | **Test Coverage & Quality** | **Trọng số Cao** | 100% test pass, Code Coverage $\ge 80\%$ (`pytest-cov`). | Trừ 10 điểm nếu thiếu coverage hoặc thiếu test cases biên. |
| **5** | **Clean Code & Readability** | **Trọng số TB** | Tuân thủ PEP 8 (Ruff), ESLint, 5 UI states (Web/Mobile), không có dead code. | Trừ 5 - 10 điểm nếu thiếu chú thích hoặc format bừa bãi. |

---

## 📊 2. Bảng Điểm Chất Lượng Tích Lũy (Thang Điểm 100)

Khi vượt qua toàn bộ Hard Quality Gates, mã nguồn được chấm điểm theo thang 100:

| Tiêu chí | Trọng số | Yêu cầu đạt chuẩn |
| :--- | :--- | :--- |
| **1. Contract Synchronization** | 20 điểm | Khớp 100% field names (`snake_case`), kiểu dữ liệu giữa DB $\leftrightarrow$ Backend $\leftrightarrow$ Frontend. Không có trường thừa/thiếu. |
| **2. Clean Architecture & Modularity** | 20 điểm | Phân tầng rõ ràng. Service không import FastAPI request trực tiếp. Router mỏng, Service chứa nghiệp vụ, Model chứa schema. |
| **3. Performance & N+1 Queries** | 20 điểm | Truy vấn quan hệ phải sử dụng `selectinload` hoặc `joinedload`. Tránh gọi DB lặp trong vòng lặp `for`. |
| **4. Security & Error Handling** | 20 điểm | Không có hardcoded secrets. Lỗi HTTP trả về định dạng chuẩn `{"detail": "..."}`. Có validation đầy đủ qua Pydantic. |
| **5. Frontend Quality & UI States** | 10 điểm | Xử lý đủ 5 trạng thái (Default, Loading, Empty, Error, Success). Responsive trên thiết bị. Không lỗi typecheck. |
| **6. Testing & Coverage ($\ge 80\%$)** | 10 điểm | Unit test đạt tối thiểu **80% coverage** (`pytest-cov`). Có test case Happy Path và Edge Cases. Tên biến rõ nghĩa. |

---

## 🚦 Xếp Loại & Quyết Định (Verdict)

- **APPROVED ($\ge 85$ điểm, Đạt 100% Hard Gates, 0 lỗi P0/P1)**: Đủ điều kiện sang Pha Release & Bàn giao.
- **CHANGES_REQUESTED ($< 85$ điểm hoặc vi phạm bất kỳ Hard Gate nào)**: Kích hoạt vòng lặp Review-Fix (tối đa 3 lần). Dev Squad bắt buộc phải khắc phục các mục bị trừ điểm.

---

## ⚡ Chiến Lược Thẩm Định Tiết Kiệm Token (Token-Optimized Audit Protocol)

Để tối ưu hóa chi phí token, chống tràn context window và tăng tốc độ xử lý khi audit dự án lớn:
1. **Bước 1 — Quét nhanh thay đổi (`git status --short`)**:
   - Nhận diện toàn bộ file mới (untracked `??`) và file sửa đổi (`M`).
2. **Bước 2 — Đo lường quy mô (`git diff --stat`)**:
   - Thống kê số dòng thêm/xóa trên từng file để phân loại file trọng yếu (Models, Routers, Services) vs file cấu hình phụ.
3. **Bước 3 — Thẩm định chi tiết theo từng file mục tiêu (`git diff -- <file>`)**:
   - Chỉ đọc diff của từng file nghiệp vụ cần đánh giá.
   - Loại trừ tự động các file lock hoặc minified:
     ```bash
     git diff -- src/ docs/ ':!*package-lock.json' ':!*.lock' ':!*.min.*'
     ```
   - Không bao giờ gọi `git diff` toàn cục không lọc khi có hơn 15 files thay đổi.
