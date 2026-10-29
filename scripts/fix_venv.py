#!/usr/bin/env python3
"""
fix_venv.py — Đồng Bộ & Sửa Lỗi Lệch Đường Dẫn Môi Trường Ảo (.venv Path Relocator)
Thuộc hệ thống AI-Vibe-Coding (Antigravity 2.0).

Công dụng:
Khi repository được clone sang máy mới hoặc đổi tên/di chuyển thư mục (ví dụ từ
'AI Team Dev' sang 'Team-Dev/AI-Vibe-Coding'), các script nhị phân (pytest, alembic,
ruff, uvicorn...) và file activate trong .venv thường bị dính đường dẫn cứng cũ
gây lỗi: "cannot execute: No such file or directory".

Script này tự động:
1. Xác định đường dẫn tuyệt đối của .venv hiện tại.
2. Quét và cập nhật shebang của mọi script thực thi trong .venv/bin (hoặc .venv/Scripts).
3. Cập nhật biến VIRTUAL_ENV trong các file activate, activate.csh, activate.fish.
4. Cập nhật pyvenv.cfg trỏ về đúng thư mục mới.
"""

import os
import platform
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
VENV_DIR = ROOT_DIR / ".venv"


def fix_virtualenv():
    if not VENV_DIR.exists():
        print(f"❌ [LỖI] Không tìm thấy thư mục môi trường ảo tại: {VENV_DIR}")
        print("   Hãy khởi tạo môi trường trước: python3 -m venv .venv")
        sys.exit(1)

    is_windows = platform.system() == "Windows"
    bin_dir = VENV_DIR / ("Scripts" if is_windows else "bin")
    if not bin_dir.exists():
        print(f"❌ [LỖI] Không tìm thấy thư mục binaries tại: {bin_dir}")
        sys.exit(1)

    current_venv_str = str(VENV_DIR)
    current_python = str(bin_dir / ("python.exe" if is_windows else "python"))
    current_python3 = str(bin_dir / ("python3.exe" if is_windows else "python3"))

    print("========================================================================")
    print("🔧 [FIX VENV] Đang đồng bộ hóa đường dẫn môi trường ảo...")
    print(f"   Thư mục gốc: {ROOT_DIR}")
    print(f"   Venv mục tiêu: {VENV_DIR}")
    print(f"   Python interpreter: {current_python}")
    print("========================================================================")

    # 1. Cập nhật pyvenv.cfg
    cfg_file = VENV_DIR / "pyvenv.cfg"
    if cfg_file.exists():
        try:
            content = cfg_file.read_text(encoding="utf-8")
            # Thay thế đường dẫn sau "-m venv"
            new_content = re.sub(
                r'(-m\s+venv\s+).*',
                rf'\1{current_venv_str}',
                content
            )
            if new_content != content:
                cfg_file.write_text(new_content, encoding="utf-8")
                print("   ✅ Đã cập nhật pyvenv.cfg")
        except Exception as e:
            print(f"   ⚠️ Lỗi khi cập nhật pyvenv.cfg: {e}")

    # 2. Cập nhật các file activate
    activate_files = [
        ("activate", r'VIRTUAL_ENV=.*', f'VIRTUAL_ENV="{current_venv_str}"'),
        ("activate.csh", r'setenv VIRTUAL_ENV\s+.*', f'setenv VIRTUAL_ENV "{current_venv_str}"'),
        ("activate.fish", r'set -gx VIRTUAL_ENV\s+.*', f'set -gx VIRTUAL_ENV "{current_venv_str}"'),
    ]

    for fname, pattern, replacement in activate_files:
        act_path = bin_dir / fname
        if act_path.exists():
            try:
                content = act_path.read_text(encoding="utf-8", errors="ignore")
                new_content = re.sub(pattern, replacement, content)
                if new_content != content:
                    act_path.write_text(new_content, encoding="utf-8")
                    print(f"   ✅ Đã cập nhật {fname}")
            except Exception as e:
                print(f"   ⚠️ Lỗi khi cập nhật {fname}: {e}")

    # 3. Quét và sửa shebang của các executable scripts trong bin/ (hoặc Scripts/)
    fixed_count = 0
    shebang_patterns = [
        # Dạng shell wrapper: '''exec' ".../.venv/bin/python..." "$0" "$@"
        (re.compile(r"('''exec'\s+\")[^\"]+/\.venv/bin/python[0-9.]*(\"\s+\"\$0\")"), rf"\1{current_python}\2"),
        # Dạng thông thường: #!.../.venv/bin/python...
        (re.compile(r"^#!\s*.*?/\.venv/bin/python[0-9.]*", re.MULTILINE), f"#!{current_python}"),
        # Dạng Windows Scripts
        (re.compile(r"^#!\s*.*?/\.venv/Scripts/python[0-9.]*", re.MULTILINE), f"#!{current_python}"),
    ]

    for item in bin_dir.iterdir():
        if not item.is_file():
            continue
        # Bỏ qua các file nhị phân compiled (.exe, .dylib, .so, symlinks trỏ tới python)
        if item.suffix.lower() in [".exe", ".dll", ".dylib", ".so"]:
            continue
        if item.name in ["python", "python3", "python3.12", "python.exe"]:
            continue

        try:
            raw_bytes = item.read_bytes()
            # Kiểm tra xem có phải file text không
            if b"\x00" in raw_bytes[:1024]:
                continue
            content = raw_bytes.decode("utf-8", errors="ignore")
        except Exception:
            continue

        modified = False
        new_content = content

        # Tìm các chuỗi trỏ tới virtualenv cũ
        for pattern, repl in shebang_patterns:
            if pattern.search(new_content):
                new_content = pattern.sub(repl, new_content)
                modified = True

        if modified:
            try:
                item.write_text(new_content, encoding="utf-8")
                # Giữ nguyên quyền thực thi
                if not is_windows:
                    os.chmod(item, 0o755)
                fixed_count += 1
            except Exception as e:
                print(f"   ⚠️ Không thể ghi file {item.name}: {e}")

    print(f"   ✅ Đã sửa shebang cho {fixed_count} tệp thực thi trong {bin_dir.name}/")

    # 4. Kiểm tra xác thực
    print("========================================================================")
    print("🔍 Kiểm tra hoạt động của pytest sau khi sửa...")
    import subprocess
    try:
        res = subprocess.run(
            [str(bin_dir / ("pytest.exe" if is_windows else "pytest")), "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if res.returncode == 0:
            print(f"🎉 THÀNH CÔNG: {res.stdout.strip() or res.stderr.strip()}")
            print("   Môi trường ảo đã sẵn sàng 100%!")
        else:
            print(f"⚠️ Pytest thoát với mã {res.returncode}: {res.stderr}")
    except Exception as e:
        print(f"⚠️ Không thể thực thi pytest trực tiếp: {e}")
    print("========================================================================\n")


if __name__ == "__main__":
    fix_virtualenv()
