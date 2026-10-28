#!/usr/bin/env python3
"""Domain & Business Rule Analyzer for AI-Vibe-Coding (`scripts/domain_analyzer.py`).

Analyzes raw user requirements / client briefs to automatically detect:
- Business Domain & Entity Mapping
- Capacity & Rate Rules (e.g. BR-01 slot limits)
- Clean Architecture Suggested Models & Data Contracts

Usage:
    python scripts/domain_analyzer.py examples/sample_client_brief.md
    python scripts/domain_analyzer.py "Cần làm app phòng khám giới hạn tối đa 3 bệnh nhân mỗi 30 phút"
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict


class DomainAnalyzer:
    """Phân tích và trích xuất thực thể, domain và quy tắc nghiệp vụ từ bất kỳ yêu cầu nào."""

    DOMAINS = [
        {
            "id": "medical_clinic",
            "keywords": ["khám", "bệnh", "clinic", "bác sĩ", "y tế", "thuốc", "phòng khám", "nha khoa", "nha sĩ", "răng hàm mặt"],
            "primary_entity": "MedicalService",
            "order_entity": "ClinicAppointment",
            "primary_label": "Dịch vụ Khám & Gói Chăm sóc Y tế",
            "unit_name": "bệnh nhân",
            "default_price": 300000.0,
            "default_capacity": 2,
        },
        {
            "id": "flower_ecommerce",
            "keywords": ["hoa tươi", "bó hoa", "lẵng hoa", "tiệm hoa", "shop hoa", "flower", "hoa cưới"],
            "primary_entity": "FlowerItem",
            "order_entity": "FlowerOrder",
            "primary_label": "Bó hoa tươi & Lẵng hoa",
            "unit_name": "bó hoa",
            "default_price": 250000.0,
            "default_capacity": 5,
        },
        {
            "id": "vehicle_care",
            "keywords": ["xe", "gara", "bảo dưỡng", "sửa xe", "phụ tùng", "motocare", "ô tô", "xe máy"],
            "primary_entity": "SparePart",
            "order_entity": "Appointment",
            "primary_label": "Phụ tùng & Dịch vụ Sửa chữa Xe",
            "unit_name": "xe",
            "default_price": 150000.0,
            "default_capacity": 3,
        },
        {
            "id": "real_estate",
            "keywords": ["bất động sản", "nhà đất", "căn hộ", "thuê nhà", "mặt bằng", "chung cư"],
            "primary_entity": "PropertyItem",
            "order_entity": "ViewingAppointment",
            "primary_label": "Bất động sản & Căn hộ cho thuê",
            "unit_name": "lịch xem",
            "default_price": 500000.0,
            "default_capacity": 4,
        },
        {
            "id": "education",
            "keywords": ["học", "khóa học", "lớp", "giáo dục", "course", "gia sư", "đào tạo"],
            "primary_entity": "CourseItem",
            "order_entity": "Enrollment",
            "primary_label": "Khóa học & Lớp Đào tạo Trực tuyến",
            "unit_name": "học viên",
            "default_price": 450000.0,
            "default_capacity": 15,
        },
        {
            "id": "restaurant",
            "keywords": ["nhà hàng", "quán ăn", "đặt bàn", "món ăn", "ẩm thực", "menu", "restaurant", "bàn ăn", "thực đơn", "món"],
            "primary_entity": "MenuItem",
            "order_entity": "TableBooking",
            "primary_label": "Món ăn & Đặt bàn Nhà hàng",
            "unit_name": "bàn",
            "default_price": 350000.0,
            "default_capacity": 5,
        },
    ]

    @classmethod
    def analyze(cls, raw_text: str, project_name: str = "") -> Dict[str, Any]:
        text_lower = raw_text.lower()

        # 1. Trích xuất quy tắc giới hạn (capacity / rate rule)
        slot_match = re.search(
            r"(?:tối đa|không quá|giới hạn)\s*(\d+)\s*(?:xe|bệnh nhân|đơn|khách|yêu cầu|slot|lượt|học viên|bàn|món)",
            text_lower,
        )
        time_match = re.search(r"(?:trong|mỗi|khung giờ)\s*(\d+)\s*(?:phút|giờ|h)", text_lower)
        time_unit = time_match.group(0) if time_match else "mỗi khung giờ"

        # 2. Nhận diện Domain
        selected_domain = None
        for d in cls.DOMAINS:
            if any(k in text_lower for k in d["keywords"]):
                selected_domain = d
                break

        if not selected_domain:
            selected_domain = {
                "id": "general_saas",
                "primary_entity": "ResourceItem",
                "order_entity": "BookingRequest",
                "primary_label": "Dịch vụ & Tài nguyên Hệ thống",
                "unit_name": "yêu cầu",
                "default_price": 100000.0,
                "default_capacity": 5,
            }

        max_slot = int(slot_match.group(1)) if slot_match else selected_domain["default_capacity"]
        rule_desc = f"Giới hạn tối đa {max_slot} {selected_domain['unit_name']} {time_unit} (Quy tắc nghiệp vụ BR-01)"

        return {
            "domain_id": selected_domain["id"],
            "primary_label": selected_domain["primary_label"],
            "primary_entity": selected_domain["primary_entity"],
            "order_entity": selected_domain["order_entity"],
            "unit_name": selected_domain["unit_name"],
            "default_price": selected_domain["default_price"],
            "capacity_limit": max_slot,
            "time_window": time_unit,
            "business_rule_01": rule_desc,
            "suggested_tables": [
                "users (id, email, full_name, hashed_password, role, is_active)",
                f"{selected_domain['primary_entity'].lower()}s (id, name, description, price, is_available)",
                f"{selected_domain['order_entity'].lower()}s (id, user_id, status, scheduled_at, notes, total_amount)",
            ],
        }

    @classmethod
    def generate_gherkin(cls, result: Dict[str, Any]) -> str:
        """Sinh bộ kịch bản Gherkin BDD tự động bám sát quy tắc nghiệp vụ BR-01."""
        entity = result["order_entity"]
        unit = result["unit_name"]
        cap = result["capacity_limit"]
        window = result["time_window"]

        return f"""Feature: Quản lý đặt lịch & Kiểm soát tải ({entity} Management)
  Là một người dùng hệ thống
  Tôi muốn thực hiện đặt lịch dịch vụ
  Để đảm bảo đơn hàng được xác nhận đúng quy chuẩn vận hành

  Scenario: Đặt lịch thành công khi còn chỗ trống (Happy Path)
    Given khung giờ dự kiến còn khả dụng ({cap - 1}/{cap} {unit})
    When tôi gửi yêu cầu tạo đơn {entity} hợp lệ
    Then hệ thống phản hồi mã HTTP 201 Created
    And trạng thái đơn ghi nhận là "PENDING"
    And số lượng tiếp nhận trong {window} tăng thêm 1

  Scenario: Từ chối đặt lịch khi khung giờ đã đạt giới hạn tối đa (Edge Case - BR-01)
    Given khung giờ dự kiến đã đạt giới hạn tối đa ({cap}/{cap} {unit})
    When tôi gửi yêu cầu tạo đơn {entity} vào khung giờ đó
    Then hệ thống từ chối với mã HTTP 400 Bad Request
    And thông điệp lỗi trả về chứa "Khung giờ đã đầy, vui lòng chọn thời gian khác"
    And không có bản ghi mới nào được lưu vào cơ sở dữ liệu

  Scenario: Từ chối khi thông tin yêu cầu không hợp lệ (Edge Case - Validation)
    When tôi gửi payload thiếu trường bắt buộc hoặc thời gian trong quá khứ
    Then hệ thống trả về mã HTTP 422 Unprocessable Entity
    And thông báo chi tiết lỗi validation cụ thể"""

    @classmethod
    def generate_contract_matrix(cls, result: Dict[str, Any]) -> str:
        """Sinh Ma Trận Ánh Xạ Dữ Liệu 3 Tầng (Cross-Layer Contract Matrix) cho plan.md."""
        order_table = result["order_entity"].lower() + "s"
        return rf"""### 2. Ma Trận Ánh Xạ Dữ Liệu 3 Tầng ({order_table})

