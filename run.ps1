# PowerShell Runner cho Windows Developers (run.ps1)
# Cung cấp bộ lệnh tương đương Makefile cho môi trường Windows với tự động nhận diện .venv

param (
    [Parameter(Position = 0)]
    [string]$Command = "help",

    [Parameter(Position = 1)]
    [string]$Arg1 = "",

    [Parameter(Position = 2)]
    [string]$Arg2 = ""
)

# Tự động nhận diện Python trong .venv nếu có, ngược lại dùng Python hệ thống
$PythonBin = if (Test-Path ".\.venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }

function Show-Help {
    Write-Host "========================================================================" -ForegroundColor Cyan
    Write-Host "          AI-Vibe-Coding — Bộ Tự Động Hóa Cho Windows (PowerShell)       " -ForegroundColor Cyan
    Write-Host "========================================================================" -ForegroundColor Cyan
    Write-Host "  --- THỰC THI & KIỂM THỬ ---"
    Write-Host "  .\run.ps1 setup           : Khởi tạo virtualenv .venv và cài đặt dependencies"
    Write-Host "  .\run.ps1 dev             : Khởi chạy Backend FastAPI (Uvicorn reload)"
    Write-Host "  .\run.ps1 test            : Chạy kiểm thử Pytest trên SQLite in-memory"
    Write-Host "  .\run.ps1 smoke           : Chạy bộ kiểm thử tự động 5 tầng (smoke_test.py)"
    Write-Host "  .\run.ps1 contracts       : Kiểm tra đồng bộ hợp đồng dữ liệu"
    Write-Host "  .\run.ps1 migrations      : Kiểm tra toàn vẹn đồ thị Alembic Migrations"
    Write-Host "  .\run.ps1 seed            : Khởi tạo dữ liệu mẫu ban đầu"
    Write-Host "  .\run.ps1 release         : Đóng gói bản phát hành (.zip, manifest)"
    Write-Host "  .\run.ps1 docker-up       : Khởi động Backend + DB qua Docker Compose"
    Write-Host "  .\run.ps1 docker-fullstack: Khởi động Fullstack (DB + Backend + Frontend)"
    Write-Host "  .\run.ps1 docker-down     : Dừng toàn bộ Docker containers"
    Write-Host "  .\run.ps1 clean           : Xóa sạch bytecode, cache và files tạm thời"
    Write-Host ""
    Write-Host "  --- TÁC TỬ & SUBAGENTS ANTIGRAVITY 2.0 ---"
    Write-Host "  .\run.ps1 agents-check    : Xác thực 20 Subagents & Squad specs"
    Write-Host "  .\run.ps1 agents-list     : Liệt kê danh sách và vai trò của 5 Sub-Teams"
    Write-Host ""
    Write-Host "  --- TINH HOA 1: PRESETS & CLIENT ARCHITECTURE ---"
    Write-Host "  .\run.ps1 frontend-status : Kiểm tra trạng thái hiện tại của Web & Mobile Client"
    Write-Host "  .\run.ps1 preset-vite     : Chuyển đổi Web Client sang React + Vite (SPA / Fast)"
    Write-Host "  .\run.ps1 preset-nextjs   : Chuyển đổi Web Client sang Next.js 15 (SSR / SEO)"
    Write-Host "  .\run.ps1 add-mobile      : Khởi tạo App Mobile React Native Expo trong src/mobile/"
    Write-Host ""
    Write-Host "  --- TINH HOA 2: STATE CHECKPOINTS & RESUME / ROLLBACK ---"
    Write-Host "  .\run.ps1 checkpoint <phase> <note> : Lưu Checkpoint mới kèm Snapshot mã nguồn"
    Write-Host "  .\run.ps1 checkpoints     : Liệt kê danh sách toàn bộ các checkpoints đã lưu"
    Write-Host "  .\run.ps1 resume          : Xem vị trí dừng và hướng dẫn tiếp tục phiên làm việc"
    Write-Host "  .\run.ps1 restore <id>    : Khôi phục mã nguồn và trạng thái về checkpoint cụ thể"
    Write-Host "  .\run.ps1 snapshot [tag]  : Chụp ảnh nhanh mã nguồn phòng ngừa rủi ro"
    Write-Host "========================================================================" -ForegroundColor Cyan
}

switch ($Command.ToLower()) {
    "setup" {
        Write-Host "📦 Đang khởi tạo môi trường ảo và cài đặt dependencies..." -ForegroundColor Green
        python -m venv .venv
        .\.venv\Scripts\python.exe -m pip install --upgrade pip
        .\.venv\Scripts\pip.exe install -e ".[dev]"
    }
    "dev" {
        Write-Host "🚀 Đang khởi động Backend FastAPI (Python: $PythonBin)..." -ForegroundColor Green
        & $PythonBin -m uvicorn src.backend.app.main:app --reload --port 8000
    }
    "test" {
        Write-Host "🧪 Đang chạy kiểm thử Pytest Backend (Python: $PythonBin)..." -ForegroundColor Green
        & $PythonBin -m pytest -v src/backend/tests
    }
    "smoke" {
        Write-Host "🔥 Đang chạy bộ kiểm thử tự động 5 tầng (Python: $PythonBin)..." -ForegroundColor Green
        & $PythonBin scripts/smoke_test.py
    }
    "contracts" {
        Write-Host "📐 Đang kiểm tra đồng bộ hợp đồng dữ liệu..." -ForegroundColor Green
        & $PythonBin scripts/verify_contracts.py
    }
    "migrations" {
        Write-Host "🗄️ Đang kiểm tra đồ thị Alembic Migrations..." -ForegroundColor Green
        & $PythonBin scripts/verify_migrations.py
    }
    "seed" {
        Write-Host "🌱 Đang nạp dữ liệu mẫu..." -ForegroundColor Green
        & $PythonBin src/db/seeds/runner.py
    }
    "snapshot" {
        $tag = if ($Arg1) { $Arg1 } else { "manual" }
        Write-Host "📦 Đang tạo bản sao chụp mã nguồn..." -ForegroundColor Green
        & $PythonBin scripts/snapshot.py $tag
    }
    "release" {
        Write-Host "🎁 Đang đóng gói bản phát hành..." -ForegroundColor Green
        & $PythonBin scripts/bundle_release.py core-release 1.0.0
    }
    "docker-up" {
        Write-Host "🐳 Đang khởi động Docker Compose (Core: DB + Backend)..." -ForegroundColor Green
        docker compose up --build -d
    }
    "docker-fullstack" {
        Write-Host "🐳 Đang khởi động Docker Compose Fullstack (DB + Backend + Frontend)..." -ForegroundColor Green
        docker compose --profile fullstack up --build -d
    }
    "docker-down" {
        Write-Host "🛑 Đang dừng toàn bộ Docker containers..." -ForegroundColor Green
        docker compose --profile fullstack down
    }
    "frontend-status" {
        & $PythonBin scripts/setup_frontend.py --status
    }
    "preset-vite" {
        & $PythonBin scripts/setup_frontend.py --preset vite
    }
    "preset-nextjs" {
        & $PythonBin scripts/setup_frontend.py --preset nextjs
    }
    "add-mobile" {
        & $PythonBin scripts/setup_frontend.py --add-mobile
    }
    "checkpoint" {
        $phase = if ($Arg1) { $Arg1 } else { "discovery" }
        $note = if ($Arg2) { $Arg2 } else { "Checkpoint tự động" }
        & $PythonBin scripts/checkpoint.py save --phase $phase --note $note
    }
    "checkpoints" {
        & $PythonBin scripts/checkpoint.py list
    }
    "resume" {
        & $PythonBin scripts/checkpoint.py resume
    }
    "restore" {
        if (-not $Arg1) {
            Write-Host "❌ Vui lòng cung cấp mã checkpoint: .\run.ps1 restore <checkpoint_id>" -ForegroundColor Red
        } else {
            & $PythonBin scripts/checkpoint.py restore $Arg1
        }
    }
    "agents-check" {
        & $PythonBin scripts/register_agents.py --validate
    }
    "agents-list" {
        & $PythonBin scripts/register_agents.py --list
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
