#!/usr/bin/env python3
"""snapshot.py — Công cụ chụp ảnh nhanh mã nguồn & Khôi phục an toàn (Snapshot & Instant Rollback).

Thuộc hệ thống AI-Vibe-Coding (Antigravity 2.0).
Tự động lọc bỏ các thư mục rác (node_modules, .venv, __pycache__, dist) giúp tốc độ chụp < 1 giây.
Hỗ trợ cả 2 cơ chế:
1. Live Directory Snapshot (.snapshots/): Dạng thư mục sống, cho phép xem file và git diff trực tiếp.
2. Compressed Archive Snapshot (dist/snapshots/): File nén .tar.gz lưu trữ nhỏ gọn.

Usage:
    python scripts/snapshot.py take [name] [--dir]
    python scripts/snapshot.py list
    python scripts/snapshot.py diff <name>
    python scripts/snapshot.py restore <snapshot_name>
    python scripts/snapshot.py clean [--keep 3] [--all]
"""

import argparse
import datetime
import os
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

# Đảm bảo console UTF-8 trên Windows
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
ARCHIVE_DIR = ROOT_DIR / "dist" / "snapshots"
LIVE_DIR = ROOT_DIR / ".snapshots"

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
    ".snapshots",
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

INCLUDE_DIRS = ["src", "config", "docs", "scripts", "templates"]


def should_include_file(file_path: Path) -> bool:
    for part in file_path.parts:
        if part in EXCLUDE_DIRS:
            return False
    if file_path.suffix in EXCLUDE_EXTS:
        return False
    return True


def copy_filtered_tree(src: Path, dst: Path):
    """Copy directory recursively skipping excluded files (Live Directory Snapshot)."""
    if not src.exists():
        return
    dst.mkdir(parents=True, exist_ok=True)
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        rel_root = Path(root).relative_to(src)
        target_root = dst / rel_root
        target_root.mkdir(parents=True, exist_ok=True)
        for f in files:
            src_file = Path(root) / f
            if should_include_file(src_file):
                shutil.copy2(src_file, target_root / f)


