# Bảng Kiểm Nghiệm Thu Khách Hàng (UAT Checklist)

---
feature_slug: "<feature-slug>"
lead: "Client Success & Handover Lead (handover-lead)"
client: "Product Owner / Khách hàng"
status: "READY_FOR_ACCEPTANCE"
---

## 1. Hướng Dẫn Khởi Chạy 1-Chạm (1-Click Test Drive)
Khách hàng có thể trải nghiệm sản phẩm ngay trên máy cá nhân với các lệnh sau:
```bash
# Khởi chạy toàn bộ hệ thống bằng Docker
make docker-up

# Hoặc khởi chạy backend cục bộ
make dev
```
- Web Portal: `http://localhost:3000`
- API Swagger Docs: `http://localhost:8000/api/v1/docs`

---

## 2. Kịch Bản Kiểm Tra Nghiệm Thu (User Acceptance Test Cases)

| Mã kiểm tra | Kịch bản nghiệm thu | Các bước thực hiện | Kết quả mong đợi | Trạng thái |
| :--- | :--- | :--- | :--- | :---: |
| **UAT-01** | Đăng nhập tài khoản | 1. Nhập email & pass<br/>2. Click "Đăng nhập" | Chuyển vào Dashboard thành công | `[ ]` |
| **UAT-02** | Xem danh sách dịch vụ | 1. Vào mục Dịch vụ<br/>2. Kiểm tra danh mục | Hiển thị đầy đủ tên, giá và thời gian | `[ ]` |
| **UAT-03** | Đặt lịch bảo dưỡng xe | 1. Chọn ngày giờ<br/>2. Chọn chi nhánh<br/>3. Click "Xác nhận" | Tạo lịch thành công, mã đơn hiển thị | `[ ]` |
| **UAT-04** | Xử lý khi mất mạng | 1. Ngắt kết nối mạng<br/>2. Thao tác gửi đơn | Hiển thị thông báo lỗi màu đỏ kèm nút Thử lại | `[ ]` |

---

## 3. Ký Duyệt Bàn Giao (Client Sign-off)
- **Đại diện Khách hàng**: `[Đã Duyệt / Chưa Duyệt]`
- **Ngày nghiệm thu**: `.../.../2026`
- **Ý kiến phản hồi**: `...`
