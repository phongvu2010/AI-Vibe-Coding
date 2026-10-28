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

SNAKE_CASE_PATTERN = re.compile(r"^[a-z0-9]+(_[a-z0-9]+)*$")
CAMEL_CASE_PATTERN = re.compile(r"^[a-z]+[A-Z0-9]")


def is_snake_case(name: str) -> bool:
    """Kiểm tra tên trường có tuân thủ 100% chuẩn snake_case không."""
    if name.startswith("_"):
        name = name[1:]
    return bool(SNAKE_CASE_PATTERN.match(name))


def is_camel_case(name: str) -> bool:
    """Kiểm tra tên trường có mang định dạng camelCase hay không."""
    return bool(CAMEL_CASE_PATTERN.match(name))


def extract_plan_matrix_fields(plan_file: Path) -> List[Dict[str, str]]:
    """Bóc tách các trường từ bảng Ma Trận Hợp Đồng Dữ Liệu Đa Tầng trong plan.md."""
    if not plan_file.exists():
        return []

    fields = []
    in_matrix_section = False
    try:
        with open(plan_file, encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return []

    for idx, line in enumerate(lines, start=1):
        if any(h in line for h in [
            "Cross-Layer Data Contract Matrix",
            "Cross-Layer Contract Matrix",
            "Ma Trận Hợp Đồng Dữ Liệu",
            "Ma Trận Ánh Xạ Dữ Liệu"
        ]):
            in_matrix_section = True
            continue
        if in_matrix_section and line.startswith("## ") and not any(h in line for h in ["Cross-Layer", "Ma Trận", "Contract Matrix"]):
            in_matrix_section = False
            break

        if in_matrix_section and "|" in line:
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 3:
                first = parts[0].replace("`", "").strip().lower()
                if (
                    first.startswith(("-", ":", "---"))
                    or "tên trường" in first
                    or "field" in first
                    or first == ""
                ):
                    continue
                field_name = parts[0].replace("`", "").strip()
                db_type = parts[1].replace("`", "").strip() if len(parts) > 1 else ""
                backend_type = parts[2].replace("`", "").strip() if len(parts) > 2 else ""
                frontend_type = parts[3].replace("`", "").strip() if len(parts) > 3 else ""
                if field_name:
                    fields.append({
                        "name": field_name,
                        "db_type": db_type,
                        "backend_type": backend_type,
                        "frontend_type": frontend_type,
                        "line": str(idx),
                    })
    return fields


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


def extract_backend_pydantic_fields(schemas_dir: Path) -> Dict[str, List[Dict[str, str]]]:
    """Bóc tách chi tiết các trường Pydantic kèm file và dòng (tương thích AI-Team-Dev)."""
    results: Dict[str, List[Dict[str, str]]] = {}
    if not schemas_dir.exists():
        return results

    for py_file in schemas_dir.glob("*.py"):
        if py_file.name.startswith("__"):
            continue
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        except Exception:
            continue

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                fields = []
                for item in node.body:
                    if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                        if not item.target.id.startswith("_") and item.target.id not in ["model_config", "Config"]:
                            fields.append({
                                "name": item.target.id,
                                "type": ast.unparse(item.annotation) if hasattr(ast, "unparse") else "",
                                "file": py_file.name,
                                "line": str(item.lineno),
                            })
                if fields:
                    results[node.name] = fields
    return results


def extract_pydantic_schemas_with_types(schemas_dir: Path) -> Dict[str, Dict[str, str]]:
    """Bóc tách Pydantic schemas kèm kiểu dữ liệu từng trường và giải quyết kế thừa."""
    raw_classes: Dict[str, Tuple[List[str], Dict[str, str]]] = {}
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
                    fields: Dict[str, str] = {}
                    for item in node.body:
                        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                            if item.target.id not in ["model_config", "Config"]:
                                type_str = ast.unparse(item.annotation) if hasattr(ast, "unparse") else "Any"
                                fields[item.target.id] = type_str
                        elif isinstance(item, ast.Assign):
                            for target in item.targets:
                                if isinstance(target, ast.Name) and target.id not in ["model_config", "Config"]:
                                    fields[target.id] = "Any"
                    raw_classes[node.name] = (base_names, fields)
        except Exception as e:
            print(f"⚠️ Không thể parse Schema file {file.name}: {e}")

    resolved: Dict[str, Dict[str, str]] = {}

    def resolve_typed_fields(cls_name: str, visited: Optional[Set[str]] = None) -> Dict[str, str]:
        if visited is None:
            visited = set()
        if cls_name in visited or cls_name not in raw_classes:
            return {}
        visited.add(cls_name)

        bases, direct_fields = raw_classes[cls_name]
        total = dict(direct_fields)
        for b in bases:
            inherited = resolve_typed_fields(b, visited.copy())
            for k, v in inherited.items():
                if k not in total:
                    total[k] = v
        return total

    for name in raw_classes:
        resolved[name] = resolve_typed_fields(name)

    return resolved


def extract_frontend_ts_fields(types_dir: Path) -> Dict[str, List[Dict[str, str]]]:
    """Bóc tách chi tiết các trường TypeScript Interface kèm file và type (tương thích AI-Team-Dev)."""
    results: Dict[str, List[Dict[str, str]]] = {}
    if not types_dir.exists():
        return results

    interface_pattern = re.compile(
        r"(?:export\s+)?(?:interface|type)\s+([A-Za-z0-9_]+)(?:\s*=\s*|\s+extends[^{]+)?\s*\{([^}]+)\}",
        re.DOTALL,
    )
    prop_pattern = re.compile(r"^\s*([a-zA-Z0-9_]+)\s*\??\s*:\s*([^;]+);?", re.MULTILINE)

    for ts_file in types_dir.glob("**/*.ts"):
        try:
            content = ts_file.read_text(encoding="utf-8")
        except Exception:
            continue

        for match in interface_pattern.finditer(content):
            iface_name = match.group(1)
            body = match.group(2)
            fields = []
            for prop in prop_pattern.finditer(body):
                fields.append({
                    "name": prop.group(1),
                    "type": prop.group(2).strip(),
                    "file": ts_file.name,
                })
            if fields:
                results[iface_name] = fields
    return results


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


def extract_ts_interfaces_with_types(types_dir: Path) -> Dict[str, Dict[str, str]]:
    """Bóc tách TypeScript Interfaces kèm kiểu dữ liệu từng trường."""
    interfaces: Dict[str, Dict[str, str]] = {}
    if not types_dir.exists():
        return interfaces

    for file in sorted(types_dir.glob("*.ts")):
        try:
            content = file.read_text(encoding="utf-8")
            current_iface = None
            for line in content.splitlines():
                line_str = line.strip()

                match_iface = re.match(r"^(?:export\s+)?interface\s+([A-Za-z0-9_]+)", line_str)
                if match_iface:
                    current_iface = match_iface.group(1)
                    if current_iface not in interfaces:
                        interfaces[current_iface] = {}
                    continue

                if current_iface:
                    if line_str.startswith("}"):
                        current_iface = None
                        continue

                    match_field = re.match(r"^([a-zA-Z0-9_]+)\??\s*:\s*([^;]+);?", line_str)
                    if match_field:
                        field_name = match_field.group(1)
                        field_type = match_field.group(2).strip()
                        interfaces[current_iface][field_name] = field_type
        except Exception as e:
            print(f"⚠️ Không thể đọc TS types file {file.name}: {e}")

    return interfaces


def check_type_compatibility(py_type: str, ts_type: str) -> Tuple[bool, str]:
    """Kiểm tra tính tương thích giữa kiểu dữ liệu Python Pydantic và TypeScript."""
    py_t = py_type.strip()
    ts_t = ts_type.strip().rstrip(";")

    # Chuẩn hóa Optional / Union / None
    py_t_clean = re.sub(r"Optional\[(.*)\]", r"\1", py_t)
    py_t_clean = re.sub(r"Union\[(.*),\s*NoneType?\]", r"\1", py_t_clean)
    py_t_clean = re.sub(r"(.*?)\s*\|\s*None", r"\1", py_t_clean).strip()

    ts_t_clean = re.sub(r"\s*\|\s*(?:null|undefined)", "", ts_t).strip()

    # Any / unknown
    if py_t_clean in ("Any", "object") or ts_t_clean in ("any", "unknown"):
        return True, "Khớp kiểu linh hoạt"

    # String types
    string_py_types = {"str", "EmailStr", "uuid.UUID", "UUID", "datetime", "date", "time", "HttpUrl"}
    if any(st in py_t_clean for st in string_py_types):
        if ts_t_clean in ("string", "any", "Date") or ts_t_clean.startswith("string |") or "string" in ts_t_clean:
            return True, "Khớp kiểu chuỗi"
        return False, f"Python '{py_type}' kỳ vọng TypeScript 'string', nhưng nhận được '{ts_type}'"

    # Number types
    number_py_types = {"int", "float", "Decimal"}
    if py_t_clean in number_py_types:
        if ts_t_clean in ("number", "any") or "number" in ts_t_clean:
            return True, "Khớp kiểu số"
        return False, f"Python '{py_type}' kỳ vọng TypeScript 'number', nhưng nhận được '{ts_type}'"

    # Boolean types
    if py_t_clean in ("bool", "boolean"):
        if ts_t_clean in ("boolean", "any"):
            return True, "Khớp kiểu boolean"
        return False, f"Python '{py_type}' kỳ vọng TypeScript 'boolean', nhưng nhận được '{ts_type}'"

    # List / Array types
    if py_t_clean.startswith(("List[", "list[", "Sequence[")):
        if "[]" in ts_t_clean or ts_t_clean.startswith("Array<") or ts_t_clean == "any":
            return True, "Khớp kiểu mảng (array)"
        return False, f"Python '{py_type}' kỳ vọng TypeScript Array/[] nhưng nhận được '{ts_type}'"

    # Dict / Record types
    if py_t_clean.startswith(("Dict[", "dict[", "Mapping[")):
        if ts_t_clean.startswith("Record<") or ts_t_clean in ("any", "object"):
            return True, "Khớp kiểu object/record"
        return False, f"Python '{py_type}' kỳ vọng TypeScript Record<...> nhưng nhận được '{ts_type}'"

    return True, "Kiểu tùy biến chấp nhận tương thích"


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
    schemas_with_types = extract_pydantic_schemas_with_types(schemas_dir)
    frontend_types = extract_ts_interfaces(frontend_types_dir)
    frontend_types_with_types = extract_ts_interfaces_with_types(frontend_types_dir)
    mobile_types = extract_ts_interfaces(mobile_types_dir)
    mobile_types_with_types = extract_ts_interfaces_with_types(mobile_types_dir)

    print(f"   • Đã quét: {len(db_models)} DB Models | {len(schemas)} Schemas | "
          f"{len(frontend_types)} Web Interfaces | {len(mobile_types)} Mobile Interfaces")

    errors: List[str] = []
    warnings: List[str] = []

    # =========================================================================
    # BƯỚC 0: ĐỐI CHIẾU VỚI KẾ HOẠCH KIẾN TRÚC PLAN.MD (CONTRACT MATRIX)
    # =========================================================================
    print("\n▶ 0. KIỂM ĐỊNH KẾ HOẠCH KIẾN TRÚC PLAN.MD (CONTRACT MATRIX):")
    plan_files = []
    if feature_slug != "toàn dự án":
        target_plan = root / "docs" / "specs" / feature_slug / "plan.md"
        if target_plan.exists():
            plan_files.append(target_plan)
        else:
            print(f"   ℹ️ Không tìm thấy plan.md đặc thù tại docs/specs/{feature_slug}/")
    else:
        plan_files = sorted(list(root.glob("docs/specs/*/plan.md")))

    if not plan_files:
        print("   ℹ️ Chưa có plan.md nào trong docs/specs/ (Bỏ qua bước kiểm tra plan).")
    else:
        for plan_path in plan_files:
            rel_plan = plan_path.relative_to(root)
            print(f"   📄 Đang phân tích ma trận dữ liệu: {rel_plan}")
            matrix_fields = extract_plan_matrix_fields(plan_path)
            if not matrix_fields:
                print("      ⚠️ Không phát hiện bảng Ma Trận Hợp Đồng Dữ Liệu Đa Tầng trong plan.")
            else:
                plan_casing_errors = 0
                for f_info in matrix_fields:
                    f_name = f_info["name"]
                    if is_camel_case(f_name):
                        msg = f"❌ [PLAN CAMEL_CASE VIOLATION] [{rel_plan}:L{f_info['line']}] Trường '{f_name}' dùng camelCase!"
                        errors.append(msg)
                        plan_casing_errors += 1
                        print(f"      {msg}")
                    elif not is_snake_case(f_name):
                        msg = f"❌ [PLAN INVALID CASING] [{rel_plan}:L{f_info['line']}] Trường '{f_name}' không phải snake_case!"
                        errors.append(msg)
                        plan_casing_errors += 1
                        print(f"      {msg}")
                if plan_casing_errors == 0:
                    print(f"      ✅ Đã xác thực {len(matrix_fields)} trường trong plan.md: 100% snake_case hợp lệ.")

    # =========================================================================
    # BƯỚC 1: KIỂM TRA CHUẨN CASING (100% snake_case & Chặn bắt camelCase)
    # =========================================================================
    print("\n▶ 1. KIỂM TRA CHUẨN CASING (100% snake_case):")
    casing_violations = []

    for model, f_set in db_models.items():
        for f in f_set:
            if is_camel_case(f):
                casing_violations.append(f"❌ [DB Model: {model}] Thuộc tính '{f}' dùng camelCase thay vì snake_case!")
            elif not is_snake_case(f):
                casing_violations.append(f"❌ [DB Model: {model}] Thuộc tính '{f}' không tuân thủ snake_case!")

    for schema, f_set in schemas.items():
        for f in f_set:
            if is_camel_case(f):
                casing_violations.append(f"❌ [Pydantic Schema: {schema}] Thuộc tính '{f}' dùng camelCase thay vì snake_case!")
            elif not is_snake_case(f):
                casing_violations.append(f"❌ [Pydantic Schema: {schema}] Thuộc tính '{f}' không tuân thủ snake_case!")

    for iface, f_set in frontend_types.items():
        for f in f_set:
            if is_camel_case(f):
                casing_violations.append(f"❌ [Frontend TS: {iface}] Thuộc tính '{f}' dùng camelCase thay vì snake_case!")
            elif not is_snake_case(f):
                casing_violations.append(f"❌ [Frontend TS: {iface}] Thuộc tính '{f}' không tuân thủ snake_case!")

    for iface, f_set in mobile_types.items():
        for f in f_set:
            if is_camel_case(f):
                casing_violations.append(f"❌ [Mobile TS: {iface}] Thuộc tính '{f}' dùng camelCase thay vì snake_case!")
            elif not is_snake_case(f):
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
    # BƯỚC 4: ĐỐI CHIẾU TƯƠNG THÍCH KIỂU DỮ LIỆU ĐA TẦNG (DATA TYPE COMPATIBILITY)
    # =========================================================================
    print("\n▶ 4. ĐỐI CHIẾU TƯƠNG THÍCH KIỂU DỮ LIỆU ĐA TẦNG (PYDANTIC ↔ TYPESCRIPT):")
    type_checks_passed = 0
    type_checks_total = 0
    for entity_name in db_models:
        resp_schema = f"{entity_name}Response"
        if resp_schema in schemas_with_types:
            py_fields = schemas_with_types[resp_schema]
            # Match against Frontend TS interface
            fe_iface = frontend_types_with_types.get(entity_name) or frontend_types_with_types.get(f"{entity_name}Item")
            if fe_iface:
                for fname, py_type in py_fields.items():
                    if fname in fe_iface:
                        ts_type = fe_iface[fname]
                        type_checks_total += 1
                        ok, reason = check_type_compatibility(py_type, ts_type)
                        if ok:
                            type_checks_passed += 1
                        else:
                            msg = f"❌ [TYPE INCOMPATIBILITY] '{entity_name}.{fname}': Backend ({py_type}) ↔ Web TS ({ts_type}) - {reason}"
                            errors.append(msg)
                            print(f"   {msg}")

            # Match against Mobile TS interface
            mo_iface = mobile_types_with_types.get(entity_name) or mobile_types_with_types.get(f"{entity_name}Item")
            if mo_iface:
                for fname, py_type in py_fields.items():
                    if fname in mo_iface:
                        ts_type = mo_iface[fname]
                        type_checks_total += 1
                        ok, reason = check_type_compatibility(py_type, ts_type)
                        if ok:
                            type_checks_passed += 1
                        else:
                            msg = f"❌ [TYPE INCOMPATIBILITY] '{entity_name}.{fname}': Backend ({py_type}) ↔ Mobile TS ({ts_type}) - {reason}"
                            errors.append(msg)
                            print(f"   {msg}")

    if type_checks_total > 0 and not any("[TYPE INCOMPATIBILITY]" in e for e in errors):
        print(f"   └── ✅ Toàn bộ {type_checks_total} cặp trường dữ liệu khớp chuẩn kiểu dữ liệu giữa Pydantic và TypeScript!")
    elif type_checks_total == 0:
        print("   └── ℹ️ Không phát hiện cặp trường đối ứng trực tiếp để so sánh kiểu dữ liệu.")

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
