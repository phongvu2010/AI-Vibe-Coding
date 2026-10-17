#!/usr/bin/env python3
"""
start_dev.py
Trình khởi động môi trường phát triển thông minh (Smart Dev Runner).
Tự động kiểm tra cổng mạng, hợp đồng dữ liệu trước khi khởi chạy Backend FastAPI.
"""

import subprocess
import sys
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent.parent
    python_bin = sys.executable

    print("🚀 [START DEV] Đang chuẩn bị môi trường phát triển...")

    # 1. Kiểm tra cổng mạng
    print("1️⃣ Kiểm tra cổng mạng...")
    res = subprocess.run([python_bin, str(root / "scripts" / "verify_network.py")])
    if res.returncode != 0:
        print("❌ Lỗi kiểm tra cổng mạng!")
        sys.exit(1)

    # 2. Kiểm tra hợp đồng dữ liệu
    print("2️⃣ Kiểm tra đồng bộ hợp đồng dữ liệu...")
    res = subprocess.run([python_bin, str(root / "scripts" / "verify_contracts.py")])
    if res.returncode != 0:
        print("❌ Hợp đồng dữ liệu không đồng bộ! Vui lòng khắc phục trước khi chạy dev.")
        sys.exit(1)

    # 3. Khởi chạy Uvicorn Backend
    print("3️⃣ Khởi động Uvicorn Backend trên http://localhost:8000...")
    try:
        subprocess.run(
            [
                python_bin,
                "-m",
                "uvicorn",
                "src.backend.app.main:app",
                "--reload",
                "--port",
                "8000",
                "--host",
                "0.0.0.0",
            ],
            cwd=root,
        )
    except KeyboardInterrupt:
        print("\n🛑 Đã dừng Uvicorn Backend an toàn.")


if __name__ == "__main__":
    main()
