#!/usr/bin/env python3
"""
verify_network.py
Kiểm tra tình trạng các cổng mạng (Port Readiness & Conflict Checker).
Giúp phát hiện sớm xung đột cổng mạng (8000, 3000, 5432) trước khi khởi chạy hệ thống.
"""

import socket
import sys

PORTS_TO_CHECK = {
    8000: "FastAPI Backend API",
    3000: "Next.js Web Portal",
    5432: "PostgreSQL Database",
    8081: "Expo Metro Bundler (Mobile)",
}

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0

def main():
    print("🌐 [NETWORK VERIFICATION] Đang rà soát trạng thái các cổng mạng...")
    occupied = []
    available = []

    for port, service in PORTS_TO_CHECK.items():
        if is_port_in_use(port):
            occupied.append((port, service))
            print(f"   ⚠️ Cổng {port} ({service}) hiện ĐANG ĐƯỢC SỬ DỤNG.")
        else:
            available.append((port, service))
            print(f"   ✅ Cổng {port} ({service}) ĐANG SẴN SÀNG.")

    if occupied:
        print("\nℹ️ [THÔNG BÁO] Một số cổng đang hoạt động. Nếu đây là các container Docker của dự án, bạn có thể bỏ qua.")
    else:
        print("\n🎉 [ALL CLEAR] Toàn bộ cổng mạng đều sẵn sàng cho khởi động mới!")

    sys.exit(0)

if __name__ == "__main__":
    main()
