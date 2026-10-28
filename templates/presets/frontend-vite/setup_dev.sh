#!/usr/bin/env bash
# ==============================================================================
# setup_dev.sh — Tự động khởi tạo & khởi chạy Frontend Client (Next.js / Vite / Expo)
# Tích hợp cho AI-Vibe-Coding (Antigravity 2.0)
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================================================="
echo "          🚀 KHỞI TẠO & CHẠY FRONTEND DEV SERVER (AI-VIBE-CODING)         "
echo "=========================================================================="

if ! command -v node &> /dev/null; then
    echo "❌ Lỗi: Node.js chưa được cài đặt. Vui lòng cài đặt Node.js v18+ (khuyên dùng Node.js v20 LTS)."
    exit 1
fi

NODE_VERSION=$(node -v)
echo "✔ Node.js runtime: $NODE_VERSION"

# Kiểm tra & cài đặt dependencies nếu chưa có node_modules
if [ ! -d "node_modules" ]; then
    echo "📦 Đang cài đặt thư viện qua npm install..."
    npm install
    echo "✔ Cài đặt dependencies hoàn tất!"
else
    echo "✔ Thư mục node_modules đã tồn tại. Bỏ qua bước cài đặt."
fi

# Nhận diện stack: React Native Expo vs Next.js vs Vite
if [ -f "app.json" ] || [ -f "metro.config.js" ]; then
    echo "📱 Phát hiện kiến trúc: React Native + Expo (Mobile Client)"
    echo "▶ Khởi chạy Expo development server..."
    npx expo start
elif [ -f "next.config.mjs" ] || [ -f "next.config.js" ]; then
    echo "🌐 Phát hiện kiến trúc: Next.js 15 (Web SSR Client)"
    echo "▶ Khởi chạy Next.js dev server tại http://localhost:3000..."
    npm run dev
elif [ -f "vite.config.ts" ] || [ -f "vite.config.js" ]; then
    echo "⚡ Phát hiện kiến trúc: React + Vite (Web SPA Client)"
    echo "▶ Khởi chạy Vite dev server tại http://localhost:3000..."
    npm run dev
else
    echo "▶ Khởi chạy frontend dev server mặc định..."
    npm run dev
fi
