<#
.SYNOPSIS
  Developer Automation Toolkit cho Windows PowerShell (AI-Vibe-Coding / Antigravity 2.0).
  Hỗ trợ đầy đủ các lệnh tương đương Makefile trên Windows native (không cần WSL hay Git Bash).

.EXAMPLE
  .\scripts\dev.ps1 help
  .\scripts\dev.ps1 smoke
  .\scripts\dev.ps1 test
  .\scripts\dev.ps1 contracts
  .\scripts\dev.ps1 dev
  .\scripts\dev.ps1 task -Task "Sửa lỗi validation số điện thoại"
  .\scripts\dev.ps1 checkpoint -Phase "gate_1_prd" -Status "APPROVED"
  .\scripts\dev.ps1 preset-vite
#>

[CmdletBinding()]
param (
    [Parameter(Position=0)]
    [ValidateSet("help", "smoke", "test", "test-backend", "test-examples", "test-cov", "cov-html", "contracts", "migrations", "check-db",
                 "test-all", "test-frontend", "test-frontend-unit", "test-frontend-e2e", "test-orchestrator",
                 "run-backend", "run-frontend", "backup", "clean-project", "clean-skeleton",
                 "dev", "dev-backend", "dev-quick", "synthesize", "task", "fast-track", "checkpoint", "checkpoints",
                 "resume", "restore", "sync", "status", "models", "mcp", "subteams", "preset-vite", "preset-nextjs",
                 "add-mobile", "release", "seed", "snapshot", "docker-db", "docker-up", "docker-down", "clean", "install", "venv")]

    [Parameter(ValueFromPipelineByPropertyName=$true)]
    [string]$Task = "",

    [Parameter(ValueFromPipelineByPropertyName=$true)]
    [string]$Phase = "discovery",

    [Parameter(ValueFromPipelineByPropertyName=$true)]
    [string]$Status = "APPROVED",

    [Parameter(ValueFromPipelineByPropertyName=$true)]
    [string]$Note = "Checkpoint tự động",

    [Parameter(ValueFromPipelineByPropertyName=$true)]
    [string]$Id = "latest",

    [Parameter(ValueFromPipelineByPropertyName=$true)]
    [string]$Feature = "motocare-booking",

    [Parameter(ValueFromPipelineByPropertyName=$true)]
    [string]$Version = "1.0.0",

    [Parameter(ValueFromPipelineByPropertyName=$true)]
    [string]$Project = "",

    [Parameter(ValueFromPipelineByPropertyName=$true)]
    [string]$File = "",

    [Parameter(ValueFromPipelineByPropertyName=$true)]
    [string]$Platform = "auto"
)

# 1. Bật UTF-8 cho Console & Python Subprocess trên Windows
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

# 2. Nhận diện Python Binary & Virtual Environment
$VenvPython = Join-Path (Get-Location) ".venv\Scripts\python.exe"
if (Test-Path $VenvPython) {
    $PythonCmd = $VenvPython
    $PipCmd = Join-Path (Get-Location) ".venv\Scripts\pip.exe"
} else {
    $PythonCmd = "python"
    $PipCmd = "pip"
}

$NodeCmd = "node"

function Show-Header {
    Write-Host ""
    Write-Host "==========================================================================" -ForegroundColor Cyan
    Write-Host "      🚀 AI-VIBE-CODING — DEVELOPER AUTOMATION TOOLKIT (WINDOWS POWERSHELL) " -ForegroundColor Yellow
    Write-Host "==========================================================================" -ForegroundColor Cyan
}