def create_snapshot(tag: str = "auto", as_dir: bool = False) -> Path:
    """Tạo snapshot mã nguồn (dạng thư mục uncompressed hoặc file nén .tar.gz)."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = (tag or "manual").strip().lower().replace(" ", "_")

    if as_dir:
        LIVE_DIR.mkdir(parents=True, exist_ok=True)
        target_dir = LIVE_DIR / f"{safe_name}_{timestamp}"
        target_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 [LIVE SNAPSHOT] Đang sao chép thư mục sống vào: {target_dir.name}...")
        for item in INCLUDE_DIRS:
            item_path = ROOT_DIR / item
            if item_path.exists():
                copy_filtered_tree(item_path, target_dir / item)

        meta_file = target_dir / "SNAPSHOT_META.txt"
        meta_file.write_text(
            f"Snapshot Name: {safe_name}\n"
            f"Type: Live Directory\n"
            f"Created At: {datetime.datetime.now().isoformat()}\n"
            f"Timestamp: {timestamp}\n",
            encoding="utf-8"
        )
        print(f"✅ [LIVE SNAPSHOT COMPLETED] Đã lưu tại: {target_dir.relative_to(ROOT_DIR)}")
        print(f"👉 Xem diff với hiện tại: python scripts/snapshot.py diff {target_dir.name}")
        return target_dir
    else:
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        archive_name = f"snapshot_{safe_name}_{timestamp}.tar.gz"
        archive_path = ARCHIVE_DIR / archive_name
        print(f"📦 [ARCHIVE SNAPSHOT] Đang đóng gói mã nguồn vào: {archive_name}...")

        def filter_tar(tarinfo):
            path_obj = Path(tarinfo.name)
            if not should_include_file(path_obj):
                return None
            return tarinfo

        with tarfile.open(archive_path, "w:gz") as tar:
            for item in INCLUDE_DIRS:
                item_path = ROOT_DIR / item
                if item_path.exists():
                    tar.add(item_path, arcname=item, filter=filter_tar)

        print(f"✅ [ARCHIVE SNAPSHOT COMPLETED] Đã lưu tại: {archive_path.relative_to(ROOT_DIR)}")
        return archive_path


# Alias for backward-compatibility with AI-Team-Dev
take_snapshot = create_snapshot


def list_snapshots():
    """Liệt kê toàn bộ snapshots hiện có cả dạng thư mục sống (.snapshots) và nén (dist/snapshots)."""
    print("\n" + "=" * 78)
    print("📋 DANH SÁCH BẢN CHỤP MÃ NGUỒN (AVAILABLE SNAPSHOTS)")
    print("=" * 78)

    has_any = False
    idx = 1

    # 1. Live Directory Snapshots
    if LIVE_DIR.exists():
        live_snaps = sorted([d for d in LIVE_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")],
                            key=lambda d: d.stat().st_mtime, reverse=True)
        if live_snaps:
            has_any = True
            print("  --- 📁 LIVE DIRECTORY SNAPSHOTS (.snapshots/ - Hỗ trợ Diff & Browse) ---")
            for s in live_snaps:
                mtime = datetime.datetime.fromtimestamp(s.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                print(f"  [{idx:2d}] (DIR) {s.name:<45} (Tạo lúc: {mtime})")
                idx += 1

    # 2. Archive Snapshots
    if ARCHIVE_DIR.exists():
        tar_snaps = sorted(ARCHIVE_DIR.glob("*.tar.gz"), key=lambda f: f.stat().st_mtime, reverse=True)
        if tar_snaps:
            has_any = True
            print("  --- 📦 COMPRESSED ARCHIVES (dist/snapshots/*.tar.gz) ---")
            for s in tar_snaps:
                mtime = datetime.datetime.fromtimestamp(s.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                size_kb = s.stat().st_size / 1024
                print(f"  [{idx:2d}] (TAR) {s.name:<45} ({size_kb:6.1f} KB | {mtime})")
                idx += 1

    if not has_any:
        print("  ℹ️ Chưa có bản chụp snapshot nào được lưu.")

    print("=" * 78)
    print("👉 Khôi phục: python scripts/snapshot.py restore <snapshot_name>")
    print("👉 Xem diff : python scripts/snapshot.py diff <dir_snapshot_name>\n")


def diff_snapshot(target_name: str):
    """So sánh thay đổi giữa mã nguồn hiện tại và một bản snapshot thư mục."""
    if not LIVE_DIR.exists():
        print("❌ Thư mục .snapshots/ không tồn tại.")
        return

    matches = [d for d in LIVE_DIR.iterdir() if d.is_dir() and target_name in d.name]
    if not matches:
        print(f"❌ Không tìm thấy live snapshot nào khớp với: '{target_name}'")
        return

    target_dir = matches[0]
    print(f"\n🔍 [DIFF] So sánh hiện tại với Snapshot: '{target_dir.name}'...")

    import filecmp
    modified, added, deleted = [], [], []

    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        rel = Path(root).relative_to(target_dir)
        for f in files:
            if f == "SNAPSHOT_META.txt":
                continue
            p1 = target_dir / rel / f
            p2 = ROOT_DIR / rel / f
            if not p2.exists():
                deleted.append(str(rel / f))
            elif should_include_file(p2) and not filecmp.cmp(p1, p2, shallow=False):
                modified.append(str(rel / f))

    for item in INCLUDE_DIRS:
        base = ROOT_DIR / item
        if not base.exists():
            continue
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            rel = Path(root).relative_to(ROOT_DIR)
            for f in files:
                p2 = ROOT_DIR / rel / f
                if not should_include_file(p2):
                    continue
                p1 = target_dir / rel / f
                if not p1.exists():
                    added.append(str(rel / f))

    print(f"📊 Kết quả đối soát: {len(modified)} sửa đổi, {len(added)} tạo mới, {len(deleted)} bị xóa.")
    for m in modified[:15]:
        print(f"  📝 [MODIFIED] {m}")
    for a in added[:15]:
        print(f"  ➕ [ADDED]    {a}")
    for d in deleted[:15]:
        print(f"  ➖ [DELETED]  {d}")
    if not modified and not added and not deleted:
        print("  ✔ Mã nguồn hiện tại hoàn toàn khớp 100% với bản snapshot!")


def restore_snapshot(target_name: str) -> bool:
    """Khôi phục mã nguồn từ snapshot với tự động sao lưu an toàn pre-restore."""
    # 1. Kiểm tra live directory trước
    target_live = None
    if LIVE_DIR.exists():
        matches = [d for d in LIVE_DIR.iterdir() if d.is_dir() and target_name in d.name]
        if matches:
            target_live = matches[0]

    # 2. Kiểm tra tar archive
    target_tar = None
    if ARCHIVE_DIR.exists():
        matches_tar = list(ARCHIVE_DIR.glob(f"*{target_name}*"))
        if matches_tar:
            target_tar = matches_tar[0]

    if not target_live and not target_tar:
        print(f"❌ Không tìm thấy bản snapshot nào khớp với từ khóa: '{target_name}'")
        return False

    print("🛡️ [Safety Precaution] Đang tự động lưu snapshot dự phòng 'pre_restore_backup'...")
    create_snapshot("pre_restore_backup", as_dir=False)

    if target_live:
        print(f"🔄 Đang khôi phục mã nguồn từ Live Snapshot: '{target_live.name}'...")
        try:
            for item in INCLUDE_DIRS:
                src_item = target_live / item
                dst_item = ROOT_DIR / item
                if src_item.exists():
                    if dst_item.exists():
                        shutil.rmtree(dst_item, ignore_errors=True)
                    shutil.copytree(src_item, dst_item, dirs_exist_ok=True)
            print(f"✅ [ROLLBACK COMPLETED] Khôi phục thành công từ Live Snapshot: {target_live.name}!")
            return True
        except Exception as e:
            print(f"❌ Lỗi khi khôi phục snapshot: {e}")
            return False
    else:
        print(f"🔄 Đang khôi phục mã nguồn từ Archive: '{target_tar.name}'...")
        try:
            with tarfile.open(target_tar, "r:gz") as tar:
                tar.extractall(path=ROOT_DIR)
            print(f"✅ [ROLLBACK COMPLETED] Khôi phục thành công từ Archive: {target_tar.name}!")
            return True
        except Exception as e:
            print(f"❌ Lỗi khi khôi phục archive: {e}")
            return False


def clean_snapshots(keep_latest: int = 3, clean_all: bool = False) -> None:
    """Xóa các bản snapshot cũ."""
    # Clean archives
    if ARCHIVE_DIR.exists():
        archives = sorted(ARCHIVE_DIR.glob("*.tar.gz"), key=lambda f: f.stat().st_mtime, reverse=True)
        to_del = archives if clean_all else archives[keep_latest:]
        for a in to_del:
            print(f"🗑️ Đang xóa archive snapshot cũ: {a.name}")
            a.unlink(missing_ok=True)

    # Clean live directories
    if LIVE_DIR.exists():
        live_dirs = sorted([d for d in LIVE_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")],
                           key=lambda d: d.stat().st_mtime, reverse=True)
        to_del_dir = live_dirs if clean_all else live_dirs[keep_latest:]
        for d in to_del_dir:
            print(f"🗑️ Đang xóa live snapshot cũ: {d.name}")
            shutil.rmtree(d, ignore_errors=True)

    print("✅ Đã hoàn tất dọn dẹp snapshots!")


def main():
    parser = argparse.ArgumentParser(description="Chụp ảnh nhanh & khôi phục an toàn (Snapshot & Rollback).")
    subparsers = parser.add_subparsers(dest="command")

    # take
    take_parser = subparsers.add_parser("take", help="Tạo snapshot mới")
    take_parser.add_argument("name", nargs="?", default="manual", help="Tag tên snapshot")
    take_parser.add_argument("--dir", action="store_true", help="Lưu dạng thư mục sống uncompressed (.snapshots/)")

    # list
    subparsers.add_parser("list", help="Liệt kê danh sách snapshot")

    # diff
    diff_parser = subparsers.add_parser("diff", help="So sánh thay đổi với live snapshot")
    diff_parser.add_argument("name", help="Tên hoặc từ khóa snapshot cần diff")

    # restore
    restore_parser = subparsers.add_parser("restore", help="Khôi phục snapshot")
    restore_parser.add_argument("name", help="Tên hoặc từ khóa snapshot cần khôi phục")

    # clean
    clean_parser = subparsers.add_parser("clean", help="Dọn dẹp snapshot cũ")
    clean_parser.add_argument("--keep", type=int, default=3, help="Số bản snapshot mới nhất giữ lại")
    clean_parser.add_argument("--all", action="store_true", help="Xóa sạch toàn bộ snapshots")

    # Cú pháp ngắn: python scripts/snapshot.py [tag]
    if len(sys.argv) > 1 and sys.argv[1] not in ["take", "list", "diff", "restore", "clean", "-h", "--help"]:
        create_snapshot(sys.argv[1], as_dir=False)
        return

    args = parser.parse_args()
    if args.command == "take":
        create_snapshot(args.name, as_dir=args.dir)
    elif args.command == "list":
        list_snapshots()
    elif args.command == "diff":
        diff_snapshot(args.name)
    elif args.command == "restore":
        restore_snapshot(args.name)
    elif args.command == "clean":
        clean_snapshots(keep_latest=args.keep, clean_all=args.all)
    else:
        create_snapshot("manual", as_dir=False)


if __name__ == "__main__":
    main()
