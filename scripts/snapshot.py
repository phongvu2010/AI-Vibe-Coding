#!/usr/bin/env python3
"""
snapshot.py
Công cụ chụp ảnh nhanh mã nguồn & khôi phục trạng thái an toàn (Snapshot & Rollback).
Bảo vệ mã nguồn trước các đợt refactor hoặc khi vòng lặp tự sửa lỗi gặp sự cố.
"""

import datetime
import sys
import tarfile
from pathlib import Path


def create_snapshot(tag: str = "auto") -> Path:
    root = Path(__file__).resolve().parent.parent
    snapshot_dir = root / "dist" / "snapshots"
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"snapshot_{tag}_{timestamp}.tar.gz"
    archive_path = snapshot_dir / archive_name

    print(f"📦 [SNAPSHOT] Đang chụp nhanh mã nguồn vào: {archive_name}...")

    # Các thư mục cần sao lưu
    include_dirs = ["src", "config", "docs", "scripts"]

    with tarfile.open(archive_path, "w:gz") as tar:
        for item in include_dirs:
            item_path = root / item
            if item_path.exists():
                tar.add(item_path, arcname=item)

    print(f"✅ [SNAPSHOT COMPLETED] Đã lưu snapshot tại: {archive_path}")
    return archive_path

def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else "manual"
    create_snapshot(tag)

if __name__ == "__main__":
    main()
