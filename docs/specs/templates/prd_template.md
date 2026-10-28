---
feature_slug: "<feature-slug>"
version: "1.0.0"
artifact_type: "prd"
author: "lead-ba"
created_at: "YYYY-MM-DDTHH:MM:SSZ"
updated_at: "YYYY-MM-DDTHH:MM:SSZ"
status: "DRAFT" # DRAFT | PENDING_REVIEW | APPROVED_BY_USER
iteration: 1
---

# Product Requirements Document (PRD): `<Tên Tính Năng>`

> **Chủ sở hữu**: `@lead-ba` (Business Analyst & Requirements Engineer)  
> **Chốt chặn phê duyệt**: **GATE 1: Client / Product Owner Sign-off** (`review_gate_1_prd.md`)  
> **Nguyên tắc**: Bám sát mục tiêu SMART, bóc tách Epic thành Atomic Features (Size S/M), làm rõ 100% điểm mơ hồ qua phỏng vấn tương tác (`ask_question`).

---

## 1. Tổng Quan & Mục Tiêu Kinh Doanh (Executive Summary & Objectives)

### 1.1. Bối cảnh & Vấn đề Cần Giải Quyết (Problem Statement)
- **Vấn đề thực tế**: <Mô tả chi tiết khó khăn của người dùng hoặc điểm nghẽn quy trình nghiệp vụ>
- **Giải pháp đề xuất**: <Mô tả tính năng phần mềm sẽ giải quyết vấn đề như thế nào>

### 1.2. Mục tiêu SMART & Chỉ Số Đo Lường (SMART Goals & KPIs)
- **Specific**: <Mục tiêu chức năng cụ thể và ranh giới rõ ràng>
- **Measurable**: <Chỉ số định lượng: e.g. Tỷ lệ hoàn tất > 95%, thời gian phản hồi < 200ms>
- **Achievable**: <Khả năng triển khai khả thi với Tech Stack hiện có>
- **Relevant**: <Phù hợp với mục tiêu kinh doanh cốt lõi của sản phẩm>
- **Time-bound**: <Thời hạn hoàn thành và nghiệm thu>

### 1.3. Ma Trận Bóc Tách Quy Mô (Epic Decomposition Matrix)
> [!NOTE]
> Tuyệt đối không nhồi nhét cả một Epic lớn (Size L/XL) vào một PRD duy nhất. BA chủ động bóc tách thành các lát cắt nguyên tử độc lập (Atomic Features - Size S/M).

| Mã Lát Cắt | Tên Tính Năng Nguyên Tử | Quy Mô | Độ Ưu Tiên | Thuộc Phạm Vi Này? | Phụ Thuộc (Depends on) |
| :---: | :--- | :---: | :---: | :---: | :--- |
| `<slug>-p0` | <Tính năng cốt lõi MVP> | Size S/M | P0 (Must-have) | **CÓ (In-Scope)** | Không |
| `<slug>-p1` | <Tính năng nâng cao đợt 2> | Size M | P1 (Should-have) | Ngoài phạm vi | `<slug>-p0` |
| `<slug>-p2` | <Báo cáo / Tối ưu hóa> | Size L | P2 (Nice-to-have) | Ngoài phạm vi | `<slug>-p1` |

---

## 2. Chân Dung Người Dùng & Phân Quyền (Personas & Permissions)

| Persona (Vai Trò) | Quyền hạn Hệ thống | Mục tiêu Cốt lõi & Kỳ vọng |
| :--- | :--- | :--- |
| **Khách hàng cuối (Customer)** | Đăng ký, đăng nhập, xem danh mục, thực hiện thao tác nghiệp vụ của chính mình | Giao diện thân thiện, trực quan, phản hồi tức thì |
| **Nhân viên (Staff / Tech)** | Quản lý danh sách tác vụ, cập nhật trạng thái xử lý theo chi nhánh | Thao tác nhanh, chính xác, cập nhật trạng thái thời gian thực |
| **Quản trị viên (Admin)** | Toàn quyền kiểm soát danh mục, phân quyền và dữ liệu hệ thống | Báo cáo trực quan, kiểm soát bảo mật và toàn vẹn dữ liệu |

---

## 3. Yêu Cầu Chức Năng & Quy Tắc Nghiệp Vụ (FRs & BRs)

### 3.1. Danh mục Yêu cầu Chức năng (Functional Requirements)
- **FR-01**: <Mô tả chức năng chi tiết 1>
- **FR-02**: <Mô tả chức năng chi tiết 2>
- **FR-03**: <Mô tả chức năng chi tiết 3>

