.PHONY: help dev test smoke contracts migrations snapshot release docker-up docker-fullstack docker-down seed clean \
        frontend-status preset-vite preset-nextjs add-mobile checkpoint checkpoints resume restore \
        agents-check agents-list

# --- Tự động nhận diện Python & Môi trường ảo (.venv) đa nền tảng (macOS / Linux / Windows) ---
ifeq ($(OS),Windows_NT)
    # Môi trường Windows (PowerShell, Git Bash, MinGW, Cygwin)
    DETECTED_VENV_PYTHON := $(firstword $(wildcard .venv/Scripts/python.exe) $(wildcard .venv/Scripts/python))
    SYSTEM_PYTHON := python
    VENV_PYTHON_BIN := .venv/Scripts/python.exe
    VENV_PIP := .venv/Scripts/pip.exe
else
    # Môi trường POSIX (macOS, Linux, WSL)
    DETECTED_VENV_PYTHON := $(firstword $(wildcard .venv/bin/python3) $(wildcard .venv/bin/python))
    SYSTEM_PYTHON := python3
    VENV_PYTHON_BIN := .venv/bin/python
    VENV_PIP := .venv/bin/pip
endif

# Nếu tìm thấy môi trường ảo .venv, ưu tiên dùng Python trong .venv, ngược lại dùng Python hệ thống
ifeq ($(DETECTED_VENV_PYTHON),)
    PYTHON ?= $(SYSTEM_PYTHON)
else
    PYTHON ?= $(DETECTED_VENV_PYTHON)
endif

PHASE ?= discovery
STATUS ?= APPROVED
NOTE ?= Checkpoint tự động
ID ?= latest

help:
	@echo "========================================================================"
	@echo "          AI-Vibe-Coding — Bộ Tự Động Hóa 1-Chạm cho Tech Lead          "
	@echo "========================================================================"
	@echo "  --- THỰC THI & KIỂM THỬ ---"
	@echo "  make setup           : Khởi tạo virtualenv .venv và cài đặt dependencies đầy đủ"
	@echo "  make dev             : Khởi chạy Backend FastAPI (Uvicorn reload)"
	@echo "  make test            : Chạy kiểm thử Pytest trên SQLite in-memory cô lập"
	@echo "  make smoke           : Chạy bộ kiểm thử tự động 5 tầng (smoke_test.py)"
	@echo "  make contracts       : Kiểm tra đồng bộ hợp đồng dữ liệu (verify_contracts.py)"
	@echo "  make migrations      : Kiểm tra toàn vẹn đồ thị Alembic (verify_migrations.py)"
	@echo "  make seed            : Khởi tạo dữ liệu mẫu ban đầu vào database"
	@echo "  make release         : Đóng gói bản phát hành (.zip, manifest, docs)"
	@echo "  make docker-up       : Khởi động Backend + DB qua Docker Compose"
	@echo "  make docker-fullstack: Khởi động Fullstack (DB + Backend + Frontend)"
	@echo "  make docker-down     : Dừng toàn bộ Docker containers"
	@echo "  make clean           : Xóa sạch bytecode, cache và files tạm thời"
	@echo ""
	@echo "  --- TÁC TỬ & SUBAGENTS ANTIGRAVITY 2.0 ---"
	@echo "  make agents-check    : Xác thực 20 Subagents & Squad specs trong .agents/agents/"
	@echo "  make agents-list     : Liệt kê danh sách và vai trò của 5 Sub-Teams"
	@echo ""
	@echo "  --- TINH HOA 1: PRESETS & CLIENT ARCHITECTURE ---"
	@echo "  make frontend-status : Kiểm tra trạng thái hiện tại của Web & Mobile Client"
	@echo "  make preset-vite     : Chuyển đổi Web Client sang React + Vite (SPA / Fast)"
	@echo "  make preset-nextjs   : Chuyển đổi Web Client sang Next.js 15 (SSR / SEO)"
	@echo "  make add-mobile      : Khởi tạo App Mobile React Native Expo trong src/mobile/"
	@echo ""
	@echo "  --- TINH HOA 2: STATE CHECKPOINTS & RESUME / ROLLBACK ---"
	@echo "  make checkpoint      : Lưu Checkpoint kèm Snapshot (PHASE=... STATUS=... NOTE=...)"
	@echo "  make checkpoints     : Liệt kê danh sách toàn bộ các checkpoints đã lưu"
	@echo "  make resume          : Xem vị trí dừng và hướng dẫn tiếp tục phiên làm việc"
	@echo "  make restore ID=...  : Khôi phục mã nguồn và trạng thái về checkpoint cụ thể"
	@echo "  make snapshot        : Chụp nhanh mã nguồn phòng ngừa rủi ro"
	@echo "========================================================================"

