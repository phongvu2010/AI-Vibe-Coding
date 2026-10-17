# Đề Bài Mẫu Từ Khách Hàng: Nền Tảng Đặt Lịch Bảo Dưỡng Xe Máy (MotoCare)

---

## 📌 1. Bối Cảnh & Vấn Đề Nghiệp Vụ
Khách hàng là chuỗi trung tâm chăm sóc xe máy cao cấp muốn xây dựng nền tảng **MotoCare** giúp khách hàng đặt lịch bảo dưỡng trực tuyến, theo dõi tiến độ sửa chữa theo thời gian thực và quản lý lịch sử xe.

## 🎯 2. Yêu Cầu Tính Năng Cốt Lõi (MVP Scope - Phase 1)
1. **Xác thực & Quản lý Người dùng (Auth & Profile)**:
   - Đăng ký, đăng nhập qua Email / Mật khẩu.
   - Quản lý hồ sơ cá nhân và danh sách xe của khách hàng (Biển số xe, Hãng xe, Dòng xe, Năm sản xuất).
2. **Danh mục Dịch vụ (Service Catalog)**:
   - Danh sách các gói bảo dưỡng định kỳ (Thay nhớt, Bảo dưỡng toàn diện 10 bước, Kiểm tra phanh).
   - Hiển thị giá tiền, thời gian dự kiến và danh sách linh kiện đi kèm.
3. **Đặt Lịch & Theo Dõi Tiến Độ (Booking & Status Tracking)**:
   - Chọn trung tâm bảo dưỡng gần nhất, chọn ngày giờ và dịch vụ.
   - 4 Trạng thái đơn đặt lịch: `pending` (Chờ tiếp nhận) $\rightarrow$ `in_progress` (Đang sửa chữa) $\rightarrow$ `completed` (Hoàn thành) $\rightarrow$ `cancelled` (Hủy).
4. **Nền tảng Mục tiêu**:
   - Web Portal dành cho khách hàng đặt lịch và Admin quản lý.
   - Mobile App (React Native Expo) cho khách hàng trên điện thoại.

## 🛡️ 3. Yêu Cầu Phi Chức Năng (Non-Functional)
- Thời gian phản hồi API < 200ms.
- Phân tầng bảo mật RBAC: Khách hàng chỉ xem được lịch của mình; Nhân viên xem được lịch tại chi nhánh; Admin quản trị toàn bộ.
