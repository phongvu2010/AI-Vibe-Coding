---
name: frontend_nextjs_tailwind
description: "Guidelines for Next.js 15 App Router, React 19, Tailwind CSS styling, strict TypeScript interfaces matching backend snake_case, and implementing the 5 UI states."
---

# Next.js 15, React 19 & Tailwind CSS Engineering Skill

Kỹ năng này hướng dẫn `frontend-dev` xây dựng giao diện Web chuẩn mực:

## 1. Đồng Bộ Hợp Đồng (Contract Synchronization)
- Toàn bộ TypeScript interfaces phải sử dụng `snake_case` khớp 100% với Pydantic Schemas của Backend.
- Định nghĩa mock data tương ứng tại `src/frontend/src/lib/api/mocks/` để phục vụ Wave 1.

## 2. Xử Lý 5 Trạng Thái Giao Diện
Mọi component bất đồng bộ bắt buộc xử lý đủ 5 trạng thái:
1. `default`: Hiển thị form hoặc trang tĩnh sẵn sàng.
2. `loading`: Hiển thị Skeleton placeholder có hiệu ứng `animate-pulse`.
3. `empty`: Thông báo danh sách trống thân thiện kèm nút tạo mới.
4. `error`: Alert lỗi trực quan màu đỏ kèm nút "Thử lại" (Retry).
5. `success`: Hiển thị dữ liệu chính xác.
