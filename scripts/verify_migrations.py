#!/usr/bin/env python3
"""
verify_migrations.py
Kiểm tra tính toàn vẹn của đồ thị phân nhánh Alembic Migration (Migration DAG Integrity).
Đảm bảo không có nhánh mồ côi (orphan branches) hoặc đứt gãy chuỗi revisions.
"""

import sys
import re
from pathlib import Path

def check_migrations():
    root = Path(__file__).resolve().parent.parent
    versions_dir = root / "src" / "db" / "migrations" / "versions"

    print("🔍 [MIGRATION DAG] Đang kiểm tra tính toàn vẹn của Alembic migrations...")
    if not versions_dir.exists():
        print("⚠️ [MIGRATION DAG] Thư mục migrations/versions chưa tồn tại. Bỏ qua kiểm tra.")
        sys.exit(0)

    revisions = {}
    down_revisions = {}

    migration_files = list(versions_dir.glob("*.py"))
    if not migration_files:
        print("ℹ️ [MIGRATION DAG] Chưa có file migration nào. Hệ thống sẵn sàng cho lần khởi tạo đầu tiên.")
        sys.exit(0)

    for file in migration_files:
        if file.name.startswith("__"):
            continue
        content = file.read_text(encoding="utf-8")
        
        rev_match = re.search(r"revision\s*:\s*str\s*=\s*['\"]([^'\"]+)['\"]", content)
        down_match = re.search(r"down_revision\s*:\s*Union\[str,\s*None\]\s*=\s*(['\"][^'\"]+['\"]|None)", content)
        
        if not rev_match:
            # Fallback pattern
            rev_match = re.search(r"revision\s*=\s*['\"]([^'\"]+)['\"]", content)
        if not down_match:
            down_match = re.search(r"down_revision\s*=\s*(['\"][^'\"]+['\"]|None)", content)

        if rev_match:
            rev_id = rev_match.group(1)
            revisions[rev_id] = file.name
            
            down_id = None
            if down_match and down_match.group(1) != "None":
                down_id = down_match.group(1).strip("'\"")
            down_revisions[rev_id] = down_id

    # Kiểm tra liên kết
    errors = []
    roots = []
    for rev, down in down_revisions.items():
        if down is None:
            roots.append(rev)
        elif down not in revisions:
            errors.append(f"❌ [BROKEN CHAIN] Revision '{rev}' ({revisions[rev]}) tham chiếu down_revision '{down}' không tồn tại!")

    if len(roots) > 1:
        errors.append(f"⚠️ [MULTIPLE ROOTS] Phát hiện nhiều hơn 1 revision gốc: {roots}")

    if errors:
        print("\n".join(errors))
        print("❌ [MIGRATION DAG FAILED] Đồ thị migration bị lỗi!")
        sys.exit(1)

    print(f"✅ [MIGRATION DAG PASSED] {len(revisions)} revisions liên kết hợp lệ, đồ thị chuỗi hoàn hảo.")
    sys.exit(0)

if __name__ == "__main__":
    check_migrations()
