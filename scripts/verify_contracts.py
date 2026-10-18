#!/usr/bin/env python3
"""
verify_contracts.py — Kiểm tra & Đối Chiếu Đồng Bộ Hợp Đồng Dữ Liệu Đa Tầng
(Cross-Layer Data Contract Synchronizer & Cross-Checker).
Thuộc hệ thống AI-Vibe-Coding (Antigravity 2.0).

Chức năng nâng cao:
1. Kiểm tra 100% tuân thủ quy tắc snake_case trên cả 3 tầng (Database, Backend, Frontend/Mobile).
2. Tự động bóc tách AST của SQLAlchemy Models (bao gồm các Mixins kế thừa: UUIDPrimaryKeyMixin, TimestampMixin).
3. Tự động bóc tách AST của Pydantic v2 Schemas và giải quyết toàn bộ cây kế thừa (BaseModel inheritance).
4. Phân tích TypeScript Interfaces trên cả Web (src/frontend/) và Mobile (src/mobile/).
5. [NÂNG CẤP MỚI - CROSS-CHECK]:
   - Đối chiếu chéo các trường giữa DB Model ↔ Backend Response Schema ↔ Frontend TS Interface ↔ Mobile TS Interface.
   - Phát hiện rò rỉ dữ liệu nhạy cảm (Security Leakage Guard: password, hashed_password, secret_key trong Response Schema).
   - Phát hiện lệch chuẩn hợp đồng (Contract Drift): Thiếu trường, thừa trường hoặc không khớp giữa Web và Mobile.
   - Đối chiếu chéo Payload tạo mới (UserCreate Schema ↔ UserCreatePayload TS Interface).
"""

import ast
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# Đảm bảo console UTF-8 trên mọi hệ điều hành
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SENSITIVE_DB_FIELDS = {
    "password",
    "hashed_password",
    "password_hash",
    "salt",
    "secret_key",
    "access_token_secret",
}


def is_snake_case(name: str) -> bool:
    """Kiểm tra tên trường có tuân thủ 100% chuẩn snake_case không."""
    if name.startswith("_"):
        name = name[1:]
    return bool(re.match(r"^[a-z0-9]+(_[a-z0-9]+)*$", name))


def extract_db_mixins(base_file: Path) -> Dict[str, Set[str]]:
    """Tự động phát hiện các Mixin và các trường do Mixin cung cấp trong base.py."""
    mixins = {
        "UUIDPrimaryKeyMixin": {"id"},
        "TimestampMixin": {"created_at", "updated_at"},
    }
    if not base_file.exists():
        return mixins

    try:
        content = base_file.read_text(encoding="utf-8")
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name.endswith("Mixin"):
                fields = set()
                for item in node.body:
                    if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                        if not item.target.id.startswith("_"):
                            fields.add(item.target.id)
                    elif isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name) and not target.id.startswith("_"):
                                fields.add(target.id)
                if fields:
                    mixins[node.name] = fields
    except Exception:
        pass
    return mixins


def extract_db_models(models_dir: Path, base_file: Path) -> Dict[str, Set[str]]:
    """Bóc tách các SQLAlchemy Models và tập hợp toàn bộ trường (bao gồm cả Mixins)."""
    models = {}
    if not models_dir.exists():
        return models

    mixins = extract_db_mixins(base_file)

    for file in sorted(models_dir.glob("*.py")):
        if file.name.startswith("__"):
            continue
        try:
            content = file.read_text(encoding="utf-8")
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Chỉ lấy các class kế thừa Base
                    base_names = [b.id for b in node.bases if isinstance(b, ast.Name)]
                    if "Base" in base_names or any("Mixin" in b for b in base_names):
                        fields = set()
                        # Nạp các trường từ Mixins
                        for b in base_names:
                            if b in mixins:
                                fields.update(mixins[b])

                        # Nạp các trường trực tiếp trong model (bỏ qua __tablename__, __table_args__, v.v.)
                        for item in node.body:
                            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                                if not item.target.id.startswith("_"):
                                    fields.add(item.target.id)
                            elif isinstance(item, ast.Assign):
                                for target in item.targets:
                                    if isinstance(target, ast.Name) and not target.id.startswith("_"):
                                        # Chỉ tính nếu gán mapped_column hoặc Column
                                        is_column = False
                                        if isinstance(item.value, ast.Call):
                                            func_name = getattr(item.value.func, "id", "") or getattr(item.value.func, "attr", "")
                                            if func_name in ["mapped_column", "Column"]:
                                                is_column = True
                                        if is_column:
                                            fields.add(target.id)

                        models[node.name] = fields
        except Exception as e:
            print(f"⚠️ Không thể parse DB model file {file.name}: {e}")

    return models