setup:
	@echo "📦 Đang khởi tạo môi trường ảo và cài đặt dependencies..."
	$(SYSTEM_PYTHON) -m venv .venv
	$(VENV_PYTHON_BIN) -m pip install --upgrade pip
	$(VENV_PYTHON_BIN) -m pip install -e ".[dev]"

dev:
	@echo "🚀 Đang khởi động Backend FastAPI (Python: $(PYTHON))..."
	$(PYTHON) -m uvicorn src.backend.app.main:app --reload --port 8000

test:
	@echo "🧪 Đang chạy kiểm thử Pytest Backend & DB (Python: $(PYTHON))..."
	$(PYTHON) -m pytest -v src/backend/tests

smoke:
	@echo "🔥 Đang chạy bộ kiểm thử tự động 5 tầng (Python: $(PYTHON))..."
	$(PYTHON) scripts/smoke_test.py

contracts:
	@echo "📐 Đang kiểm tra đồng bộ hợp đồng dữ liệu..."
	$(PYTHON) scripts/verify_contracts.py

migrations:
	@echo "🗄️ Đang kiểm tra đồ thị Alembic Migrations..."
	$(PYTHON) scripts/verify_migrations.py

seed:
	@echo "🌱 Đang nạp dữ liệu mẫu..."
	$(PYTHON) src/db/seeds/runner.py

snapshot:
	@echo "📦 Đang tạo bản sao chụp mã nguồn..."
	$(PYTHON) scripts/snapshot.py manual

release:
	@echo "🎁 Đang đóng gói bản phát hành..."
	$(PYTHON) scripts/bundle_release.py core-release 1.0.0

docker-up:
	@echo "🐳 Đang khởi động Docker Compose (Core: DB + Backend)..."
	docker compose up --build -d

docker-fullstack:
	@echo "🐳 Đang khởi động Docker Compose Fullstack (DB + Backend + Frontend)..."
	docker compose --profile fullstack up --build -d

docker-down:
	@echo "🛑 Đang dừng toàn bộ Docker containers..."
	docker compose --profile fullstack down

clean:
	@echo "🧹 Đang dọn dẹp các tệp tạm..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# --- Presets & Client Scaffolding ---
frontend-status:
	@$(PYTHON) scripts/setup_frontend.py --status

preset-vite:
	@$(PYTHON) scripts/setup_frontend.py --preset vite

preset-nextjs:
	@$(PYTHON) scripts/setup_frontend.py --preset nextjs

add-mobile:
	@$(PYTHON) scripts/setup_frontend.py --add-mobile

# --- State Checkpoints & Session Resume ---
checkpoint:
	@$(PYTHON) scripts/checkpoint.py save --phase $(PHASE) --status $(STATUS) --note "$(NOTE)"

checkpoints:
	@$(PYTHON) scripts/checkpoint.py list

resume:
	@$(PYTHON) scripts/checkpoint.py resume

restore:
	@$(PYTHON) scripts/checkpoint.py restore $(ID)

# --- Subagents Antigravity 2.0 ---
agents-check:
	@$(PYTHON) scripts/register_agents.py --validate

agents-list:
	@$(PYTHON) scripts/register_agents.py --list
