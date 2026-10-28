#!/usr/bin/env python3
"""clean_skeleton.py — Reset Codebase to Day-0 Clean Skeleton.

Part of AI-Vibe-Coding (Antigravity 2.0).

Allows developers to reset the `src/` directory from the demo application state
(User entity, UserCard component, migrations, mock fixtures) to a pristine,
unopinionated Clean Architecture skeleton, ready for new client briefs (Day-0).

Automatic Safety:
- Takes a snapshot before resetting so you can restore anytime via `--restore`.

Usage:
    python scripts/clean_skeleton.py --status
    python scripts/clean_skeleton.py --reset
    python scripts/clean_skeleton.py --restore
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# Ensure UTF-8 console output on Windows
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"

DEMO_FILES = [
    SRC_DIR / "db" / "models" / "user.py",
    SRC_DIR / "db" / "repositories" / "user_repository.py",
    SRC_DIR / "db" / "migrations" / "versions" / "0001_initial_schema.py",
    SRC_DIR / "backend" / "app" / "schemas" / "user.py",
    SRC_DIR / "backend" / "app" / "services" / "user_service.py",
    SRC_DIR / "backend" / "app" / "api" / "v1" / "users.py",
    SRC_DIR / "backend" / "tests" / "test_users.py",
    SRC_DIR / "frontend" / "src" / "types" / "user.ts",
    SRC_DIR / "frontend" / "src" / "components" / "UserCard.tsx",
    SRC_DIR / "frontend" / "src" / "lib" / "api" / "mocks" / "user_mock.ts",
]


def check_status() -> bool:
    """Kiểm tra trạng thái codebase: True nếu đang ở Demo mode, False nếu là Clean Skeleton."""
    existing_demos = [f for f in DEMO_FILES if f.exists()]
    print("=" * 68)
    print("🧹 AI-Vibe-Coding — Trạng Thái Bộ Khung Mã Nguồn (Codebase Skeleton)")
    print("=" * 68)
    if existing_demos:
        print(f"📌 Trạng thái hiện tại: [DEMO MODE] ({len(existing_demos)}/{len(DEMO_FILES)} tệp demo có mặt)")
        print("   Các thành phần mẫu: User Model, User Repository, UserCard UI, User Schemas, Mock Fixtures.")
        print("   👉 Để đưa về trạng thái sạch Day-0 cho dự án mới: python scripts/clean_skeleton.py --reset")
        print("=" * 68)
        return True
    else:
        print("📌 Trạng thái hiện tại: [CLEAN SKELETON MODE] (Day-0 Pristine)")
        print("   Thư mục src/ hoàn toàn sạch sẽ, sẵn sàng tiếp nhận đề bài mới từ Client Brief.")
        print("   👉 Để khôi phục lại code mẫu demo: python scripts/clean_skeleton.py --restore")
        print("=" * 68)
        return False


def reset_to_clean_skeleton() -> bool:
    """Tạo snapshot an toàn rồi đưa src/ về trạng thái Clean Skeleton."""
    print("📸 [1/3] Đang tự động tạo bản chụp an toàn trước khi dọn dẹp (Snapshot)...")
    try:
        subprocess.run(
            [sys.executable, str(ROOT_DIR / "scripts" / "snapshot.py"), "take", "before_clean_skeleton"],
            cwd=str(ROOT_DIR),
            check=False,
        )
    except Exception as e:
        print(f"⚠️ Cảnh báo tạo snapshot: {e}")

    print("🧹 [2/3] Đang loại bỏ các tệp mẫu demo (User entity, mock fixtures, demo migrations)...")
    removed_count = 0
    for f in DEMO_FILES:
        if f.exists():
            try:
                f.unlink()
                removed_count += 1
            except Exception as e:
                print(f"  ❌ Không thể xóa {f.name}: {e}")

    # Đảm bảo thư mục versions có .gitkeep
    versions_dir = SRC_DIR / "db" / "migrations" / "versions"
    versions_dir.mkdir(parents=True, exist_ok=True)
    gitkeep = versions_dir / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("# Directory for Alembic migrations\n", encoding="utf-8")

    # 3. Cập nhật các file đầu mối về dạng Clean Skeleton
    print("✨ [3/3] Đang cập nhật router và schemas về trạng thái khởi đầu sạch...")

    # DB models __init__.py
    (SRC_DIR / "db" / "models" / "__init__.py").write_text(
        '"""SQLAlchemy 2.0 Declarative Models Package (`src.db.models`)."""\n',
        encoding="utf-8",
    )

    # DB repositories __init__.py
    (SRC_DIR / "db" / "repositories" / "__init__.py").write_text(
        '"""Async Database Repositories Package (`src.db.repositories`)."""\n',
        encoding="utf-8",
    )

    # Backend schemas __init__.py
    (SRC_DIR / "backend" / "app" / "schemas" / "__init__.py").write_text(
        '"""Pydantic v2 validation schemas package (`src.backend.app.schemas`)."""\n',
        encoding="utf-8",
    )

    # Backend services __init__.py
    (SRC_DIR / "backend" / "app" / "services" / "__init__.py").write_text(
        '"""Business logic services package (`src.backend.app.services`)."""\n',
        encoding="utf-8",
    )

    # Backend router.py
    clean_router = '''"""API v1 Router aggregator (`src.backend.app.api.v1.router`).
