---
name: requirement_elicitation
description: "Instructions for Lead BA on conducting high-leverage user interviews using ask_question, parsing raw user requests into SMART objectives, feature slicing (Atomic S/M/L), and formatting Gherkin user stories."
---

# Requirement Elicitation & PRD Formulation Skill

Kỹ năng này hướng dẫn `lead-ba` và `account-lead` thực hiện phỏng vấn làm rõ yêu cầu khách hàng và lập tài liệu PRD chuẩn hóa:

---

## 1. Phân Định Trách Nhiệm: Lead BA (`lead-ba`) vs Tech Planner (`tech-planner`)

Để tránh chồng chéo nhiệm vụ và đảm bảo tính mạch lạc xuyên suốt pipeline:

| Tiêu chí | Lead BA (`lead-ba`) | Tech Planner (`tech-planner`) |
| :--- | :--- | :--- |
| **Câu hỏi cốt lõi** | **WHAT & WHY**: Tính năng này giải quyết vấn đề gì? Ai dùng? Quy tắc nghiệp vụ ra sao? | **HOW**: Hệ thống cài đặt như thế nào? Bảng DB nào? API schema nào? Component nào? |
| **Đối tượng phỏng vấn** | Phỏng vấn trực tiếp Người dùng (End User / Product Owner) qua `ask_question`. | Tra cứu PRD và khảo sát codebase kỹ thuật, không làm phiền người dùng về tiểu tiết. |
| **Đầu vào (Input)** | Prompt / Yêu cầu ban đầu từ người dùng (thường mơ hồ, ngắn gọn, thiếu edge cases). | Tài liệu PRD (`docs/specs/<feature-slug>/prd.md`) đã được người dùng nghiệm thu. |
| **Sản phẩm bàn giao** | `docs/specs/<feature-slug>/prd.md` (FRs, BRs, Personas, User Journeys, Edge Cases, BACs). | `docs/specs/<feature-slug>/plan.md` (Cross-layer Data Matrix, API Spec, UI Spec, AC/TC Matrix). |
| **Ranh giới cấm** | Không quyết định tên cột DB, cú pháp code, thư viện kỹ thuật. | Không tự ý thay đổi quy tắc nghiệp vụ hoặc phạm vi đã chốt trong PRD. |

---

## 2. Giao Thức Đánh Giá Quy Mô & Bóc Tách Epic (Granular Feature Slicing Protocol)

Trước khi đi sâu vào chi tiết, BA Agent bắt buộc phải định cỡ (T-Shirt Sizing) yêu cầu của người dùng:
- **Nguyên tắc "Atomic Slice" (Lát cắt Nguyên tử)**: Một chu trình Dev chỉ nên xử lý một phạm vi rõ ràng:
  - **Size S (Small)**: 1 resource, 2-3 endpoints CRUD cơ bản, 1 màn hình.
  - **Size M (Medium)**: 2-3 resources liên kết, quy tắc nghiệp vụ rẽ nhánh, 2 màn hình.
  - **Size L/Epic**: Hệ thống đa phân hệ $\to$ BẮT BUỘC bóc tách thành các Slice nhỏ hơn (Phase 1 MVP, Phase 2 Advanced) để thực thi từng bước an toàn.

### 2.1. Quy Tắc Chống Phình Phạm Vi & Bóc Tách Epic Tuần Tự (Anti-Bloat & Granular Slicing)
1. **Tuyệt đối không nhồi nhét (Anti-Bloat Rule)**: Không cố gắng gom toàn bộ một hệ thống lớn (Epic) vào duy nhất một tài liệu `prd.md`. Nhồi nhét quá nhiều nghiệp vụ vào một context window sẽ làm cạn kiệt context, gây ra ảo giác (hallucination) và làm suy giảm độ chính xác của các agent kỹ thuật phía sau.
2. **Kỹ thuật bóc tách thành chuỗi `<feature-slug>` độc lập tuần tự**:
   - Thay vì yêu cầu chung chung "Xây dựng sàn thương mại điện tử" (`ecommerce-full`), BA Agent hướng dẫn khách hàng chia nhỏ thành chuỗi các tính năng hạt nhân (Atomic Slices):
     * `01-catalog-browsing`: Duyệt danh mục, tìm kiếm và xem chi tiết sản phẩm.
     * `02-cart-management`: Thêm/sửa/xóa giỏ hàng và tính giá tạm tính.
     * `03-checkout-flow`: Nhập địa chỉ giao hàng, áp mã giảm giá và chọn phương thức vận chuyển.
     * `04-payment-webhook`: Tích hợp cổng thanh toán trực tuyến và lắng nghe webhook.
   - Mỗi `<feature-slug>` sở hữu riêng một thư mục hồ sơ: `docs/specs/<feature-slug>/prd.md`, `plan.md`, `test-report.md`.
