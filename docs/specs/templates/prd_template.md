# Product Requirements Document (PRD)

---
feature_slug: "<feature-slug>"
version: "1.0.0"
author: "Lead BA Agent (lead-ba)"
status: "DRAFT | APPROVED_BY_USER"
created_at: "<ISO-8601-Timestamp>"
---

## 1. Tổng Quan Nghiệp Vụ & Mục Tiêu SMART
- **Bối cảnh**: <Mô tả lý do và nhu cầu thực tế của tính năng>
- **Mục tiêu SMART**:
  - S (Specific): <Mục tiêu cụ thể đạt được>
  - M (Measurable): <Chỉ số đo lường thành công>
  - A (Achievable): <Khả năng hoàn thành trong phạm vi>
  - R (Relevant): <Giá trị mang lại cho người dùng/khách hàng>
  - T (Time-bound): <Kỳ vọng bàn giao>

## 2. Đối Tượng Người Dùng & Phân Quyền (Personas & Permissions)
| Persona | Quyền hạn (Permissions) | Mô tả vai trò |
| :--- | :--- | :--- |
| **Customer** | Xem dịch vụ, tạo lịch hẹn, xem lịch hẹn của chính mình | Khách hàng cuối |
| **Staff / Technician** | Xem lịch hẹn theo chi nhánh, cập nhật trạng thái đơn | Kỹ thuật viên bảo dưỡng |
| **Admin** | Quản lý toàn bộ người dùng, dịch vụ và đơn đặt lịch | Quản trị viên hệ thống |

## 3. Yêu Cầu Chức Năng (Functional Requirements - FR)
- **FR-01**: <Mô tả chức năng 1>
- **FR-02**: <Mô tả chức năng 2>
- **FR-03**: <Mô tả chức năng 3>

## 4. Quy Tắc Nghiệp Vụ (Business Rules - BR)
- **BR-01**: <Quy tắc ràng buộc logic 1>
- **BR-02**: <Quy tắc ràng buộc logic 2>

## 5. Kịch Bản Góc & Ngoại Lệ (Edge Cases - EC)
- **EC-01**: <Khi mất kết nối mạng hoặc lỗi server>
- **EC-02**: <Khi dữ liệu đầu vào bị trùng lặp>

## 6. Danh Sách User Stories (Gherkin Format)
```gherkin
Feature: <Tên Tính Năng>

  Scenario: <Happy Path 1>
    Given <Tiền điều kiện>
    When <Thao tác người dùng>
    Then <Kết quả mong đợi>

  Scenario: <Edge Case 1 - Validation Error>
    Given <Tiền điều kiện>
    When <Nhập sai thông tin>
    Then <Thông báo lỗi tương ứng>
```