Register new feature routers here following the Clean Layered Architecture.
"""

from fastapi import APIRouter
from src.backend.app.api.v1 import health

api_router = APIRouter()

# Core system health check
api_router.include_router(health.router, tags=["system"])

# Register your feature endpoints here:
# from src.backend.app.api.v1.endpoints import items
# api_router.include_router(items.router, prefix="/items", tags=["items"])
'''
    (SRC_DIR / "backend" / "app" / "api" / "v1" / "router.py").write_text(clean_router, encoding="utf-8")

    # Frontend types/index.ts
    clean_types = '''// Universal TypeScript Definitions for AI-Vibe-Coding (Day-0 Clean Skeleton)
export interface BaseEntity {
  id: string;
  created_at: string;
  updated_at: string;
}

export interface ApiErrorResponse {
  detail: string;
  code?: string;
  status_code?: number;
}
'''
    (SRC_DIR / "frontend" / "src" / "types" / "index.ts").write_text(clean_types, encoding="utf-8")

    # Frontend page.tsx
    clean_page = '''import React from "react";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 text-center bg-slate-50">
      <div className="max-w-2xl rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="inline-flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700 mb-4">
          <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
          Day-0 Clean Skeleton Ready
        </div>
        <h1 className="text-3xl font-bold tracking-tight text-slate-900 mb-2">
          AI-Vibe-Coding Workspace
        </h1>
        <p className="text-slate-600 mb-6">
          Mã nguồn đã được dọn sạch về trạng thái Clean Architecture Day-0.
          Hãy gửi đề bài mới (Client Brief) vào Chat Canvas để bắt đầu triển khai sản phẩm!
        </p>
      </div>
    </main>
  );
}
'''
    (SRC_DIR / "frontend" / "src" / "app" / "page.tsx").write_text(clean_page, encoding="utf-8")

    print(f"✔ Đã loại bỏ {removed_count} tệp demo.")
    print("✔ Mã nguồn src/ đã được đưa về trạng thái Clean Skeleton Day-0 hoàn toàn sạch sẽ!")
    print("👉 Bạn có thể khôi phục lại code demo bất kỳ lúc nào qua lệnh:")
    print("   python scripts/clean_skeleton.py --restore")
    return True


def restore_demo() -> bool:
    """Khôi phục lại phiên bản trước khi dọn dẹp từ snapshot."""
    print("🔄 Đang khôi phục lại mã nguồn từ snapshot 'before_clean_skeleton'...")
    try:
        res = subprocess.run(
            [sys.executable, str(ROOT_DIR / "scripts" / "snapshot.py"), "restore", "before_clean_skeleton"],
            cwd=str(ROOT_DIR),
            check=False,
            capture_output=True,
            text=True,
        )
        print(res.stdout)
        if res.returncode == 0:
            print("✔ Khôi phục hoàn tất!")
            return True
        else:
            print(f"❌ Lỗi khôi phục: {res.stderr}")
            return False
    except Exception as e:
        print(f"❌ Lỗi khi khôi phục snapshot: {e}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Clean Skeleton Reset cho AI-Vibe-Coding")
    parser.add_argument("--status", action="store_true", help="Kiểm tra trạng thái skeleton hiện tại")
    parser.add_argument("--reset", action="store_true", help="Dọn sạch demo, đưa src/ về trạng thái Day-0 Clean Skeleton")
    parser.add_argument("--restore", action="store_true", help="Khôi phục lại demo từ snapshot trước đó")
    args = parser.parse_args()

    if args.reset:
        return 0 if reset_to_clean_skeleton() else 1
    elif args.restore:
        return 0 if restore_demo() else 1
    else:
        check_status()
        return 0


if __name__ == "__main__":
    sys.exit(main())