| Trường Dữ Liệu | Kiểu DB (SQLAlchemy/PG) | Kiểu Backend (Pydantic v2) | Kiểu Frontend (TypeScript) | Nullable | Mặc định | Ràng buộc / Ghi chú |
| :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| `id` | `Uuid(as_uuid=True)` | `UUID` / `str` | `string` | Không | `uuid.uuid4` | Khóa chính RFC 4122 |
| `user_id` | `Uuid(as_uuid=True)` | `UUID` / `str` | `string` | Không | - | Foreign Key trỏ `users.id` |
| `status` | `String(32)` | `StrEnum` | `'PENDING' \| 'CONFIRMED' \| 'CANCELLED'` | Không | `'PENDING'` | Trạng thái vòng đời |
| `scheduled_at` | `DateTime(timezone=True)` | `datetime` | `string` | Không | - | Định dạng ISO 8601 UTC (Z) |
| `notes` | `Text` | `str \| None` | `string \| null` | Có | `None` | Tối đa 500 ký tự |
| `total_amount` | `Numeric(12, 2)` | `Decimal` / `float` | `number` | Không | `0.0` | Số tiền VNĐ |
| `created_at` | `DateTime(timezone=True)` | `datetime` | `string` | Không | UTC now | Timestamp khởi tạo |
| `updated_at` | `DateTime(timezone=True)` | `datetime` | `string` | Không | UTC now | Timestamp cập nhật |"""


def main():
    if len(sys.argv) < 2:
        print("Cách dùng: python scripts/domain_analyzer.py <file_path_hoặc_chuỗi_yêu_cầu> [--gherkin] [--matrix]")
        sys.exit(1)

    show_gherkin = "--gherkin" in sys.argv
    show_matrix = "--matrix" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if not args:
        print("Vui lòng cung cấp nội dung brief hoặc đường dẫn file.")
        sys.exit(1)

    target = args[0]
    target_path = Path(target)
    if target_path.exists() and target_path.is_file():
        content = target_path.read_text(encoding="utf-8")
        source = f"File: {target_path.name}"
    else:
        content = " ".join(args)
        source = "Raw Input"

    result = DomainAnalyzer.analyze(content)

    print("\n" + "=" * 70)
    print(f"🎯 KẾT QUẢ PHÂN TÍCH NGHIỆP VỤ & THỰC THỂ ({source})")
    print("=" * 70)
    print(f"• Domain xác định : {result['domain_id'].upper()} ({result['primary_label']})")
    print(f"• Thực thể chính  : {result['primary_entity']} (Đơn vị tính: {result['unit_name']})")
    print(f"• Thực thể đơn hẹn: {result['order_entity']}")
    print(f"• Giá tham chiếu  : {result['default_price']:,.0f} VNĐ")
    print(f"• Quy tắc BR-01   : {result['business_rule_01']}")
    print("• Gợi ý bảng DB   :")
    for t in result["suggested_tables"]:
        print(f"  - {t}")
    print("=" * 70)

    if show_gherkin:
        print("\n" + "-" * 70)
        print("🥒 KỊCH BẢN GHERKIN BDD SINH TỰ ĐỘNG CHO PRD:")
        print("-" * 70)
        print(DomainAnalyzer.generate_gherkin(result))

    if show_matrix:
        print("\n" + "-" * 70)
        print("📐 MA TRẬN ÁNH XẠ DỮ LIỆU 3 TẦNG CHO PLAN.MD:")
        print("-" * 70)
        print(DomainAnalyzer.generate_contract_matrix(result))
    print()


if __name__ == "__main__":
    main()
