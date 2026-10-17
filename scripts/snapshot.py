#!/usr/bin/env python3
"""
snapshot.py — Công cụ chụp ảnh nhanh mã nguồn & Khôi phục an toàn (Snapshot & Instant Rollback)
Thuộc hệ thống AI-Vibe-Coding (Antigravity 2.0).
Tự động lọc bỏ các thư mục rác (node_modules, .venv, __pycache__, dist) giúp tốc độ chụp < 1 giây.
"""

import datetime
import os
import sys
import tarfile
from pathlib import Path

# Đảm bảo console UTF-8 trên Windows
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
SNAPSHOT_DIR = ROOT_DIR / "dist" / "snapshots"

EXCLUDE_DIRS = {
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "node_modules",
    ".next",
    ".expo",
    ".git",
    "dist",
    "build",
}

EXCLUDE_EXTS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".sqlite",
    ".sqlite3",
    ".db",
    ".log",
    ".tmp",
    ".DS_Store",
}


def should_include_file(file_path: Path) -> bool:
    for part in file_path.parts:
        if part in EXCLUDE_DIRS:
            return False
    if file_path.suffix in EXCLUDE_EXTS:
        return False
    return True


def create_snapshot(tag: str = "auto") -> Path:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"snapshot_{tag}_{timestamp}.tar.gz"
    archive_path = SNAPSHOT_DIR / archive_name

    print(f"📦 [SNAPSHOT] Đang chụp nhanh mã nguồn vào: {archive_name}...")
    include_dirs = ["src", "config", "docs", "scripts", "templates"]

    def filter_tar(tarinfo):
        path_obj = Path(tarinfo.name)
        if not should_include_file(path_obj):
            return None
        return tarinfo

    with tarfile.open(archive_path, "w:gz") as tar:
        for item in include_dirs:
            item_path = ROOT_DIR / item
            if item_path.exists():
                tar.add(item_path, arcname=item, filter=filter_tar)

    print(f"✅ [SNAPSHOT COMPLETED] Đã lưu snapshot tại: {archive_path.relative_to(ROOT_DIR)}")
    return archive_path


def restore_snapshot(archive_name: str) -> bool:
    archive_path = SNAPSHOT_DIR / archive_name
    if not archive_path.exists():
        matches = list(SNAPSHOT_DIR.glob(f"*{archive_name}*"))
        if matches:
            archive_path = matches[0]
        else:
            print(f"❌ Không tìm thấy file snapshot: {archive_name}")
            return False

    print(f"🔄 Đang khôi phục mã nguồn từ {archive_path.name}...")
    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(path=ROOT_DIR)
        print(f"✅ [ROLLBACK COMPLETED] Khôi phục mã nguồn thành công từ {archive_path.name}!")
        return True
    except Exception as e:
        print(f"❌ Lỗi khi khôi phục snapshot: {e}")
        return False


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "restore":
        if len(sys.argv) < 3:
            print("Cách dùng: python scripts/snapshot.py restore <snapshot_filename>")
            sys.exit(1)
        restore_snapshot(sys.argv[2])
    else:
        tag = sys.argv[1] if len(sys.argv) > 1 else "manual"
        create_snapshot(tag)


if __name__ == "__main__":
    main()
