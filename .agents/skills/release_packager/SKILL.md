---
name: release_packager
description: "Instructions for Release Engineer and Handover Lead to bundle software packages, compute SHA256 hashes, generate RELEASE_MANIFEST.json, and prepare UAT checklists."
---

# Automated Release Packaging & Handover Skill

Kỹ năng này hướng dẫn `release-engineer` và `handover-lead` thực hiện khâu đóng gói và bàn giao phần mềm:

## 1. Quy Trình Đóng Gói Bản Phát Hành
1. Chạy lệnh:
   ```bash
   python scripts/bundle_release.py <feature-slug> <version>
   ```
2. Kiểm tra các tệp đầu ra trong `dist/releases/`:
   - Gói nén: `<feature-slug>_v<version>_<timestamp>.zip`
   - Bảng kê tệp: `RELEASE_MANIFEST.json` chứa danh sách tệp, kích thước, và mã băm SHA256.

## 2. Chuẩn Bị Hồ Sơ Bàn Giao Khách Hàng
Bao gồm 3 tài liệu thiết yếu:
1. `USER_MANUAL.md`: Hướng dẫn cho người dùng cuối trải nghiệm tính năng mới.
2. `UAT_CHECKLIST.md`: Bảng kiểm nghiệm thu chi tiết từng bước cho khách hàng ký duyệt.
3. `DEPLOYMENT.md`: Hướng dẫn vận hành hệ thống bằng Docker.
