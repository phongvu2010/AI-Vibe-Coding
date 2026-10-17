# Mục Tiêu Chất Lượng & Ngân Sách Token (SLA & Token Budgets)
### AI-Vibe-Coding Software House

Hệ thống đặt ra các chỉ số chất lượng dịch vụ (Service Level Agreements - SLA) và hạn mức tiêu thụ token cho từng Sub-Team nhằm tối đa hóa hiệu suất và giảm thiểu chi phí vận hành.

---

## ⏱️ 1. Chỉ Tiêu Thời Gian Xử Lý (Turnaround Time SLA)

| Sub-Team | Nhiệm vụ chính | SLA Mục Tiêu (Lượt phản hồi) | Tiêu chí Hoàn thành |
| :--- | :--- | :---: | :--- |
| **Sub-Team 1: Discovery** | Phỏng vấn & xuất bản PRD | 1-2 lượt chat | 1-3 câu hỏi P0 hoàn tất, `prd.md` & `ui_ux_spec.md` sẵn sàng. |
| **Sub-Team 2: Architecture**| Thiết kế kỹ thuật & Contract | 1 lượt dispatch | `plan.md` có đầy đủ ERD, API specs, Contract Matrix. |
| **Sub-Team 3: Engineering** | Lập trình đợt kép (Wave 1 & 2) | 2 đợt gối đầu | Models, Schemas, Repos, UI components và Live API hoàn tất. |
| **Sub-Team 4: QA & Review** | Kiểm thử & Thẩm định diff | $\le 3$ vòng lặp | 5 tầng test pass 100%, điểm review $\ge 85/100$. |
| **Sub-Team 5: Release** | Đóng gói & Soạn tài liệu | 1 lượt hoàn tất | File `.zip`, manifest checksum, `USER_MANUAL.md` sẵn sàng. |

---

## 💰 2. Ngân Sách Token & Tối Ưu Chi Phí

| Sub-Team | Tỷ lệ Ngân sách Token | Model Tier khuyến nghị | Biện pháp tối ưu hóa |
| :--- | :---: | :--- | :--- |
| **Sub-Team 1** | 15% | `flash` / `pro` (BA) | Phỏng vấn ngắn gọn, tập trung vào P0, không spam câu hỏi vụn vặt. |
| **Sub-Team 2** | 20% | `pro` | Dùng cấu trúc bảng Matrix và sơ đồ Mermaid súc tích. |
| **Sub-Team 3** | 35% | `inherit` (Tech Lead) | Viết code theo phân tầng Clean Architecture, dùng code snippet chính xác. |
| **Sub-Team 4** | 20% | `flash` (QA) / `pro` (Review) | Cắt tỉa traceback còn 15-25 dòng qua `parse_traceback.py`. |
| **Sub-Team 5** | 10% | `flash_lite` | Sử dụng templates markdown có sẵn, sinh manifest tự động bằng script. |
| **TỔNG CỘNG** | **100%** | **Tiết kiệm 70%** | So với việc dùng mô hình Pro đại trà cho toàn bộ chu trình. |