3. **Mỗi chu trình chỉ giải quyết một Atomic Slice**: Chỉ khi Slice trước vượt qua Quality Gate 3 và nghiệm thu bàn giao, mới tiến hành kích hoạt Slice kế tiếp.

---

## 3. Nguyên Tắc Phỏng Vấn (High-Leverage Interview) & Ma Trận Điểm Mù (Blind Spot Matrix)
- Chỉ đặt tối đa **1 đến 3 câu hỏi P0 then chốt**.
- Câu hỏi phải liên quan đến:
  1. Phạm vi MVP (Những gì BẮT BUỘC có trong phiên bản này).
  2. Phân quyền và người dùng mục tiêu (Ai dùng chức năng này, phân biệt User vs Admin).
  3. Quy tắc rẽ nhánh cốt lõi (Nếu gặp trường hợp ngoại lệ, hệ thống phản ứng ra sao).
- Gom câu hỏi thành trắc nghiệm, đánh dấu `(Recommended)` ở phương án tối ưu nhất.

### 3.1. Ma Trận Phát Hiện Điểm Mù Nghiệp Vụ (Blind Spot Matrix)
Khi tiếp nhận yêu cầu từ người dùng, BA Agent chủ động rà soát 4 điểm mù sau để phát hiện rủi ro:
1. **Scope Boundary (Phạm vi ranh giới)**:
   - *Vấn đề*: Người dùng yêu cầu "Làm tính năng quản lý sản phẩm".
   - *Cần làm rõ*: MVP có bao gồm quản lý kho, nhập hàng, biến thể sản phẩm (màu sắc, kích cỡ) không, hay chỉ là CRUD sản phẩm cơ bản?
2. **Actor & Permission (Tác nhân & Quyền hạn)**:
   - *Vấn đề*: "Người dùng có thể xóa bài viết".
   - *Cần làm rõ*: Bất kỳ người dùng nào hay chỉ tác giả của bài viết? Admin có quyền xóa không? Có cơ chế Soft Delete (thùng rác) để phục hồi không?
3. **Data Constraints & Business Rules (Ràng buộc dữ liệu & Quy tắc)**:
   - *Vấn đề*: "Người dùng nhập mã giảm giá".
   - *Cần làm rõ*: Mã giảm giá có phân biệt hoa/thường không? Một đơn hàng áp dụng tối đa bao nhiêu mã? Có áp dụng đồng thời với khuyến mãi khác không?
4. **Edge Cases & Failure Behavior (Hành vi khi có lỗi)**:
   - *Vấn đề*: Người dùng bấm lưu dữ liệu khi mất mạng hoặc server chậm.
   - *Cần làm rõ*: Hệ thống hiển thị cảnh báo gì? Có tự động lưu bản nháp vào LocalStorage không? Có cơ chế Retry không?

---

## 4. Định Dạng User Story Chuẩn Gherkin
Mỗi User Story phải có cấu trúc:
```gherkin
Feature: <Tên tính năng>
  As a <Role/Persona>
  I want to <Action>
  So that <Business Value>

  Scenario: <Happy Path Scenario>
    Given <Tiền điều kiện>
    When <Hành động của người dùng>
    Then <Kết quả mong đợi>

  Scenario: <Edge Case 1 - Dữ liệu không hợp lệ>
    Given ...
    When ...
    Then ...

  Scenario: <Edge Case 2 - Xung đột hoặc mất kết nối>
    Given ...
    When ...
    Then ...
```

---

## 5. Bóc Tách Văn Bản Thô & Phát Hiện Vùng Mờ (Unstructured Text Parsing)
Khi nhận brief thô từ khách hàng (email, chat, biên bản họp):
1. **Trích xuất Thực thể & Hạn mức cốt lõi (Domain Entities & Capacity Rules):**
   - Xác định danh từ trung tâm: Khách hàng, Đơn hàng, Lịch hẹn, Xe, Sản phẩm.
   - Trích xuất các số liệu giới hạn: "tối đa N xe", "trong mỗi khung giờ", "hạn thanh toán trong M phút".
