---
name: requirement_parser
description: "Phân tích và bóc tách yêu cầu thô của khách hàng (email, chat, biên bản họp), trích xuất tác nhân (actors), thực thể dữ liệu, phát hiện vùng mờ (Ambiguity Detection) và sinh bảng câu hỏi làm rõ (Clarification Q&A)."
---

# Requirement Parser Skill

## Mục đích
Hỗ trợ `account-lead` và `lead-ba` bóc tách các văn bản phi cấu trúc từ khách hàng (email, đoạn chat, biên bản họp, voice memo transcript) thành danh sách yêu cầu có cấu trúc trước khi lập PRD.

## Quy trình 4 bước thực hiện:

### 1. Trích xuất Mục tiêu Dự án (Project Objective & Business Goals)
- Xác định bài toán kinh doanh cốt lõi mà khách hàng muốn giải quyết.
- Bóc tách KPI kỳ vọng (ví dụ: thời gian đặt phòng giảm 50%, quản lý 10,000 người dùng).

### 2. Liệt kê Tác nhân & Quyền hạn (Actors & Personas)
- Xác định các nhóm người dùng tương tác với hệ thống:
  - *End User / Customer*: Khách hàng cuối sử dụng ứng dụng.
  - *Internal Staff / Operator*: Nhân viên vận hành, kỹ thuật viên.
  - *Administrator*: Quản trị viên hệ thống có toàn quyền.
- Xác định sơ bộ ma trận phân quyền (Ai được xem/sửa tài nguyên nào).

### 3. Phát hiện Vùng mờ & Mâu thuẫn Nghiệp vụ (Ambiguity & Conflict Detection)
Chủ động rà soát các điểm thiếu sót thường gặp trong văn bản thô:
- **Thiếu luồng ngoại lệ & xử lý lỗi**: Khi thanh toán thất bại, hết chỗ, mất mạng thì hiển thị thế nào?
- **Thiếu ràng buộc dữ liệu**: Định dạng số điện thoại, độ dài mật khẩu, quy tắc trùng lặp email.
- **Thiếu tiêu chí phi chức năng (NFR)**: Thời gian phản hồi API mong đợi, dung lượng file upload tối đa.
- **Mâu thuẫn logic**: Đề bài yêu cầu vừa thanh toán trước vừa cho phép hủy không phạt sát giờ.

### 4. Xuất bản Bảng Câu Hỏi Làm Rõ (Clarification Q&A Matrix)
Thiết lập bảng câu hỏi P0 gửi người dùng qua công cụ `ask_question`:

| ID | Vấn đề / Yêu cầu gốc | Điểm mơ hồ phát hiện | Phương án đề xuất `(Recommended)` | Các phương án thay thế |
| :--- | :--- | :--- | :--- | :--- |
| **Q-01** | "Cần thanh toán trực tuyến" | Chưa rõ cổng thanh toán & phương thức thanh toán | Tích hợp Stripe / MoMo với webhook xác thực tức thì | Cổng nội địa VNPay, COD (tiền mặt) |
| **Q-02** | "Khách có thể đổi lịch hẹn" | Giới hạn thời gian đổi lịch trước bao lâu? | Cho phép đổi lịch trước tối thiểu 2 giờ | Đổi lịch tự do, không cho đổi lịch |
