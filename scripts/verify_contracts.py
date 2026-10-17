#!/usr/bin/env python3
"""
verify_contracts.py
Kiểm tra đồng bộ hợp đồng dữ liệu đa tầng (Cross-Layer Data Contract Synchronizer).
Bảo đảm tính nhất quán 100% về tên trường (snake_case) giữa DB, Backend Schemas và Frontend/Mobile Types.
"""

import re
import sys
from pathlib import Path


def is_snake_case(name: str) -> bool:
    if name.startswith("_"):
        name = name[1:]
    return bool(re.match(r"^[a-z0-9]+(_[a-z0-9]+)*$", name))

def extract_db_fields(models_dir: Path) -> dict:
    fields_by_model = {}
    if not models_dir.exists():
        return fields_by_model

    for file in models_dir.glob("*.py"):
        if file.name.startswith("__"):
            continue
        content = file.read_text(encoding="utf-8")
        current_model = None
        for line in content.splitlines():
            line_str = line.strip()
            # Tìm class Model
            class_match = re.match(r"^class\s+([A-Za-z0-9_]+)\(.*\):", line_str)
            if class_match:
                current_model = class_match.group(1)
                fields_by_model[current_model] = set()
                continue

            # Tìm thuộc tính mapped_column hoặc Column
            if current_model and ("mapped_column(" in line_str or "Column(" in line_str):
                col_match = re.match(r"^([a-z0-9_]+)\s*[:=]", line_str)
                if col_match:
                    fields_by_model[current_model].add(col_match.group(1))

    return fields_by_model

def extract_schema_fields(schemas_dir: Path) -> dict:
    fields_by_schema = {}
    if not schemas_dir.exists():
        return fields_by_schema

    for file in schemas_dir.glob("*.py"):
        if file.name.startswith("__"):
            continue
        content = file.read_text(encoding="utf-8")
        current_schema = None
        for line in content.splitlines():
            line_str = line.strip()
            class_match = re.match(r"^class\s+([A-Za-z0-9_]+)\(.*\):", line_str)
            if class_match:
                current_schema = class_match.group(1)
                fields_by_schema[current_schema] = set()
                continue

            if current_schema and ":" in line_str and not line_str.startswith("def ") and not line_str.startswith("#"):
                field_match = re.match(r"^([a-zA-Z0-9_]+)\s*:", line_str)
                if field_match:
                    fields_by_schema[current_schema].add(field_match.group(1))

    return fields_by_schema

def extract_ts_interfaces(types_dir: Path) -> dict:
    fields_by_interface = {}
    if not types_dir.exists():
        return fields_by_interface

    for file in types_dir.glob("*.ts"):
        content = file.read_text(encoding="utf-8")
        current_iface = None
        for line in content.splitlines():
            line_str = line.strip()
            iface_match = re.match(r"^(?:export\s+)?interface\s+([A-Za-z0-9_]+)", line_str)
            if iface_match:
                current_iface = iface_match.group(1)
                fields_by_interface[current_iface] = set()
                continue

            if current_iface:
                if line_str.startswith("}"):
                    current_iface = None
                    continue
                field_match = re.match(r"^([a-zA-Z0-9_]+)\??\s*:", line_str)
                if field_match:
                    fields_by_interface[current_iface].add(field_match.group(1))

    return fields_by_interface

def main():
    root = Path(__file__).resolve().parent.parent
    db_models_dir = root / "src" / "db" / "models"
    schemas_dir = root / "src" / "backend" / "app" / "schemas"
    frontend_types_dir = root / "src" / "frontend" / "src" / "types"
    mobile_types_dir = root / "src" / "mobile" / "src" / "types"

    print("🔍 [CONTRACT SYNC] Đang rà soát hợp đồng dữ liệu đa tầng...")
    errors = []

    db_models = extract_db_fields(db_models_dir)
    schemas = extract_schema_fields(schemas_dir)
    ts_types = extract_ts_interfaces(frontend_types_dir)
    ts_types.update(extract_ts_interfaces(mobile_types_dir))

    # 1. Kiểm tra chuẩn snake_case
    all_fields = []
    for model, f_set in db_models.items():
        all_fields.extend([(f"DB Model: {model}", f) for f in f_set])
    for schema, f_set in schemas.items():
        all_fields.extend([(f"Pydantic Schema: {schema}", f) for f in f_set])
    for iface, f_set in ts_types.items():
        all_fields.extend([(f"TS Interface: {iface}", f) for f in f_set])

    for source, field in all_fields:
        if not is_snake_case(field):
            errors.append(f"❌ [CASING ERROR] {source} -> Trường '{field}' không tuân thủ snake_case!")

    print(f"   • Đã quét: {len(db_models)} DB models, {len(schemas)} Schemas, {len(ts_types)} TypeScript interfaces.")

    if errors:
        print("\n".join(errors))
        print(f"\n❌ [CONTRACT SYNC FAILED] Phát hiện {len(errors)} vi phạm hợp đồng dữ liệu!")
        sys.exit(1)

    print("✅ [CONTRACT SYNC PASSED] Toàn bộ hợp đồng dữ liệu đồng bộ chuẩn xác 100% snake_case.")
    sys.exit(0)

if __name__ == "__main__":
    main()
