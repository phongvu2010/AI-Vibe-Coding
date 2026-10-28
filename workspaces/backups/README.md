# 📦 BACKUPS DIRECTORY (RUNTIME ARCHIVE)

Thư mục này lưu trữ các bản sao lưu tự động (snapshots / zip archives) của toàn bộ mã nguồn `output_project` và `artifacts` trước khi thực hiện dọn dẹp dự án hoặc rollback:
```bash
make backup PROJECT="Tên_Dự_Án"      # Sao lưu thủ công snapshot
make clean-project                   # Tự động sao lưu an toàn rồi dọn sạch để đón dự án mới
```