2. **Liệt kê Tác nhân (Personas & Roles):**
   - Phân biệt rõ vai trò: Khách vãng lai, Người dùng đã đăng ký, Nhân viên kỹ thuật, Quản trị viên (Admin).
3. **Phát hiện Vùng mờ & Mâu thuẫn logic (Ambiguity Detection):**
   - Thiếu luồng xử lý thất bại (Thanh toán lỗi, hết slot, hủy lịch sát giờ).
   - Thiếu tiêu chí phi chức năng (NFRs: Tốc độ phản hồi < 500ms, dung lượng tải file).
4. **Chuyển hóa thành Câu hỏi P0 cho `ask_question`:**
   - Không hỏi những chi tiết kỹ thuật hiển nhiên.
   - Chỉ phỏng vấn các điểm rẽ nhánh quyết định mô hình dữ liệu (ERD) hoặc phạm vi nghiệp vụ (Scope).

---

## 6. Tiêu Chuẩn Soạn Thảo Metadata Header PRD (`docs/specs/<feature-slug>/prd.md`)

Tài liệu PRD phải bắt đầu bằng khối Metadata Header chuẩn hóa:
```yaml
---
feature_slug: "<feature-slug>"
version: "1.0.0"
artifact_type: "prd"
author: "lead-ba"
created_at: "YYYY-MM-DDTHH:MM:SSZ"
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
status: "DRAFT" # DRAFT -> PENDING_REVIEW -> APPROVED_BY_USER
iteration: 1
---
```

---

## 7. Tiêu Chuẩn Viết FRs & Business Acceptance Criteria (BACs)

### 7.1. Tiêu chuẩn viết Yêu cầu chức năng (FRs):
- Đặt mã định danh duy nhất: `FR-01`, `FR-02`, `FR-03`...
- Mỗi FR phải độc lập, kiểm thử được và nêu rõ hành vi hệ thống:
  - *Ví dụ tốt*: `FR-01: Hệ thống cho phép người dùng lọc danh sách giao dịch theo khoảng ngày (Từ ngày - Đến ngày) với kết quả cập nhật theo thời gian thực.`
  - *Ví dụ xấu*: `FR-01: Làm bộ lọc xịn sò.`

### 7.2. Tiêu chuẩn viết Tiêu chí nghiệm thu nghiệp vụ (BACs):
Áp dụng cấu trúc **Given - When - Then** chuẩn Agile cho từng quy tắc nghiệp vụ rẽ nhánh:
```markdown
### BAC-01: Xác thực mã giảm giá hợp lệ
- **Given**: Người dùng đã thêm sản phẩm vào giỏ hàng với tổng giá trị đạt tối thiểu 200,000 VNĐ.
- **When**: Người dùng nhập mã "GIAM50K" và bấm "Áp dụng".
- **Then**: Hệ thống trừ 50,000 VNĐ vào tổng thanh toán, hiển thị nhãn xanh "Đã áp dụng mã GIAM50K", và cập nhật số tiền cần trả.

### BAC-02: Giới hạn số lượng đơn hàng vượt công suất phục vụ (Capacity Rule)
- **Given**: Khung giờ 09:00 - 10:00 đã đạt tối đa 5 xe đặt lịch bảo dưỡng.
- **When**: Khách hàng chọn đặt lịch bảo dưỡng mới vào khung giờ 09:00 - 10:00.
- **Then**: Hệ thống hiển thị cảnh báo "Khung giờ đã kín chỗ, vui lòng chọn khung giờ khác", vô hiệu hóa nút xác nhận đặt lịch.
```

---

## 8. Quy Trình Phê Duyệt PRD Sign-off Gate (Gate 1)

1. **Soạn thảo xong bản thảo PRD**: Thiết lập `status: "DRAFT"`.
2. **Trình bày tóm tắt cho User**: Tóm lược phạm vi In-Scope, Out-of-Scope, Business Rules chính và các BACs.
3. **Xin xác nhận Sign-off**: Sử dụng `ask_question` hoặc tương tác trực tiếp với User để lấy xác nhận: "Bạn có đồng ý với bản PRD này để chuyển sang giai đoạn thiết kế kỹ thuật (Planning) không?".
4. **Cập nhật trạng thái**: Khi User đồng ý, cập nhật `status: "APPROVED_BY_USER"`.
5. **Kích hoạt Sub-Team 2**: Thông báo chuyển giao hồ sơ `docs/specs/<feature-slug>/prd.md` cho `system-architect` và `tech-planner`.