switch ($Action) {
    "help" {
        Show-Header
        Write-Host "  --- 🏛️ TRACK 1: ENTERPRISE FULL-LIFECYCLE SDLC ---" -ForegroundColor Green
        Write-Host "  .\scripts\dev.ps1 dev                                Khởi chạy Fullstack (FastAPI + Frontend)"
        Write-Host "  .\scripts\dev.ps1 dev-backend                        Khởi chạy riêng FastAPI backend (:8000)"
        Write-Host "  .\scripts\dev.ps1 dev-quick                          Chạy tự động hóa toàn trình (CI/CD mode)"
        Write-Host "  .\scripts\dev.ps1 run-backend                        Khởi chạy máy chủ Backend (FastAPI :8000)"
        Write-Host "  .\scripts\dev.ps1 run-frontend                       Khởi chạy máy chủ Web Frontend (:3000 / :5173)"
        Write-Host ""
        Write-Host "  --- ⚡ TRACK 2: TACTICAL FAST-TRACK SQUAD ---" -ForegroundColor Yellow
        Write-Host "  .\scripts\dev.ps1 task -Task `"Mô tả task`"            Thực thi nhanh task hoặc bugfix"
        Write-Host "  .\scripts\dev.ps1 fast-track -Task `"Mô tả task`"       Alias của task (bỏ qua Gate 1 & 2)"
        Write-Host ""
        Write-Host "  --- 🔍 KIỂM THỬ & BẢO ĐẢM HỢP ĐỒNG (GUARDRAILS) ---" -ForegroundColor Cyan
        Write-Host "  .\scripts\dev.ps1 smoke                              Chạy toàn bộ 5 tầng Smoke Test"
        Write-Host "  .\scripts\dev.ps1 test                               Chạy toàn bộ Pytest backend & db"
        Write-Host "  .\scripts\dev.ps1 contracts                          Thẩm định hợp đồng snake_case đa tầng"
        Write-Host "  .\scripts\dev.ps1 migrations                         Kiểm tra toàn vẹn Alembic DAG & drift"
        Write-Host "  .\scripts\dev.ps1 cov-html                           Xuất báo cáo Code Coverage HTML"
        Write-Host "  .\scripts\dev.ps1 test-all                           Chạy toàn diện tất cả các tầng kiểm thử"
        Write-Host "  .\scripts\dev.ps1 test-frontend                      Chạy kiểm thử toàn bộ tầng Frontend"
        Write-Host "  .\scripts\dev.ps1 test-frontend-unit                 Chạy kiểm thử đơn vị Frontend (Unit tests)"
        Write-Host "  .\scripts\dev.ps1 test-frontend-e2e                  Chạy kiểm thử hành trình người dùng (E2E)"
        Write-Host "  .\scripts\dev.ps1 test-orchestrator                  Chạy kiểm thử động cơ điều phối SDLC"
        Write-Host ""
        Write-Host "  --- 💾 STATE CHECKPOINTS & PHỤC HỒI ---" -ForegroundColor Magenta
        Write-Host "  .\scripts\dev.ps1 checkpoint -Phase .. -Status ..    Lưu checkpoint SDLC"
        Write-Host "  .\scripts\dev.ps1 checkpoints                        Xem lịch sử các checkpoint đã lưu"
        Write-Host "  .\scripts\dev.ps1 resume                             Tiếp tục chu trình từ checkpoint gần nhất"
        Write-Host "  .\scripts\dev.ps1 restore -Id ..                     Khôi phục mã nguồn về checkpoint"
        Write-Host "  .\scripts\dev.ps1 sync                               Đồng bộ mã nguồn vào checkpoint"
        Write-Host "  .\scripts\dev.ps1 status                             Xem trạng thái Gate & Tests hiện tại"
        Write-Host ""
        Write-Host "  --- 🎨 CLIENT ARCHITECTURE PRESETS ---" -ForegroundColor Blue
        Write-Host "  .\scripts\dev.ps1 preset-vite                        Chuyển Frontend sang React + Vite SPA"
        Write-Host "  .\scripts\dev.ps1 preset-nextjs                      Chuyển Frontend sang Next.js 15 SSR"
        Write-Host "  .\scripts\dev.ps1 add-mobile                         Khởi tạo Mobile App React Native Expo"
        Write-Host ""
        Write-Host "  --- 📦 TIỆN ÍCH HỆ THỐNG ---" -ForegroundColor Gray
        Write-Host "  .\scripts\dev.ps1 release -Feature .. -Version ..    Đóng gói thành phẩm bản phát hành .zip"
        Write-Host "  .\scripts\dev.ps1 seed                               Nạp dữ liệu mẫu ban đầu vào DB"
        Write-Host "  .\scripts\dev.ps1 snapshot                           Chụp nhanh bản lưu trữ mã nguồn"
        Write-Host "  .\scripts\dev.ps1 docker-up                          Khởi chạy Docker Compose (DB, Backend, Web)"
        Write-Host "  .\scripts\dev.ps1 docker-down                        Dừng toàn bộ Docker containers"
        Write-Host "  .\scripts\dev.ps1 clean                              Dọn dẹp caches, .pyc, dist/"
        Write-Host "  .\scripts\dev.ps1 backup                             Sao lưu tức thời workspace ra thư mục backups"
        Write-Host "  .\scripts\dev.ps1 clean-project                      Dọn sạch output_project và artifacts sau khi backup"
        Write-Host "  .\scripts\dev.ps1 clean-skeleton                     Đưa src/ về trạng thái Day-0 Clean Skeleton"
        Write-Host "  .\scripts\dev.ps1 venv                               Khởi tạo môi trường ảo .venv"
        Write-Host "==========================================================================" -ForegroundColor Cyan
        Write-Host ""
    }

    "smoke" {
        & $PythonCmd scripts\smoke_test.py
    }

    "test" {
        $env:PYTHONPATH = "src"
        & $PythonCmd -m pytest src\backend\tests src\db\tests -v
    }

    "test-backend" {
        $env:PYTHONPATH = "src"
        & $PythonCmd -m pytest src\backend\tests -v
    }

    "test-examples" {
        Write-Host "▶ Đang chạy kiểm thử Dự án Mẫu Tham Khảo (examples\motocare_reference)..." -ForegroundColor Cyan
        if (Test-Path "examples\motocare_reference\output_project\backend") {
            $env:PYTHONPATH = "examples\motocare_reference\output_project\backend"
            & $PythonCmd -m pytest examples\motocare_reference\output_project\backend -v
        } else {
            Write-Host "ℹ️ Không tìm thấy thư mục examples\motocare_reference\output_project" -ForegroundColor Yellow
        }
    }

    "test-cov" {
        $env:PYTHONPATH = "src"
        & $PythonCmd -m pytest src\backend\tests src\db\tests -v --cov=backend.app --cov-report=term-missing
    }

    "cov-html" {
        $env:PYTHONPATH = "src"
        if (-not (Test-Path "workspaces\artifacts\04_quality\htmlcov")) { New-Item -ItemType Directory -Path "workspaces\artifacts\04_quality\htmlcov" -Force | Out-Null }
        & $PythonCmd -m pytest src\backend\tests src\db\tests --cov=backend.app --cov-report=html:workspaces\artifacts\04_quality\htmlcov
        Write-Host "✔ Đã xuất báo cáo HTML coverage tại: workspaces\artifacts\04_quality\htmlcov\index.html" -ForegroundColor Green
    }

    "contracts" {
        & $PythonCmd scripts\verify_contracts.py $Feature
    }

    "migrations" {
        & $PythonCmd scripts\verify_migrations.py
    }

    "check-db" {
        & $PythonCmd -m alembic check
    }

    "test-orchestrator" {
        &  -m pytest tests -v
    }

    "test-frontend-unit" {
         = "src
rontend
un_tests.cjs"
         = "workspaces\output_project
rontend
un_tests.cjs"
        if (Test-Path ) {
            &  
        } elseif (Test-Path ) {
            &  
        } else {
            Push-Location "src
rontend"
            try { npm test } finally { Pop-Location }
        }
    }

    "test-frontend-e2e" {
         = "src
rontend\scripts
un_e2e_tests.cjs"
         = "workspaces\output_project
rontend
un_e2e_tests.cjs"
        if (Test-Path ) {
            &  
        } elseif (Test-Path ) {
            &  
        } else {
            Write-Host "ℹ️ Không tìm thấy kịch bản run_e2e_tests.cjs" -ForegroundColor Yellow
        }
    }

    "test-frontend" {
        Write-Host "▶ Đang kiểm tra TypeScript Strict Mode..." -ForegroundColor Cyan
        if (Test-Path "src
rontend\package.json") {
            Push-Location "src
rontend"
            try { npm run typecheck } finally { Pop-Location }
        }
        & .MyCommand.Path "test-frontend-unit"
        & .MyCommand.Path "test-frontend-e2e"
    }

    "test-all" {
        Write-Host "==========================================================================" -ForegroundColor Cyan
        Write-Host "▶ Đang chạy kiểm tra toàn diện tất cả các tầng (Full Test Suite)..." -ForegroundColor Yellow
        Write-Host "==========================================================================" -ForegroundColor Cyan
        & .MyCommand.Path "smoke"
        & .MyCommand.Path "test"
        & .MyCommand.Path "contracts"
        & .MyCommand.Path "migrations"
        & .MyCommand.Path "test-orchestrator"
        & .MyCommand.Path "test-frontend"
        Write-Host "✔ Đã hoàn thành toàn bộ các bài kiểm thử chất lượng!" -ForegroundColor Green
    }

    "run-backend" {
        if (Test-Path "src\backend\app\main.py") {
            /Users/hunterdo/Documents/Python Project/Team-DevYTHONPATH = "src"
            &  -m uvicorn backend.app.main:app --reload --app-dir "src" --port 8000
        } elseif (Test-Path "workspaces\output_project\backend\app\main.py") {
            /Users/hunterdo/Documents/Python Project/Team-DevYTHONPATH = "workspaces\output_project\backend"
            &  -m uvicorn app.main:app --reload --app-dir "workspaces\output_project\backend" --port 8000
        } else {
            &  scripts\start_dev.py --backend-only
        }
    }

    "run-frontend" {
         = if (Test-Path "src
rontend\package.json") { "src
rontend" } else { "workspaces\output_project
rontend" }
        if (Test-Path ) {
            Push-Location 
            try { npm run dev } finally { Pop-Location }
        } else {
            Write-Host "⚠️ Chưa tìm thấy thư mục Frontend." -ForegroundColor Yellow
        }
    }

    "backup" {
        &  scriptsunner.py --project  --backup
    }

    "clean-project" {
        Write-Host "📦 Đang tự động sao lưu an toàn trước khi dọn dẹp..." -ForegroundColor Yellow
        &  scriptsunner.py --project  --backup
        Write-Host "🧹 Đang dọn sạch output_project và artifacts để sẵn sàng cho dự án mới..." -ForegroundColor Cyan
        &  -c "import shutil, pathlib; [shutil.rmtree(pathlib.Path('workspaces/output_project') / d, ignore_errors=True) for d in ['backend', 'frontend', 'mobile', 'infra']]; [p.unlink(missing_ok=True) for p in pathlib.Path('workspaces/artifacts').rglob('*') if p.is_file() and p.name != '.gitkeep']; [(pathlib.Path('workspaces') / p).mkdir(parents=True, exist_ok=True) for p in ['output_project', 'artifacts/01_discovery', 'artifacts/02_architecture', 'artifacts/04_quality', 'artifacts/05_handover']]; [(pathlib.Path('workspaces') / p / '.gitkeep').touch() for p in ['output_project', 'artifacts/01_discovery', 'artifacts/02_architecture', 'artifacts/04_quality', 'artifacts/05_handover']]"
        Write-Host "✔ Đã tạo backup và dọn sạch workspace an toàn!" -ForegroundColor Green
    }

    "clean-skeleton" {
        &  scripts\clean_skeleton.py --reset
    }

    "dev" {
        if ($File -or ($Project -and (Test-Path $File))) {
            $PlatformArg = if ($Platform -ne "auto") { "--platform $Platform" } else { "" }
            $ProjArg = if ($Project) { "--project `"$Project`"" } else { "" }
            Write-Host "🚀 Khởi chạy chu trình SDLC cho dự án '$Project' từ Brief '$File'..." -ForegroundColor Cyan
            & $PythonCmd scripts\runner.py $ProjArg --brief "$File" $PlatformArg
        } else {
            & $PythonCmd scripts\start_dev.py
        }
    }

    "dev-backend" {
        & $PythonCmd scripts\start_dev.py --backend-only
    }

    "dev-quick" {
        & $PythonCmd scripts\run_headless_sdlc.py --non-interactive
    }

    "task" {
        if ([string]::IsNullOrWhiteSpace($Task)) {
            Write-Host "❌ Vui lòng cung cấp tham số -Task. Ví dụ: .\scripts\dev.ps1 task -Task `"Sửa lỗi validation`"" -ForegroundColor Red
            exit 1
        }
        & $PythonCmd scripts\fast_track.py --task $Task --auto
    }

    "fast-track" {
        if ([string]::IsNullOrWhiteSpace($Task)) {
            Write-Host "❌ Vui lòng cung cấp tham số -Task." -ForegroundColor Red
            exit 1
        }
        & $PythonCmd scripts\fast_track.py --task $Task --auto
    }

    "checkpoint" {
        & $PythonCmd scripts\checkpoint.py save --phase $Phase --status $Status --note $Note
    }

    "checkpoints" {
        & $PythonCmd scripts\checkpoint.py list
    }

    "resume" {
        & $PythonCmd scripts\checkpoint.py resume
    }

    "restore" {
        & $PythonCmd scripts\checkpoint.py restore --checkpoint-id $Id
    }

    "sync" {
        & $PythonCmd scripts\sync_state.py
    }

    "status" {
        & $PythonCmd scripts\sync_state.py --check-only
    }

    "models" {
        & $PythonCmd scripts\agent_dispatcher.py --models
    }

    "mcp" {
        & $PythonCmd scripts\agent_dispatcher.py --mcp
    }

    "subteams" {
        & $PythonCmd scripts\agent_dispatcher.py --list-agents
    }

    "preset-vite" {
        & $PythonCmd scripts\setup_frontend.py --preset vite
    }

    "preset-nextjs" {
        & $PythonCmd scripts\setup_frontend.py --preset nextjs
    }

    "add-mobile" {
        & $PythonCmd scripts\setup_frontend.py --add-mobile
    }

    "release" {
        & $PythonCmd scripts\bundle_release.py $Feature --version $Version
    }

    "seed" {
        $env:PYTHONPATH = "src"
        & $PythonCmd src\db\seeds\runner.py
    }

    "snapshot" {
        & $PythonCmd scripts\snapshot.py manual
    }

    "docker-db" {
        docker compose up -d db
    }

    "docker-up" {
        docker compose up -d db
    }

    "docker-down" {
        docker compose down
    }

    "clean" {
        Get-ChildItem -Path . -Recurse -Include __pycache__ -Directory | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        Get-ChildItem -Path . -Recurse -Include *.pyc -File | Remove-Item -Force -ErrorAction SilentlyContinue
        if (Test-Path ".pytest_cache") { Remove-Item -Recurse -Force .pytest_cache -ErrorAction SilentlyContinue }
        if (Test-Path ".coverage") { Remove-Item -Force .coverage -ErrorAction SilentlyContinue }
        Write-Host "✔ Đã dọn dẹp sạch sẽ caches và temporary files!" -ForegroundColor Green
    }

    "venv" {
        if (-not (Test-Path ".venv")) {
            Write-Host "📦 Đang khởi tạo môi trường ảo Python cô lập tại '.venv'..." -ForegroundColor Cyan
            & $PythonCmd -m venv .venv
            $VenvPip = Join-Path (Get-Location) ".venv\Scripts\pip.exe"
            & $VenvPip install --upgrade pip
            & $VenvPip install -e ".[dev]"
            Write-Host "✔ Môi trường ảo .venv đã được tạo và cài đặt xong toàn bộ thư viện!" -ForegroundColor Green
        } else {
            Write-Host "ℹ️ Môi trường ảo '.venv' đã tồn tại sẵn." -ForegroundColor Yellow
        }
    }

    "install" {
        & $PipCmd install -e ".[dev]"
    }

    "test-output" {
        Write-Host "🧪 [OUTPUT PROJECT] Đang chạy kiểm thử trên workspaces/output_project..." -ForegroundColor Yellow
        &  -m pytest workspaces/output_project/backend/tests -v
    }

    "clean-output" {
        Write-Host "📦 Đang sao lưu và dọn sạch workspaces/output_project/ và workspaces/artifacts/..." -ForegroundColor Yellow
        & .MyCommand.Path "clean-project"
    }

    "lean-workspace" {
        Write-Host "🎯 [LEAN WORKSPACE] Đã kích hoạt chế độ In-Place Vibe Coding tinh gọn!" -ForegroundColor Green
        & .MyCommand.Path "clean-output"
    }
}
