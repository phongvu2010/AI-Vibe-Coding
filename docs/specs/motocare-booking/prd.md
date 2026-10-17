# PRD: Nền Tảng Đặt Lịch Bảo Dưỡng Xe Máy (MotoCare Booking)

---
feature_slug: "motocare-booking"
version: "1.0.0"
author: "Lead BA Agent (lead-ba)"
status: "APPROVED_BY_USER"
created_at: "2026-10-17T16:00:00Z"
---

## 1. Tổng Quan Nghiệp Vụ & Mục Tiêu SMART
- **Bối cảnh**: Hệ thống MotoCare giúp khách hàng đặt lịch bảo dưỡng xe máy trực tuyến, lựa chọn dịch vụ, chi nhánh và theo dõi tiến độ sửa chữa theo thời gian thực.
- **Mục tiêu SMART**:
  - **S**: Cung cấp tính năng đặt lịch 3 bước (chọn xe -> chọn dịch vụ & chi nhánh -> xác nhận).
  - **M**: Giảm 80% thời gian chờ đợi tại quầy dịch vụ, tỷ lệ hủy lịch < 5%.
  - **A**: Hoàn thành trong MVP Phase 1 với 2 models cốt lõi: `Booking` và `ServiceCatalog`.
  - **R**: Tăng trải nghiệm khách hàng và tối ưu năng suất kỹ thuật viên.
  - **T**: Hoàn thành toàn diện trong chu kỳ phát triển hiện tại.

## 2. Đối Tượng Người Dùng & Phân Quyền (RBAC)
| Persona | Quyền hạn | Mô tả |
| :--- | :--- | :--- |
| **Customer** | Tạo lịch, xem danh sách lịch hẹn của bản thân, hủy lịch khi còn `pending` | Khách hàng chủ xe |
| **Technician** | Xem danh sách lịch hẹn tại chi nhánh, cập nhật trạng thái `in_progress` -> `completed` | Kỹ thuật viên bảo dưỡng |
| **Admin** | Toàn quyền cấu hình dịch vụ, quản lý tất cả đơn đặt lịch | Quản trị viên hệ thống |

## 3. Yêu Cầu Chức Năng (Functional Requirements)
- **FR-01**: Khách hàng có thể xem danh mục dịch vụ bảo dưỡng kèm giá và thời gian dự kiến.
- **FR-02**: Khách hàng có thể tạo đơn đặt lịch bảo dưỡng chọn chi nhánh và khung giờ.
- **FR-03**: Khách hàng và kỹ thuật viên có thể tra cứu chi tiết và cập nhật trạng thái đơn đặt lịch.

## 4. Quy Tắc Nghiệp Vụ (Business Rules)
- **BR-01**: Khung giờ đặt lịch phải cách thời điểm hiện tại ít nhất 2 giờ.
- **BR-02**: Một khách hàng không được đặt quá 2 lịch hẹn cùng một khung giờ.
- **BR-03**: Trạng thái đơn đặt lịch tuân theo luồng nghiêm ngặt: `pending` -> `in_progress` -> `completed` (hoặc `cancelled` khi đang ở `pending`).

## 5. Danh Sách User Stories (Gherkin Format)
```gherkin
Feature: Đặt lịch bảo dưỡng xe máy

  Scenario: Khách hàng đặt lịch hẹn thành công (Happy Path)
    Given Khách hàng đã đăng nhập vào hệ thống
    When Khách hàng chọn dịch vụ "Bảo dưỡng 10 bước", chi nhánh "Chi nhánh Quận 1", và thời gian hợp lệ
    Then Hệ thống ghi nhận đơn với trạng thái "pending" và trả về mã booking_id

  Scenario: Khách hàng chọn khung giờ quá khứ (Validation Error)
    Given Khách hàng đang ở màn hình đặt lịch
    When Khách hàng chọn thời gian trước thời điểm hiện tại
    Then Hệ thống từ chối và báo lỗi "Thời gian đặt lịch phải sau thời điểm hiện tại ít nhất 2 giờ"
```