### 3.2. Quy tắc Nghiệp vụ Ràng buộc (Business Rules)
- **BR-01 (Capacity / Rate Limit)**: <Ví dụ: Không được vượt quá 5 lượt đặt/khung giờ>
- **BR-02 (Data Validation)**: <Ví dụ: Số điện thoại phải chuẩn định dạng 10 chữ số Việt Nam>
- **BR-03 (State Transition)**: <Ví dụ: Đơn chỉ được chuyển sang COMPLETED từ IN_PROGRESS>

---

## 4. Quản Lý Phạm Vi Dự Án (Scope Management)

### 4.1. Trong Phạm Vi Triển Khai (In-Scope — MVP / P0)
- [x] Triển khai luồng Happy Path cho người dùng chính.
- [x] Xử lý đầy đủ 5 trạng thái giao diện UI (`Default`, `Loading`, `Empty`, `Error`, `Success`).
- [x] Tạo Schema Database, API Endpoints và Kiểm thử tự động liên quan.

### 4.2. Ngoài Phạm Vi Phiên Bản Này (Out-of-Scope — Future Phases)
- [ ] Tích hợp cổng thanh toán bên thứ ba (Dời sang v2.0).
- [ ] Gửi thông báo đẩy SMS / Push notification tự động (Dời sang v2.0).
- [ ] Dashboard phân tích số liệu BI nâng cao.

---

## 5. Kịch Bản Góc & Xử Lý Ngoại Lệ (Edge Cases & Exception Handling)

| Mã EC | Tình huống Góc (Edge Case) | Hành vi Hệ thống Mong đợi |
| :---: | :--- | :--- |
| **EC-01** | Người dùng mất kết nối Internet khi gửi request | Client giữ trạng thái form, hiển thị retry button, không làm mất dữ liệu đã nhập |
| **EC-02** | Xung đột đồng thời (Race Condition đặt chỗ cùng giây) | Backend áp dụng Database lock / Serialized transaction, người đến sau nhận lỗi 409 Conflict |
| **EC-03** | Dữ liệu tìm kiếm không trả về kết quả | Hiển thị màn hình Empty State thân thiện kèm gợi ý từ khóa |

---

## 6. Kịch Bản Kiểm Thử Chấp Nhận Người Dùng (Gherkin BDD Scenarios)

```gherkin
Feature: <Tên Tính Năng>

  Background:
    Given Người dùng đã đăng nhập thành công vào hệ thống

  Scenario: [US-01] Thực hiện thao tác thành công (Happy Path)
    Given Người dùng ở màn hình chính của tính năng
    When Người dùng nhập đầy đủ thông tin hợp lệ
    And Nhấn nút "Xác nhận"
    Then Hệ thống lưu bản ghi mới vào cơ sở dữ liệu
    And Phản hồi mã HTTP 201 Created
    And Giao diện hiển thị thông báo thành công và chuyển hướng về danh sách

  Scenario: [US-02] Vi phạm quy tắc nghiệp vụ giới hạn (BR-01 Violation)
    Given Khung giờ đã đạt tối đa số lượt cho phép
    When Người dùng cố gắng đăng ký vào khung giờ này
    Then Hệ thống từ chối tạo mới bản ghi
    And Phản hồi mã HTTP 400 Bad Request kèm thông báo "Khung giờ đã đầy"
```

---

## 7. Tiêu Chí Nghiệm Thu Nghiệp Vụ & Ký Duyệt Gate 1 (Sign-off Checklist)

- [ ] **BAC-01**: 100% yêu cầu chức năng (FR-01 $\to$ FR-03) có kịch bản BDD tương ứng.
- [ ] **BAC-02**: Không còn điểm mơ hồ nghiệp vụ chưa được giải quyết.
- [ ] **BAC-03**: Khách hàng / Product Owner đã xem xét và đồng ý phạm vi qua `review_gate_1_prd.md`.

---

## 8. Nhật Ký Phỏng Vấn Làm Rõ Nghiệp Vụ (Clarification Log)

| Câu hỏi | Đối tượng hỏi | Phản hồi từ Khách hàng / PO | Quyết định Kỹ thuật / Nghiệp vụ |
| :--- | :--- | :--- | :--- |
| *Ví dụ: Khách hàng vãng lai có cần tạo tài khoản không?* | `@lead-ba` | *Bắt buộc tạo tài khoản với SĐT và mật khẩu.* | Thêm bảng `users`, mã hóa mật khẩu bcrypt và JWT authentication. |
