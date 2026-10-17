#!/usr/bin/env python3
"""
generate_offline_migration.py
Công cụ tự động tạo revision Alembic Migration ngoại tuyến (Offline Migration Generator).
Cho phép sinh file migration mới nối tiếp head hiện tại mà không cần kết nối tới database sống.
"""

import datetime
import re
import sys
from pathlib import Path


def find_current_head(versions_dir: Path) -> str:
    """Tìm revision ID của head hiện tại trong versions_dir"""
    revisions = {}
    down_revisions = {}

    for file in versions_dir.glob("*.py"):
        if file.name.startswith("__"):
            continue
        content = file.read_text(encoding="utf-8")
        rev_match = re.search(r"revision\s*:\s*str\s*=\s*['\"]([^'\"]+)['\"]", content)
        down_match = re.search(
            r"down_revision\s*:\s*Union\[str,\s*None\]\s*=\s*(['\"][^'\"]+['\"]|None)",
            content,
        )

        if not rev_match:
            rev_match = re.search(r"revision\s*=\s*['\"]([^'\"]+)['\"]", content)
        if not down_match:
            down_match = re.search(r"down_revision\s*=\s*(['\"][^'\"]+['\"]|None)", content)

        if rev_match:
            rev_id = rev_match.group(1)
            down_id = None
            if down_match and down_match.group(1) != "None":
                down_id = down_match.group(1).strip("'\"")
            revisions[rev_id] = file.name
            down_revisions[rev_id] = down_id

    # Head là revision không xuất hiện trong bất kỳ down_revision nào
    referenced_as_down = set(down_revisions.values())
    heads = [r for r in revisions if r not in referenced_as_down]

    if heads:
        return heads[0]
    return "0001_initial_schema"


def create_migration(slug: str):
    root = Path(__file__).resolve().parent.parent
    versions_dir = root / "src" / "db" / "migrations" / "versions"
    versions_dir.mkdir(parents=True, exist_ok=True)

    current_head = find_current_head(versions_dir)

    # Đếm số lượng revisions hiện có để tạo prefix
    count = len(list(versions_dir.glob("*.py"))) + 1
    new_rev = f"{count:04d}_{slug}"
    file_path = versions_dir / f"{new_rev}.py"

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.000000")

    template = f'''"""{slug}

Revision ID: {new_rev}
Revises: {current_head}
Create Date: {now_str}

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '{new_rev}'
down_revision: Union[str, None] = '{current_head}'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # TODO: Thêm các thao tác op.create_table hoặc op.add_column tại đây
    pass

def downgrade() -> None:
    # TODO: Thêm các thao tác op.drop_table hoặc op.drop_column tương ứng
    pass
'''

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(template)

    print(f"✅ [MIGRATION GENERATOR] Đã tạo revision mới: {new_rev}")
    print(f"   • Tệp: {file_path}")
    print(f"   • Down Revision (tiền nhiệm): {current_head}")


def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else "new_feature"
    create_migration(slug)


if __name__ == "__main__":
    main()