def extract_pydantic_schemas(schemas_dir: Path) -> Dict[str, Set[str]]:
    """Bóc tách Pydantic schemas và giải quyết kế thừa đa tầng (Inheritance Resolution)."""
    raw_classes: Dict[str, Tuple[List[str], Set[str]]] = {}
    if not schemas_dir.exists():
        return {}

    for file in sorted(schemas_dir.glob("*.py")):
        if file.name.startswith("__"):
            continue
        try:
            content = file.read_text(encoding="utf-8")
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    base_names = [b.id for b in node.bases if isinstance(b, ast.Name)]
                    fields = set()
                    for item in node.body:
                        # Bỏ qua hàm hoặc cấu hình class Config / model_config
                        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                            if item.target.id not in ["model_config", "Config"]:
                                fields.add(item.target.id)
                        elif isinstance(item, ast.Assign):
                            for target in item.targets:
                                if isinstance(target, ast.Name):
                                    if target.id not in ["model_config", "Config"]:
                                        fields.add(target.id)
                    raw_classes[node.name] = (base_names, fields)
        except Exception as e:
            print(f"⚠️ Không thể parse Schema file {file.name}: {e}")

    # Giải quyết đệ quy kế thừa thuộc tính
    resolved_schemas: Dict[str, Set[str]] = {}

    def resolve_fields(cls_name: str, visited: Optional[Set[str]] = None) -> Set[str]:
        if visited is None:
            visited = set()
        if cls_name in visited or cls_name not in raw_classes:
            return set()
        visited.add(cls_name)

        bases, direct_fields = raw_classes[cls_name]
        total = set(direct_fields)
        for b in bases:
            total.update(resolve_fields(b, visited.copy()))
        return total

    for name in raw_classes:
        resolved_schemas[name] = resolve_fields(name)

    return resolved_schemas


def extract_ts_interfaces(types_dir: Path) -> Dict[str, Set[str]]:
    """Bóc tách TypeScript Interfaces từ thư mục types/."""
    interfaces: Dict[str, Set[str]] = {}
    if not types_dir.exists():
        return interfaces

    for file in sorted(types_dir.glob("*.ts")):
        try:
            content = file.read_text(encoding="utf-8")
            current_iface = None
            for line in content.splitlines():
                line_str = line.strip()

                # Bắt đầu interface: export interface Name (extends Parent)?
                match_iface = re.match(r"^(?:export\s+)?interface\s+([A-Za-z0-9_]+)", line_str)
                if match_iface:
                    current_iface = match_iface.group(1)
                    if current_iface not in interfaces:
                        interfaces[current_iface] = set()
                    continue

                if current_iface:
                    if line_str.startswith("}"):
                        current_iface = None
                        continue

                    # Bắt thuộc tính: field_name?: type; hoặc field_name: type;
                    match_field = re.match(r"^([a-zA-Z0-9_]+)\??\s*:", line_str)
                    if match_field:
                        field_name = match_field.group(1)
                        interfaces[current_iface].add(field_name)
        except Exception as e:
            print(f"⚠️ Không thể đọc TS types file {file.name}: {e}")

    return interfaces


