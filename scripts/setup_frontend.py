#!/usr/bin/env python3
"""
setup_frontend.py — Quản lý & Chuyển đổi Kiến trúc Client (Frontend Web & Mobile)
Thuộc hệ thống AI-Vibe-Coding (Antigravity 2.0).

Cho phép lập trình viên / Tech Lead linh hoạt lựa chọn hoặc chuyển đổi:
1. Web Next.js 15 App Router + Tailwind CSS (Mặc định: SSR / SEO / Production)
2. Web React Vite + Tailwind CSS (SPA / Dashboard / Tốc độ khởi động siêu tốc)
3. Mobile React Native + Expo SDK + NativeWind (iOS & Android)

Cách sử dụng:
    python scripts/setup_frontend.py --status
    python scripts/setup_frontend.py --preset vite
    python scripts/setup_frontend.py --preset nextjs
    python scripts/setup_frontend.py --add-mobile
"""

import argparse
import shutil
import sys
from pathlib import Path

# Đảm bảo console UTF-8 trên Windows
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT_DIR / "src" / "frontend"
MOBILE_DIR = ROOT_DIR / "src" / "mobile"
PRESETS_DIR = ROOT_DIR / "templates" / "presets"


def get_current_web_framework() -> str:
    """Xác định framework web hiện tại trong src/frontend/."""
    if not FRONTEND_DIR.exists():
        return "Chưa khởi tạo (Thư mục không tồn tại)"
    pkg_json = FRONTEND_DIR / "package.json"
    if not pkg_json.exists():
        return "Không rõ (Thiếu package.json)"
    try:
        content = pkg_json.read_text(encoding="utf-8")
        if '"next"' in content:
            return "Next.js 15 (App Router + React 19)"
        elif '"vite"' in content:
            return "React + Vite (SPA + Tailwind CSS)"
    except Exception:
        pass
    return "Tùy biến / Khác"


def print_status() -> None:
    print("=" * 68)
    print("📱 AI-Vibe-Coding — Trạng Thái Kiến Trúc Client (Web & Mobile)")
    print("=" * 68)

    web_fw = get_current_web_framework()
    print("\n🌐 Web Client (src/frontend/):")
    print(f"   • Framework: {web_fw}")
    print("   • Styling:   Tailwind CSS")

    print("\n📲 Mobile Client (src/mobile/):")
    if MOBILE_DIR.exists() and (MOBILE_DIR / "package.json").exists():
        print("   • Framework: React Native (Expo SDK 51+ / 52)")
        print("   • Styling:   NativeWind v4 (Tailwind CSS cho Mobile)")
        print("   • Nền tảng:  iOS & Android")
        print("   • Trạng thái: ✅ Đang hoạt động")
    else:
        print("   • Trạng thái: ℹ️ Chưa kích hoạt (chạy: python scripts/setup_frontend.py --add-mobile)")

    print("\n" + "=" * 68)


def apply_preset(preset_name: str) -> bool:
    preset_dir = PRESETS_DIR / f"frontend-{preset_name}"
    if not preset_dir.exists():
        print(f"❌ Lỗi: Không tìm thấy preset '{preset_name}' tại {preset_dir}")
        return False

    print(f"🔄 Đang chuyển đổi src/frontend/ sang preset: {preset_name.upper()}...")

    try:
        if FRONTEND_DIR.exists():
            # Giữ lại node_modules để tránh cài lại nếu dependencies tương thích
            for item in FRONTEND_DIR.iterdir():
                if item.name not in ["node_modules", ".next"]:
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
        else:
            FRONTEND_DIR.mkdir(parents=True, exist_ok=True)

        # Sao chép các tệp từ preset vào src/frontend/
        for item in preset_dir.iterdir():
            dest = FRONTEND_DIR / item.name
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)

        print(f"✅ Đã chuyển đổi Web Client thành công sang: {preset_name.upper()}!")
        print("👉 Bước tiếp theo:")
        print("   1. Cài đặt thư viện: npm --prefix src/frontend install")
        print("   2. Kiểm tra type:     npm --prefix src/frontend run typecheck")
        return True
    except Exception as e:
        print(f"❌ Lỗi khi áp dụng preset: {e}")
        return False


def add_mobile() -> bool:
    preset_dir = PRESETS_DIR / "mobile-react-native"
    if not preset_dir.exists():
        print(f"❌ Lỗi: Không tìm thấy mobile preset tại {preset_dir}")
        return False

    print("🚀 Đang khởi tạo ứng dụng di động React Native tại src/mobile/...")
    try:
        MOBILE_DIR.mkdir(parents=True, exist_ok=True)
        for item in preset_dir.iterdir():
            dest = MOBILE_DIR / item.name
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)

        print("✅ Ứng dụng Mobile React Native (Expo + NativeWind) đã sẵn sàng tại src/mobile/!")
        print("👉 Bước tiếp theo:")
        print("   1. Cài đặt dependencies: npm --prefix src/mobile install")
        print("   2. Khởi chạy app:        npm --prefix src/mobile run start (hoặc npx expo start)")
        return True
    except Exception as e:
        print(f"❌ Lỗi khi thiết lập mobile: {e}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Quản lý cấu hình Frontend & Mobile cho AI-Vibe-Coding")
    parser.add_argument("--status", action="store_true", help="Hiển thị trạng thái cấu hình client hiện tại")
    parser.add_argument("--preset", choices=["nextjs", "vite"], help="Chuyển đổi preset Web frontend (nextjs hoặc vite)")
    parser.add_argument("--add-mobile", action="store_true", help="Khởi tạo ứng dụng di động React Native trong src/mobile/")

    args = parser.parse_args()

    if args.preset:
        success = apply_preset(args.preset)
        print_status()
        return 0 if success else 1

    if args.add_mobile:
        success = add_mobile()
        print_status()
        return 0 if success else 1

    # Mặc định in trạng thái
    print_status()
    return 0


if __name__ == "__main__":
    sys.exit(main())
