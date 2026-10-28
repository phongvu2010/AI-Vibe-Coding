# ĐẶC TẢ DỰ ÁN MẪU: CLINICCARE - ĐẶT KHÁM BỆNH TRỰC TUYẾN
# (Healthcare Appointment Booking & Management Platform)

## 1. Mục Tiêu Sản Phẩm (Product Vision)
Số hóa toàn diện quy trình tiếp nhận, tra cứu chuyên khoa và đặt lịch khám cho chuỗi phòng khám y tế ClinicCare. Giúp bệnh nhân chủ động thời gian, giảm thiểu 90% thời gian chờ đợi tại quầy lễ tân và tối ưu công suất phòng khám của đội ngũ bác sĩ.

---

## 2. Đối Tượng Người Dùng & Vai Trò (User Roles)
1. **Bệnh nhân (Patient / Customer)**:
   - Tra cứu chuyên khoa, bác sĩ, khung giờ khám còn trống.
   - Đặt lịch hẹn, nhận mã xác nhận, theo dõi lịch sử khám bệnh.
   - Hủy hoặc dời lịch khám trước giờ hẹn tối thiểu 2 tiếng.
2. **Bác sĩ & Lễ tân (Doctor & Receptionist Staff / Admin)**:
   - Theo dõi danh sách bệnh nhân theo ca khám trong ngày.
   - Đánh dấu trạng thái khám: `CONFIRMED` -> `IN_PROGRESS` -> `COMPLETED` hoặc `NO_SHOW`.
   - Cập nhật ghi chú tóm tắt sau khi kết thúc buổi khám.

---

## 3. Các Tính Năng Cốt Lõi MVP (In-Scope)
- **Xác thực & Người dùng**:
  - Đăng ký và đăng nhập bảo mật bằng số điện thoại / Email kèm mật khẩu mã hóa (JWT Bearer Token).
  - Phân quyền theo vai trò (RBAC): `patient`, `staff`, `admin`.
- **Danh mục Chuyên khoa & Dịch vụ**:
  - Danh mục chuyên khoa (Nội tổng quát, Tim mạch, Tai Mũi Họng, Nhi khoa, Da liễu...).
  - Bảng giá niêm yết minh bạch theo từng dịch vụ khám.
- **Đặt lịch theo Khung giờ (Slot Booking)**:
  - Chọn bác sĩ và khung giờ khám (mỗi ca khám kéo dài 30 phút).
  - **Quy tắc Nghiệp vụ Cốt lõi (BR-01)**: Mỗi khung giờ 30 phút chỉ tiếp nhận tối đa 2 bệnh nhân. Nếu quá tải, hệ thống tự động khóa khung giờ và gợi ý các slot lân cận còn trống.
  - Kiểm tra xung đột lịch: Một bệnh nhân không thể đặt 2 lịch khám trùng nhau về mặt thời gian.
- **Quản lý Đơn Đặt Khám (Appointments Management)**:
  - Tra cứu trạng thái đơn theo thời gian thực (`PENDING`, `CONFIRMED`, `CANCELLED`, `COMPLETED`).
  - Hỗ trợ bệnh nhân tự hủy đơn có lý do hủy.
- **Thanh toán & Xác nhận**:
  - Tạo mã thanh toán chuyển khoản qua mã QR động (VietQR payload).
  - Tự động sinh mã phiếu khám định danh `CC-YYYYMMDD-XXXX`.

---

## 4. Tính Năng Dành Cho Tương Lai (Out-of-Scope v2.0)
- Tích hợp cổng thanh toán quốc tế thẻ Visa/Mastercard (Stripe / OnePay).
- Khám bệnh từ xa trực tuyến qua cuộc gọi video (Telemedicine WebRTC).
- Kết nối bệnh án điện tử quốc gia và đồng bộ bảo hiểm y tế.

---

## 5. Kịch Bản Chấp Thuận Người Dùng Mẫu (Gherkin Scenarios)

### Scenario 1: Đặt lịch thành công khi khung giờ còn chỗ
```gherkin
Given bệnh nhân "Nguyen Van A" đã đăng nhập thành công
And chuyên khoa "Tim mạch" có bác sĩ "Dr. Tran" còn trống khung giờ "09:00 - 09:30" (hiện tại có 1/2 lượt đặt)
When bệnh nhân chọn bác sĩ "Dr. Tran" và xác nhận đặt lịch khám lúc "09:00" ngày mai
Then hệ thống phản hồi mã trạng thái 201 Created
And tạo mới đơn hẹn với trạng thái "CONFIRMED"
And khung giờ "09:00 - 09:30" cập nhật số lượt đặt thành 2/2 (Hết chỗ)
```

### Scenario 2: Từ chối đặt lịch khi khung giờ đã đầy (BR-01)
```gherkin
Given khung giờ "09:00 - 09:30" của bác sĩ "Dr. Tran" đã có 2/2 lượt đặt
When bệnh nhân "Nguyen Van B" cố gắng gửi yêu cầu đặt lịch lúc "09:00"
Then hệ thống phản hồi lỗi 409 Conflict với thông báo "Khung giờ này đã đủ số lượng tiếp nhận"
And danh sách gợi ý trả về khung giờ khả dụng kế tiếp là "09:30 - 10:00"
```
