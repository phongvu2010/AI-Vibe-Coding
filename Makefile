.PHONY: help dev test smoke contracts migrations snapshot release docker-up docker-down seed clean

help:
	@echo "========================================================================"
	@echo "          AI-Vibe-Coding — Bộ Tự Động Hóa 1-Chạm cho Tech Lead          "
	@echo "========================================================================"
	@echo "  make dev          : Khởi chạy Backend FastAPI (Uvicorn reload)"
	@echo "  make test         : Chạy kiểm thử Pytest trên SQLite in-memory cô lập"
	@echo "  make smoke        : Chạy bộ kiểm thử tự động 5 tầng (smoke_test.py)"
	@echo "  make contracts    : Kiểm tra đồng bộ hợp đồng dữ liệu (verify_contracts.py)"
	@echo "  make migrations   : Kiểm tra toàn vẹn đồ thị Alembic (verify_migrations.py)"
	@echo "  make seed         : Khởi tạo dữ liệu mẫu ban đầu vào database"
	@echo "  make snapshot     : Chụp ảnh nhanh mã nguồn phòng ngừa rủi ro"
	@echo "  make release      : Đóng gói bản phát hành (.zip, manifest, docs)"
	@echo "  make docker-up    : Khởi động toàn bộ dịch vụ qua Docker Compose"
	@echo "  make docker-down  : Dừng toàn bộ Docker containers"
	@echo "  make clean        : Xóa sạch bytecode, cache và files tạm thời"
	@echo "========================================================================"

dev:
	@echo "🚀 Đang khởi động Backend FastAPI..."
	python3 -m uvicorn src.backend.app.main:app --reload --port 8000

test:
	@echo "🧪 Đang chạy kiểm thử Pytest Backend & DB..."
	python3 -m pytest -v src/backend/tests

smoke:
	@echo "🔥 Đang chạy bộ kiểm thử tự động 5 tầng..."
	python3 scripts/smoke_test.py

contracts:
	@echo "📐 Đang kiểm tra đồng bộ hợp đồng dữ liệu..."
	python3 scripts/verify_contracts.py

migrations:
	@echo "🗄️ Đang kiểm tra đồ thị Alembic Migrations..."
	python3 scripts/verify_migrations.py

seed:
	@echo "🌱 Đang nạp dữ liệu mẫu..."
	python3 src/db/seeds/runner.py

snapshot:
	@echo "📦 Đang tạo bản sao chụp mã nguồn..."
	python3 scripts/snapshot.py manual

release:
	@echo "🎁 Đang đóng gói bản phát hành..."
	python3 scripts/bundle_release.py core-release 1.0.0

docker-up:
	@echo "🐳 Đang khởi động Docker Compose..."
	docker compose up --build -d

docker-down:
	@echo "🛑 Đang dừng Docker Compose..."
	docker compose down

clean:
	@echo "🧹 Đang dọn dẹp các tệp tạm..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