def main():
    root = Path(__file__).resolve().parent.parent
    db_models_dir = root / "src" / "db" / "models"
    base_file = root / "src" / "db" / "base.py"
    schemas_dir = root / "src" / "backend" / "app" / "schemas"
    frontend_types_dir = root / "src" / "frontend" / "src" / "types"
    mobile_types_dir = root / "src" / "mobile" / "src" / "types"

    feature_slug = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else "toàn dự án"

    print("=" * 72)
    print(f"🔍 [CONTRACT SYNC] Đang rà soát hợp đồng dữ liệu đa tầng ({feature_slug})...")
    print("=" * 72)

    db_models = extract_db_models(db_models_dir, base_file)
    schemas = extract_pydantic_schemas(schemas_dir)
    frontend_types = extract_ts_interfaces(frontend_types_dir)
    mobile_types = extract_ts_interfaces(mobile_types_dir)

    print(f"   • Đã quét: {len(db_models)} DB Models | {len(schemas)} Schemas | "
          f"{len(frontend_types)} Web Interfaces | {len(mobile_types)} Mobile Interfaces")

    errors: List[str] = []
    warnings: List[str] = []

    # =========================================================================
    # BƯỚC 1: KIỂM TRA CHUẨN CASING (100% snake_case)
    # =========================================================================
    print("\n▶ 1. KIỂM TRA CHUẨN CASING (100% snake_case):")
    casing_violations = []

    for model, f_set in db_models.items():
        for f in f_set:
            if not is_snake_case(f):
                casing_violations.append(f"❌ [DB Model: {model}] Thuộc tính '{f}' không tuân thủ snake_case!")

    for schema, f_set in schemas.items():
        for f in f_set:
            if not is_snake_case(f):
                casing_violations.append(f"❌ [Pydantic Schema: {schema}] Thuộc tính '{f}' không tuân thủ snake_case!")

    for iface, f_set in frontend_types.items():
        for f in f_set:
            if not is_snake_case(f):
                casing_violations.append(f"❌ [Frontend TS: {iface}] Thuộc tính '{f}' không tuân thủ snake_case!")

    for iface, f_set in mobile_types.items():
        for f in f_set:
            if not is_snake_case(f):
                casing_violations.append(f"❌ [Mobile TS: {iface}] Thuộc tính '{f}' không tuân thủ snake_case!")

    if casing_violations:
        for err in casing_violations:
            print(f"   {err}")
        errors.extend(casing_violations)
    else:
        print("   ✅ Toàn bộ thuộc tính trên 3 tầng tuân thủ chuẩn snake_case 100%.")

    # =========================================================================
    # BƯỚC 2: ĐỐI CHIẾU CHÉO NỘI DUNG HỢP ĐỒNG (CROSS-LAYER FIELD MATCHING)
    # =========================================================================
    print("\n▶ 2. ĐỐI CHIẾU CHÉO NỘI DUNG HỢP ĐỒNG (CROSS-LAYER FIELD MATCHING):")

    for entity_name, db_fields in sorted(db_models.items()):
        print(f"\n   ┌── [Thực thể: {entity_name}]")
        print(f"   │ • DB Model ({entity_name:<12}): {len(db_fields)} trường -> {sorted(list(db_fields))}")

        # Tìm Schema phản hồi tương ứng
        resp_schema_candidates = [
            f"{entity_name}Response",
            f"{entity_name}Read",
            f"{entity_name}Out",
            f"{entity_name}Schema",
            entity_name
        ]
        resp_schema_name = next((s for s in resp_schema_candidates if s in schemas), None)

        if resp_schema_name:
            resp_fields = schemas[resp_schema_name]
            print(f"   │ • Schema   ({resp_schema_name:<12}): {len(resp_fields)} trường -> {sorted(list(resp_fields))}")

            # Kiểm tra bảo mật: Không rò rỉ sensitive DB fields vào Response schema
            for sens in SENSITIVE_DB_FIELDS:
                if sens in resp_fields:
                    msg = f"❌ [SECURITY LEAK] Schema '{resp_schema_name}' làm rò rỉ trường nhạy cảm '{sens}'!"
                    errors.append(msg)
                    print(f"   │   {msg}")

            # Đối chiếu DB -> Response Schema (các trường public của DB phải có trong Schema)
            public_db_fields = db_fields - SENSITIVE_DB_FIELDS
            missing_in_schema = public_db_fields - resp_fields
            if missing_in_schema:
                msg = f"⚠️ [OMITTED DB FIELD] Model '{entity_name}' có trường {missing_in_schema} chưa xuất hiện trong '{resp_schema_name}'."
                warnings.append(msg)
                print(f"   │   {msg}")

            # Đối chiếu Response Schema -> Frontend TS Interface
            fe_iface = frontend_types.get(entity_name) or frontend_types.get(f"{entity_name}Item")
            if fe_iface is not None:
                print(f"   │ • Web TS   ({entity_name:<12}): {len(fe_iface)} trường -> {sorted(list(fe_iface))}")
                missing_in_fe = resp_fields - fe_iface
                if missing_in_fe:
                    msg = f"❌ [CONTRACT DRIFT] Web TS interface '{entity_name}' thiếu trường {missing_in_fe} từ '{resp_schema_name}'!"
                    errors.append(msg)
                    print(f"   │   {msg}")

                extra_in_fe = fe_iface - resp_fields
                if extra_in_fe:
                    msg = f"⚠️ [CLIENT EXTRA] Web TS interface '{entity_name}' có trường phụ {extra_in_fe} không có trong Backend Schema."
                    warnings.append(msg)
                    print(f"   │   {msg}")
            else:
                msg = f"⚠️ [MISSING WEB INTERFACE] Chưa tìm thấy TypeScript interface '{entity_name}' trong src/frontend/src/types/"
                warnings.append(msg)
                print(f"   │   {msg}")

            # Đối chiếu Web TS Interface -> Mobile TS Interface
            if mobile_types_dir.exists() and any(mobile_types_dir.glob("*.ts")):
                mo_iface = mobile_types.get(entity_name) or mobile_types.get(f"{entity_name}Item")
                if mo_iface is not None:
                    print(f"   │ • Mobile TS({entity_name:<12}): {len(mo_iface)} trường -> {sorted(list(mo_iface))}")
                    if fe_iface is not None and fe_iface != mo_iface:
                        diff = fe_iface.symmetric_difference(mo_iface)
                        msg = f"❌ [CLIENT DESYNC] Web Interface và Mobile Interface '{entity_name}' bất đồng bộ tại các trường: {diff}"
                        errors.append(msg)
                        print(f"   │   {msg}")
                else:
                    msg = f"ℹ️ [MOBILE INTERFACE] Chưa có TypeScript interface '{entity_name}' trong src/mobile/src/types/"
                    warnings.append(msg)
                    print(f"   │   {msg}")

            if not any(err for err in errors if entity_name in err):
                print(f"   └── ✅ Khớp nối hợp đồng hoàn hảo cho thực thể '{entity_name}'!")
            else:
                print(f"   └── ❌ Phát hiện sai lệch hợp đồng tại thực thể '{entity_name}'!")
        else:
            msg = f"⚠️ [MISSING RESPONSE SCHEMA] Chưa tìm thấy schema phản hồi cho model '{entity_name}'"
            warnings.append(msg)
            print(f"   └── {msg}")

        # =====================================================================
        # BƯỚC 3: ĐỐI CHIẾU CHÉO PAYLOAD TẠO MỚI (CREATE PAYLOAD MATCHING)
        # =====================================================================
        create_schema_name = f"{entity_name}Create"
        if create_schema_name in schemas:
            create_fields = schemas[create_schema_name]
            create_payload_candidates = [f"{entity_name}CreatePayload", f"{entity_name}Create", f"{entity_name}Input"]
            fe_create_payload = next((frontend_types[p] for p in create_payload_candidates if p in frontend_types), None)

            if fe_create_payload is not None:
                payload_diff = create_fields.symmetric_difference(fe_create_payload)
                if payload_diff:
                    msg = f"❌ [PAYLOAD DESYNC] Payload tạo mới '{entity_name}' bất đồng bộ trường: {payload_diff}"
                    errors.append(msg)
                    print(f"   ⚠️ {msg}")
                else:
                    print(f"   └── ✅ Khớp nối 100% Payload tạo mới: {create_schema_name} ↔ CreatePayload")

    # =========================================================================
    # TỔNG KẾT & KẾT QUẢ ĐÁNH GIÁ
    # =========================================================================
    print("\n" + "=" * 72)
    if warnings:
        print(f"⚠️ CẢNH BÁO TỒN ĐỌNG ({len(warnings)} lưu ý):")
        for w in warnings:
            print(f"   • {w}")
        print("-" * 72)

    if errors:
        print(f"❌ [CONTRACT SYNC FAILED] Phát hiện {len(errors)} vi phạm hợp đồng dữ liệu nghiêm trọng:")
        for e in errors:
            print(f"   • {e}")
        print("=" * 72)
        sys.exit(1)

    print("🎉 [CONTRACT SYNC PASSED] Toàn bộ hợp đồng dữ liệu đồng bộ chuẩn xác 100%!")
    print("   • Casing: 100% snake_case")
    print("   • Security: Zero sensitive field leaks")
    print("   • Cross-Layer Consistency: Database ↔ Backend ↔ Frontend ↔ Mobile hoàn toàn ăn khớp")
    print("=" * 72)
    sys.exit(0)


if __name__ == "__main__":
    main()
