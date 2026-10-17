# PowerShell Runner cho Windows Developers (run.ps1)
# Cung cấp bộ lệnh tương đương Makefile cho môi trường Windows

param (
    [Parameter(Position = 0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "========================================================================" -ForegroundColor Cyan
    Write-Host "          AI-Vibe-Coding — Bộ Tự Động Hóa Cho Windows (PowerShell)       " -ForegroundColor Cyan
    Write-Host "========================================================================" -ForegroundColor Cyan
    Write-Host "  .\run.ps1 dev          : Khởi chạy Backend FastAPI (Uvicorn reload)"
    Write-Host "  .\run.ps1 test         : Chạy kiểm thử Pytest trên SQLite in-memory"
    Write-Host "  .\run.ps1 smoke        : Chạy bộ kiểm thử tự động 5 tầng (smoke_test.py)"
    Write-Host "  .\run.ps1 contracts    : Kiểm tra đồng bộ hợp đồng dữ liệu"
    Write-Host "  .\run.ps1 migrations   : Kiểm tra toàn vẹn đồ thị Alembic Migrations"
    Write-Host "  .\run.ps1 seed         : Khởi tạo dữ liệu mẫu ban đầu"
    Write-Host "  .\run.ps1 snapshot     : Chụp ảnh nhanh mã nguồn phòng ngừa rủi ro"
    Write-Host "  .\run.ps1 release      : Đóng gói bản phát hành (.zip, manifest)"
    Write-Host "  .\run.ps1 clean        : Xóa sạch bytecode, cache và files tạm thời"
    Write-Host "========================================================================" -ForegroundColor Cyan
}

switch ($Command.ToLower()) {
    "dev" {
        Write-Host "🚀 Đang khởi động Backend FastAPI..." -ForegroundColor Green
        python -m uvicorn src.backend.app.main:app --reload --port 8000
    }
    "test" {
        Write-Host "🧪 Đang chạy kiểm thử Pytest Backend..." -ForegroundColor Green
        python -m pytest -v src/backend/tests
    }
    "smoke" {
        Write-Host "🔥 Đang chạy bộ kiểm thử tự động 5 tầng..." -ForegroundColor Green
        python scripts/smoke_test.py
    }
    "contracts" {
        Write-Host "📐 Đang kiểm tra đồng bộ hợp đồng dữ liệu..." -ForegroundColor Green
        python scripts/verify_contracts.py
    }
    "migrations" {
        Write-Host "🗄️ Đang kiểm tra đồ thị Alembic Migrations..." -ForegroundColor Green
        python scripts/verify_migrations.py
    }
    "seed" {
        Write-Host "🌱 Đang nạp dữ liệu mẫu..." -ForegroundColor Green
        python src/db/seeds/runner.py
    }
    "snapshot" {
        Write-Host "📦 Đang tạo bản sao chụp mã nguồn..." -ForegroundColor Green
        python scripts/snapshot.py manual
    }
    "release" {
        Write-Host "🎁 Đang đóng gói bản phát hành..." -ForegroundColor Green
        python scripts/bundle_release.py core-release 1.0.0
    }
    "clean" {
        Write-Host "🧹 Đang dọn dẹp các tệp tạm..." -ForegroundColor Yellow
        Get-ChildItem -Path . -Include __pycache__, .pytest_cache, .ruff_cache -Recurse -Directory -Force | Remove-Item -Recurse -Force
        Get-ChildItem -Path . -Include *.pyc -Recurse -File -Force | Remove-Item -Force
        Write-Host "✅ Dọn dẹp hoàn tất!" -ForegroundColor Green
    }
    default {
        Show-Help
    }
}
