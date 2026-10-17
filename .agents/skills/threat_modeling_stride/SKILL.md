---
name: threat_modeling_stride
description: "Framework and instructions for conducting STRIDE threat modeling, establishing RBAC/ABAC authorization matrices, and verifying OWASP Top 10 compliance."
---

# STRIDE Threat Modeling & Security Audit Skill

Kỹ năng này hướng dẫn `security-architect` và `code-reviewer` rà soát an toàn phần mềm:

## 1. Khung Phân Tích 6 Nguy Cơ STRIDE
- **Spoofing**: Xác minh danh tính qua JWT Token, bcrypt password hashing.
- **Tampering**: Khử trùng dữ liệu đầu vào, không nối chuỗi raw SQL.
- **Repudiation**: Ghi nhật ký audit trail cho các hành động nhạy cảm.
- **Information Disclosure**: Không phơi bày stack trace, bắt và đóng gói lỗi thành `{"detail": "..."}`.
- **Denial of Service**: Phân trang cho các API lấy danh sách, kiểm soát kích thước payload.
- **Elevation of Privilege**: Kiểm tra quyền hạn nghiêm ngặt (chỉ cho phép user thao tác trên tài nguyên của chính mình).
