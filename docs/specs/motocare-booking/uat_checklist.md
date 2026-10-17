# Bảng Kiểm Nghiệm Thu Khách Hàng: MotoCare Booking (UAT Checklist)

---
feature_slug: "motocare-booking"
lead: "Client Success & Handover Lead (handover-lead)"
client: "Product Owner / Khách hàng MotoCare"
status: "READY_FOR_ACCEPTANCE"
---

## 1. Hướng Dẫn Trải Nghiệm 1-Chạm (1-Click Test Drive)
```bash
# Khởi chạy toàn bộ hệ thống bằng Docker
make docker-up

# Hoặc khởi chạy backend cục bộ
make dev
```
- Web Portal: `http://localhost:3000`
- API Swagger Docs: `http://localhost:8000/api/v1/docs`

---

## 2. Kịch Bản Nghiệm Thu Thực Tế (UAT Test Cases)

| Mã kiểm tra | Kịch bản nghiệm thu | Các bước thao tác | Kết quả mong đợi | Trạng thái |
| :--- | :--- | :--- | :--- | :---: |
| **UAT-MC-01** | Xem danh mục bảo dưỡng | 1. Mở màn hình Dịch vụ<br/>2. Rà soát danh sách | Hiển thị đầy đủ tên gói, giá tiền, thời gian dự kiến | `[x] Pass` |
| **UAT-MC-02** | Đặt lịch bảo dưỡng thành công | 1. Chọn chi nhánh & dịch vụ<br/>2. Chọn ngày giờ hợp lệ<br/>3. Click "Xác nhận" | Tạo lịch thành công, trạng thái hiển thị `pending` | `[x] Pass` |
| **UAT-MC-03** | Chặn đặt lịch thời gian quá khứ | 1. Cố ý chọn ngày trong quá khứ<br/>2. Gửi form | Hệ thống chặn và báo lỗi màu đỏ rõ ràng | `[x] Pass` |
| **UAT-MC-04** | Cập nhật tiến độ bảo dưỡng | 1. Kỹ thuật viên chuyển trạng thái sang `in_progress`<br/>2. Khách hàng xem lại | Trạng thái cập nhật theo thời gian thực | `[x] Pass` |

---

## 3. Ký Duyệt Bàn Giao
- **Đại diện Khách hàng**: `Đã Duyệt (APPROVED)`
- **Ngày nghiệm thu**: `17/10/2026`
- **Đánh giá tổng kết**: "Hệ thống đáp ứng hoàn hảo các yêu cầu nghiệp vụ đặt ra trong đề bài ban đầu."
