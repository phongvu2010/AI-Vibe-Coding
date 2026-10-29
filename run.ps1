# PowerShell Runner cho Windows Developers (run.ps1)
# Cung cấp bộ lệnh tương đương Makefile cho môi trường Windows với tự động nhận diện .venv
# Hỗ trợ đầy đủ UTF-8 Unicode và tích hợp toàn diện Antigravity 2.0 SDLC

# 1. Bật UTF-8 cho Console & Python Subprocess trên Windows
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

param (
    [Parameter(Position = 0)]
    [string]$Command = "help",

    [Parameter(Position = 1)]
    [string]$Arg1 = "",

    [Parameter(Position = 2)]
    [string]$Arg2 = "",

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ExtraArgs
)

# Tự động nhận diện Python trong .venv nếu có, ngược lại dùng Python hệ thống
$PythonBin = if (Test-Path ".\.venv\Scripts\python.exe") { ".\.venv\Scripts\python.exe" } else { "python" }

function Show-Help {
    Write-Host "========================================================================" -ForegroundColor Cyan
    Write-Host "          AI-VIBE-CODING — BỘ TỰ ĐỘNG HÓA WINDOWS (POWERSHELL)          " -ForegroundColor Cyan
    Write-Host "========================================================================" -ForegroundColor Cyan
    Write-Host "  --- THỰC THI & KIỂM THỬ ---"
    Write-Host "  .\run.ps1 setup             : Khởi tạo virtualenv .venv và cài đặt dependencies"
    Write-Host "  .\run.ps1 fix-env           : Tự động sửa shebang & đồng bộ đường dẫn .venv khi di chuyển thư mục"
    Write-Host "  .\run.ps1 dev               : Khởi chạy Backend FastAPI (Uvicorn reload)"
    Write-Host "  .\run.ps1 dev-quick         : Chạy tự động hóa toàn trình không dừng HITL (CI/CD mode)"
    Write-Host "  .\run.ps1 sdlc              : Chạy tương tác toàn trình 5 Phases với Human-in-the-Loop TUI"
    Write-Host "  .\run.ps1 dev-interactive   : Bí danh của .\run.ps1 sdlc"
    Write-Host "  .\run.ps1 synthesize        : Tổng hợp mã nguồn Clean Architecture ngoại tuyến (Zero-Token)"
    Write-Host "  .\run.ps1 test              : Chạy kiểm thử Pytest trên SQLite in-memory"
    Write-Host "  .\run.ps1 test-all          : Chạy toàn diện tất cả các bài kiểm thử (Engine, Smoke, E2E, Contracts)"
    Write-Host "  .\run.ps1 test-backend      : Chạy riêng kiểm thử Backend API"
    Write-Host "  .\run.ps1 test-db           : Chạy riêng kiểm thử Tầng Cơ Sở Dữ Liệu (src/db/tests)"
    Write-Host "  .\run.ps1 test-examples     : Chạy kiểm thử cho Dự Án Mẫu Tham Khảo (Golden Reference)"
    Write-Host "  .\run.ps1 test-e2e          : Chạy kiểm thử E2E giả lập hành trình người dùng (run_e2e_tests.cjs)"
    Write-Host "  .\run.ps1 test-cov          : Chạy Pytest kèm đo độ phủ mã nguồn (Coverage >= 80%)"
    Write-Host "  .\run.ps1 cov-html          : Xuất báo cáo độ phủ Code Coverage HTML (workspaces/artifacts/...)"
    Write-Host "  .\run.ps1 smoke             : Chạy bộ kiểm thử tự động 5 tầng (smoke_test.py)"
    Write-Host "  .\run.ps1 contracts         : Kiểm tra đồng bộ hợp đồng dữ liệu đa tầng (alias: check-contracts)"
    Write-Host "  .\run.ps1 handshake         : Chốt chặn kiểm thử Handshake Wave 1 cô lập (Models + Contracts)"
    Write-Host "  .\run.ps1 migrations        : Kiểm tra toàn vẹn đồ thị Alembic Migrations (alias: check-migrations)"
    Write-Host "  .\run.ps1 typecheck         : Kiểm tra kiểu dữ liệu TypeScript Web Frontend"
    Write-Host "  .\run.ps1 typecheck-mobile  : Kiểm tra kiểu dữ liệu TypeScript Mobile App"
    Write-Host "  .\run.ps1 check-frontend    : Thẩm định tính sẵn sàng Build của Frontend"
    Write-Host "  .\run.ps1 seed              : Khởi tạo dữ liệu mẫu ban đầu"
    Write-Host "  .\run.ps1 release           : Đóng gói bản phát hành (.zip, manifest, UAT checklist)"
    Write-Host "  .\run.ps1 docker-logs       : Xem logs trực tiếp của Docker Containers"
    Write-Host "  .\run.ps1 models            : Xem ma trận định tuyến mô hình AI & tối ưu token"
    Write-Host "  .\run.ps1 clean             : Xóa sạch bytecode, cache và files tạm thời"
    Write-Host ""
    Write-Host "  --- TÁC TỬ & SUBAGENTS ANTIGRAVITY 2.0 ---"
    Write-Host "  .\run.ps1 agents-check      : Xác thực 20 Subagents, Squad specs & Skills"
    Write-Host "  .\run.ps1 agents-list       : Liệt kê danh sách và vai trò của 5 Sub-Teams"
    Write-Host "  .\run.ps1 task <mô tả>      : Chạy tác vụ nhanh qua Fast-Track Tactical Squad"
    Write-Host ""
    Write-Host "  --- HUMAN-IN-THE-LOOP & QUALITY GATES ---"
    Write-Host "  .\run.ps1 gate <1|2|3>      : Kích hoạt chốt chặn tương tác Human-in-the-Loop (Terminal Prompt)"
    Write-Host "  .\run.ps1 gate-review <1|2|3>: Xuất biên bản đánh giá Quality Gate Review Markdown"
    Write-Host "  .\run.ps1 auto-heal         : Chạy Heuristic Auto-Healing sửa lỗi zero-token"
    Write-Host ""
    Write-Host "  --- PRESETS & CLIENT ARCHITECTURE ---"
    Write-Host "  .\run.ps1 frontend-status   : Kiểm tra trạng thái hiện tại của Web & Mobile Client"
    Write-Host "  .\run.ps1 preset-vite       : Chuyển đổi Web Client sang React + Vite (SPA / Fast) (alias: setup-vite)"
    Write-Host "  .\run.ps1 preset-nextjs     : Chuyển đổi Web Client sang Next.js 15 (SSR / SEO) (alias: setup-nextjs)"
    Write-Host "  .\run.ps1 add-mobile        : Khởi tạo App Mobile React Native Expo trong src/mobile/ (alias: setup-mobile)"
    Write-Host ""
    Write-Host "  --- STATE CHECKPOINTS, BACKUP & WORKSPACE LIFECYCLE ---"
    Write-Host "  .\run.ps1 sync              : Quét mã nguồn thực tế và đồng bộ trạng thái vào Checkpoint"
    Write-Host "  .\run.ps1 status            : Xem tổng quan sức khỏe dự án & trạng thái Checkpoint"
    Write-Host "  .\run.ps1 checkpoint <p> <n>: Lưu Checkpoint mới kèm Snapshot mã nguồn"
    Write-Host "  .\run.ps1 checkpoints       : Liệt kê danh sách toàn bộ các checkpoints đã lưu"
    Write-Host "  .\run.ps1 resume            : Xem vị trí dừng và hướng dẫn tiếp tục phiên làm việc"
    Write-Host "  .\run.ps1 restore <id>      : Khôi phục mã nguồn và trạng thái về checkpoint cụ thể"
    Write-Host "  .\run.ps1 backup [tên]      : Sao lưu toàn bộ dự án hiện tại vào dist/backups/"
    Write-Host "  .\run.ps1 clean-project     : Sao lưu an toàn và dọn sạch dự án để nhận brief mới"
    Write-Host "  .\run.ps1 clean-output      : Dọn sạch workspaces/output_project và artifacts"
    Write-Host "  .\run.ps1 run-output-backend : Khởi chạy FastAPI Server cho output_project (:8000)"
    Write-Host "  .\run.ps1 run-output-frontend: Khởi chạy Web/Mobile Frontend cho output_project"
    Write-Host "  .\run.ps1 docker-output-up  : Khởi động Multi-Container Docker cho output_project"
    Write-Host "  .\run.ps1 docker-output-down: Dừng toàn bộ Docker containers của output_project"
    Write-Host "  .\run.ps1 clean-skeleton    : Đưa src/ về trạng thái Day-0 Clean Skeleton sạch sẽ"
    Write-Host "  .\run.ps1 restore-skeleton  : Khôi phục lại dữ liệu mẫu Demo trước đó"
    Write-Host "========================================================================" -ForegroundColor Cyan
}

switch ($Command.ToLower()) {
    "setup" {
        Write-Host "📦 Đang khởi tạo môi trường ảo và cài đặt dependencies..." -ForegroundColor Green
        python -m venv .venv
        .\.venv\Scripts\python.exe -m pip install --upgrade pip
        if (Test-Path "requirements.txt") {
            .\.venv\Scripts\pip.exe install -r requirements.txt
        } else {
            .\.venv\Scripts\pip.exe install -e ".[dev]"
        }
        & $PythonBin scripts/fix_venv.py
    }
    "fix-env" {
        Write-Host "🔧 Đang sửa và đồng bộ đường dẫn môi trường ảo .venv..." -ForegroundColor Green
        & $PythonBin scripts/fix_venv.py
    }
    "dev" {
        Write-Host "🚀 Đang khởi động Backend FastAPI (Python: $PythonBin)..." -ForegroundColor Green
        & $PythonBin -m uvicorn src.backend.app.main:app --reload --port 8000
    }
    "dev-backend" {
        Write-Host "🚀 [Alias] Đang khởi động Backend FastAPI (Python: $PythonBin)..." -ForegroundColor Green
        & $PythonBin -m uvicorn src.backend.app.main:app --reload --port 8000
    }
    "dev-frontend" {
        Write-Host "🌐 Đang khởi động riêng Web Frontend (:3000)..." -ForegroundColor Green
        if (Test-Path "src/frontend") {
            Push-Location src/frontend
            npm run dev
            Pop-Location
        } else {
            Write-Host "❌ Không tìm thấy thư mục src/frontend. Hãy khởi tạo qua .\run.ps1 preset-vite" -ForegroundColor Red
        }
    }
    "run-backend" {
        Write-Host "🚀 [Alias] Đang khởi động Backend FastAPI (Python: $PythonBin)..." -ForegroundColor Green
        & $PythonBin -m uvicorn src.backend.app.main:app --reload --port 8000
    }
    "run-frontend" {
        Write-Host "🌐 [Alias] Đang khởi động riêng Web Frontend (:3000)..." -ForegroundColor Green
        if (Test-Path "src/frontend") {
            Push-Location src/frontend
            npm run dev
            Pop-Location
        } else {
            Write-Host "❌ Không tìm thấy thư mục src/frontend. Hãy khởi tạo qua .\run.ps1 preset-vite" -ForegroundColor Red
        }
    }
    "venv" {
        Write-Host "📦 [Alias] Đang khởi tạo môi trường ảo và cài đặt dependencies..." -ForegroundColor Green
        python -m venv .venv
        .\.venv\Scripts\python.exe -m pip install --upgrade pip
        if (Test-Path "requirements.txt") {
            .\.venv\Scripts\pip.exe install -r requirements.txt
        } else {
            .\.venv\Scripts\pip.exe install -e ".[dev]"
        }
    }
    "install" {
        Write-Host "📦 [Alias] Đang cài đặt dependencies..." -ForegroundColor Green
        if (Test-Path "requirements.txt") {
            .\.venv\Scripts\pip.exe install -r requirements.txt
        } else {
            .\.venv\Scripts\pip.exe install -e ".[dev]"
        }
    }
    "test-orchestrator" {
        Write-Host "🧪 [Alias] Đang chạy kiểm thử cho lõi Orchestrator & Subagents..." -ForegroundColor Green
        & $PythonBin -m pytest -v tests
    }
    "dev-quick" {
        Write-Host "⚡ Khởi chạy chế độ Headless / CI-CD tự động hóa không chặn..." -ForegroundColor Green
        & $PythonBin scripts/run_headless_sdlc.py
    }
    "sdlc" {
        Write-Host "🎮 Khởi chạy chế độ Interactive SDLC với Human-in-the-Loop TUI..." -ForegroundColor Cyan
        & $PythonBin scripts/run_interactive_sdlc.py
    }
    "dev-interactive" {
        & $PythonBin scripts/run_interactive_sdlc.py
    }
    "test" {
        Write-Host "🧪 Đang chạy kiểm thử Pytest Backend (Python: $PythonBin)..." -ForegroundColor Green
        & $PythonBin -m pytest -v src/backend/tests tests
    }
    "test-all" {
        Write-Host "==========================================================================" -ForegroundColor Cyan
        Write-Host "▶ Đang chạy kiểm tra toàn diện tất cả các tầng (Full Test Suite)..." -ForegroundColor Yellow
        Write-Host "==========================================================================" -ForegroundColor Cyan
        & $PythonBin -m pytest -v tests
        & $PythonBin scripts/smoke_test.py
        node src/frontend/scripts/run_e2e_tests.cjs
        & $PythonBin scripts/verify_contracts.py
        Write-Host "🎉 [TEST-ALL PASSED] Đã hoàn thành toàn bộ các bài kiểm thử chất lượng!" -ForegroundColor Green
    }
    "test-backend" {
        Write-Host "🧪 Đang chạy riêng kiểm thử Backend API..." -ForegroundColor Green
        $env:PYTHONPATH = "src"
        & $PythonBin -m pytest -v src/backend/tests
    }
    "test-db" {
        Write-Host "🧪 Đang chạy riêng kiểm thử Tầng Cơ Sở Dữ Liệu (Python: $PythonBin)..." -ForegroundColor Green
        $env:PYTHONPATH = "src"
        & $PythonBin -m pytest -v src/db/tests
    }
    "test-examples" {
        Write-Host "🧪 Đang chạy kiểm thử toàn diện Dự Án Mẫu Tham Khảo (Golden Reference)..." -ForegroundColor Cyan
        if (Test-Path "examples/motocare_reference/output_project/backend") {
            Write-Host "▶ [1/4] Chạy Pytest Backend kèm đo độ phủ Coverage:" -ForegroundColor Yellow
             = /Users/hunterdo/Documents/Python Project/Team-DevYTHONPATH
            /Users/hunterdo/Documents/Python Project/Team-DevYTHONPATH = "examples/motocare_reference/output_project/backend"
            &  -m pytest examples/motocare_reference/output_project/backend/tests -v --cov=app --cov-report=term-missing
            /Users/hunterdo/Documents/Python Project/Team-DevYTHONPATH = 

            Write-Host "▶ [2/4] Kiểm tra Alembic Database Migrations & Zero Schema Drift:" -ForegroundColor Yellow
            Push-Location "examples/motocare_reference/output_project/backend"
            &  -m alembic upgrade head
            &  -m alembic check
            Pop-Location

            if ((Test-Path "examples/motocare_reference/output_project/frontend/run_tests.cjs") -and (Get-Command node -ErrorAction SilentlyContinue)) {
                Write-Host "▶ [3/4] Chạy Frontend Unit Tests (Jest / CJS Assertions):" -ForegroundColor Yellow
                node examples/motocare_reference/output_project/frontend/run_tests.cjs
            }

            if ((Test-Path "examples/motocare_reference/output_project/frontend/run_e2e_tests.cjs") -and (Get-Command node -ErrorAction SilentlyContinue)) {
                Write-Host "▶ [4/4] Chạy Frontend E2E / Contract Tests:" -ForegroundColor Yellow
                node examples/motocare_reference/output_project/frontend/run_e2e_tests.cjs
            }

            Write-Host "✔ Toàn bộ test suite của Dự án Mẫu Golden Reference ĐÃ PASS 100%!" -ForegroundColor Green
        } else {
            Write-Host "ℹ️ Không tìm thấy thư mục examples/motocare_reference/output_project" -ForegroundColor Yellow
        }
    }
    "test-e2e" {
        Write-Host "🌐 Đang chạy kiểm thử Frontend E2E / User Journey..." -ForegroundColor Green
        if (Test-Path "src/frontend/scripts/run_e2e_tests.cjs") {
            node src/frontend/scripts/run_e2e_tests.cjs
        } elseif (Test-Path "examples/motocare_reference/output_project/frontend/run_e2e_tests.cjs") {
            node examples/motocare_reference/output_project/frontend/run_e2e_tests.cjs
        } else {
            Write-Host "ℹ️ Không tìm thấy kịch bản run_e2e_tests.cjs" -ForegroundColor Yellow
        }
    }
    "test-frontend-e2e" {
        Write-Host "🌐 [Alias] Đang chạy kiểm thử Frontend E2E..." -ForegroundColor Green
        if (Test-Path "src/frontend/scripts/run_e2e_tests.cjs") {
            node src/frontend/scripts/run_e2e_tests.cjs
        } else {
            Write-Host "ℹ️ Không tìm thấy src/frontend/scripts/run_e2e_tests.cjs" -ForegroundColor Yellow
        }
    }
    "test-cov" {
        Write-Host "📊 Đang chạy Pytest kèm đo độ phủ Code Coverage..." -ForegroundColor Green
        if (-not (Test-Path "workspaces/artifacts/04_quality/htmlcov")) { New-Item -ItemType Directory -Path "workspaces/artifacts/04_quality/htmlcov" -Force | Out-Null }
        & $PythonBin -m pytest --cov=src/backend/app --cov-report=term-missing --cov-report=html:workspaces/artifacts/04_quality/htmlcov --cov-fail-under=80 src/backend/tests
    }
    "cov-html" {
        Write-Host "📊 Đang xuất báo cáo Code Coverage HTML vào workspaces/artifacts/04_quality/htmlcov..." -ForegroundColor Green
        if (-not (Test-Path "workspaces/artifacts/04_quality/htmlcov")) { New-Item -ItemType Directory -Path "workspaces/artifacts/04_quality/htmlcov" -Force | Out-Null }
        & $PythonBin -m pytest --cov=src/backend/app --cov-report=html:workspaces/artifacts/04_quality/htmlcov src/backend/tests
        Write-Host "✔ Đã xuất báo cáo tại: workspaces/artifacts/04_quality/htmlcov/index.html" -ForegroundColor Green
    }
    "smoke" {
        Write-Host "🔥 Đang chạy bộ kiểm thử tự động 5 tầng (Python: $PythonBin)..." -ForegroundColor Green
        & $PythonBin scripts/smoke_test.py
    }
    "check-network" {
        Write-Host "🔍 Đang kiểm tra thông mạng đa cổng (Python: $PythonBin)..." -ForegroundColor Green
        & $PythonBin scripts/verify_network.py
    }
    "contracts" {
        Write-Host "📐 Đang kiểm tra đồng bộ hợp đồng dữ liệu..." -ForegroundColor Green
        & $PythonBin scripts/verify_contracts.py
    }
    "check-contracts" {
        Write-Host "📐 [Alias] Đang kiểm tra đồng bộ hợp đồng dữ liệu..." -ForegroundColor Green
        & $PythonBin scripts/verify_contracts.py
    }
    "migrations" {
        Write-Host "🗄️ Đang kiểm tra đồ thị Alembic Migrations..." -ForegroundColor Green
        & $PythonBin scripts/verify_migrations.py
    }
    "check-migrations" {
        Write-Host "🗄️ [Alias] Đang kiểm tra đồ thị Alembic Migrations..." -ForegroundColor Green
        & $PythonBin scripts/verify_migrations.py
    }
    "typecheck" {
        Write-Host "🌐 Đang kiểm tra kiểu dữ liệu TypeScript Web Frontend..." -ForegroundColor Green
        npm --prefix src/frontend run typecheck
    }
    "typecheck-mobile" {
        Write-Host "📱 Đang kiểm tra kiểu dữ liệu TypeScript Mobile App..." -ForegroundColor Green
        npm --prefix src/mobile run typecheck
    }
    "check-frontend" {
        Write-Host "🔍 Đang thẩm định tính sẵn sàng Build của Frontend..." -ForegroundColor Green
        if (Test-Path "src/frontend/package.json") {
            node -e "const pkg = require('./src/frontend/package.json'); console.log('  ✔ package.json: ' + pkg.name); if (!pkg.scripts) throw new Error('Thiếu scripts');"
            if (Test-Path "src/frontend/tsconfig.json") {
                Write-Host "  ✔ tsconfig.json hợp lệ" -ForegroundColor Green
            }
            if (Test-Path "src/frontend/node_modules") {
                npm --prefix src/frontend run typecheck
            }
            Write-Host "✔ Frontend Build Ready!" -ForegroundColor Green
        }
    }
    "models" {
        Write-Host "🧠 Ma Trận Định Tuyến Mô Hình AI (config/model_router.yaml):" -ForegroundColor Cyan
        & $PythonBin scripts/agent_dispatcher.py --models
    }
    "mcp" {
        Write-Host "🔌 Quét danh sách MCP Servers & Tools khả dụng trên Antigravity 2.0:" -ForegroundColor Cyan
        & $PythonBin scripts/agent_dispatcher.py --mcp
    }
    "task" {
        $taskDesc = if ($Arg1) { $Arg1 } else { "Sửa lỗi hoặc cập nhật tính năng" }
        & $PythonBin scripts/fast_track.py --task $taskDesc $ExtraArgs
    }
    "fast-track" {
        $taskDesc = if ($Arg1) { $Arg1 } else { "Sửa lỗi hoặc cập nhật tính năng" }
        & $PythonBin scripts/fast_track.py --task $taskDesc $ExtraArgs
    }
    "seed" {
        Write-Host "🌱 Đang nạp dữ liệu mẫu..." -ForegroundColor Green
        & $PythonBin src/db/seeds/runner.py
    }
    "snapshot" {
        $tag = if ($Arg1) { $Arg1 } else { "manual" }
        Write-Host "📦 Đang tạo bản sao chụp mã nguồn..." -ForegroundColor Green
        & $PythonBin scripts/snapshot.py take $tag
    }
    "snapshot-dir" {
        $tag = if ($Arg1) { $Arg1 } else { "manual" }
        Write-Host "📁 Đang tạo bản sao chụp thư mục sống (.snapshots/)..." -ForegroundColor Green
        & $PythonBin scripts/snapshot.py take $tag --dir
    }
    "snapshot-diff" {
        $tag = if ($Arg1) { $Arg1 } else { "manual" }
        & $PythonBin scripts/snapshot.py diff $tag
    }
    "snapshot-list" {
        & $PythonBin scripts/snapshot.py list
    }
    "snapshot-restore" {
        if (-not $Arg1) {
            Write-Host "❌ Vui lòng cung cấp tên snapshot cần khôi phục: .\run.ps1 snapshot-restore <name>" -ForegroundColor Red
        } else {
            Write-Host "🔄 Đang khôi phục mã nguồn từ bản chụp '$Arg1'..." -ForegroundColor Green
            & $PythonBin scripts/snapshot.py restore $Arg1
        }
    }
    "domain-analyze" {
        $target = if ($Arg1) { $Arg1 } else { "examples/sample_client_brief.md" }
        & $PythonBin scripts/domain_analyzer.py $target
    }
    "synthesize" {
        $target = if ($Arg1) { $Arg1 } else { "examples/sample_client_brief.md" }
        $proj = if ($Arg2) { $Arg2 } else { "SmartApp" }
        Write-Host "⚙️ Đang thực hiện tổng hợp mã nguồn cơ sở Clean Architecture ngoại tuyến (Zero-Token)..." -ForegroundColor Green
        & $PythonBin scripts/synthesis_engine.py --brief $target --project-name $proj
    }
    "release" {
        $slug = if ($Arg1) { $Arg1 } else { "core-release" }
        $ver = if ($Arg2) { $Arg2 } else { "1.0.0" }
        Write-Host "🎁 Đang đóng gói bản phát hành ($slug v$ver)..." -ForegroundColor Green
        & $PythonBin scripts/bundle_release.py $slug --version $ver
    }
    "docker-db" {
        Write-Host "🐘 Đang khởi động riêng PostgreSQL Database container độc lập (Port 5432)..." -ForegroundColor Green
        docker compose up -d db
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
    "docker-logs" {
        Write-Host "📋 Đang lấy live log từ Docker Compose..." -ForegroundColor Green
        docker compose logs -f
    }
    "frontend-status" {
        & $PythonBin scripts/setup_frontend.py --status
    }
    "preset-vite" {
        & $PythonBin scripts/setup_frontend.py --preset vite
    }
    "setup-vite" {
        & $PythonBin scripts/setup_frontend.py --preset vite
    }
    "preset-nextjs" {
        & $PythonBin scripts/setup_frontend.py --preset nextjs
    }
    "setup-nextjs" {
        & $PythonBin scripts/setup_frontend.py --preset nextjs
    }
    "add-mobile" {
        & $PythonBin scripts/setup_frontend.py --add-mobile
    }
    "setup-mobile" {
        & $PythonBin scripts/setup_frontend.py --add-mobile
    }
    "status" {
        & $PythonBin scripts/sync_state.py --check-only
    }
    "checkpoint-status" {
        & $PythonBin scripts/checkpoint.py status
    }
    "sync" {
        & $PythonBin scripts/sync_state.py
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
    "backup" {
        $backupName = if ($Arg1) { $Arg1 } else { "backup_" + (Get-Date -Format "yyyyMMdd_HHmmss") }
        $backupDir = "dist/backups"
        if (-not (Test-Path $backupDir)) { New-Item -ItemType Directory -Path $backupDir | Out-Null }
        $zipPath = "$backupDir/$backupName.zip"
        Write-Host "📦 Đang sao lưu toàn bộ dự án vào $zipPath..." -ForegroundColor Green
        Compress-Archive -Path src, docs, templates -DestinationPath $zipPath -Force
        Write-Host "✅ Sao lưu thành công: $zipPath" -ForegroundColor Green
    }
    "clean-project" {
        Write-Host "⚠️ Đang tạo bản sao lưu an toàn trước khi dọn sạch dự án..." -ForegroundColor Yellow
        $ts = Get-Date -Format "yyyyMMdd_HHmmss"
        .\run.ps1 backup "pre_clean_$ts"
        Write-Host "🧹 Đang dọn sạch mã nguồn và specs để sẵn sàng đón nhận dự án mới..." -ForegroundColor Yellow
        & $PythonBin scripts/checkpoint.py save --phase "pre_clean" --note "Lưu trước khi reset dự án"
        Write-Host "✅ Không gian làm việc đã sẵn sàng cho đề bài mới!" -ForegroundColor Green
    }
    "new-project" {
        $projectName = if ($Arg1) { $Arg1 } else { "MyProject" }
        $briefFile = if ($Arg2) { $Arg2 } else { "examples/sample_client_brief.md" }
        Write-Host "🏭 [APP FACTORY] Khởi tạo dự án độc lập '$projectName'..." -ForegroundColor Cyan
        & $PythonBin scripts/synthesis_engine.py --brief $briefFile --output-dir "workspaces/output_project/$projectName" --project-name $projectName
        Write-Host "✅ Đã sinh mã độc lập thành công tại workspaces/output_project/$projectName!" -ForegroundColor Green
    }
    "clean-skeleton" {
        & $PythonBin scripts/clean_skeleton.py --reset
    }
    "restore-skeleton" {
        & $PythonBin scripts/clean_skeleton.py --restore
    }
    "agents-check" {
        & $PythonBin scripts/register_agents.py --validate
    }
    "agents-list" {
        & $PythonBin scripts/register_agents.py --list
    }
    "gate" {
        $GateNum = if ($Arg1) { $Arg1 } else { "1" }
        $FeatureSlug = if ($Arg2) { $Arg2 } else { "motocare-booking" }
        Write-Host "🚦 Đang kích hoạt chốt chặn tương tác Quality Gate $GateNum cho feature '$FeatureSlug'..." -ForegroundColor Yellow
        & $PythonBin scripts/generate_gate_review.py --gate $GateNum --feature $FeatureSlug --interactive
    }
    "gate-interactive" {
        $GateNum = if ($Arg1) { $Arg1 } else { "1" }
        $FeatureSlug = if ($Arg2) { $Arg2 } else { "motocare-booking" }
        Write-Host "🚦 Đang kích hoạt chốt chặn tương tác Quality Gate $GateNum cho feature '$FeatureSlug'..." -ForegroundColor Yellow
        & $PythonBin scripts/generate_gate_review.py --gate $GateNum --feature $FeatureSlug --interactive
    }
    "gate-review" {
        $GateNum = if ($Arg1) { $Arg1 } else { "1" }
        $FeatureSlug = if ($Arg2) { $Arg2 } else { "motocare-booking" }
        Write-Host "📋 Đang xuất biên bản đánh giá Quality Gate $GateNum..." -ForegroundColor Cyan
        & $PythonBin scripts/generate_gate_review.py --gate $GateNum --feature $FeatureSlug
    }
    "auto-heal" {
        Write-Host "🩺 Đang thực thi Heuristic Auto-Healing (Zero-Token Rule Patcher)..." -ForegroundColor Cyan
        & $PythonBin scripts/auto_heal_heuristics.py --apply
    }
    "handshake" {
        Write-Host "🤝 Đang kiểm tra Wave 1 Handshake Gate (Database Models + Contracts + Frontend Mock)..." -ForegroundColor Cyan
        Write-Host "1/3. Biên dịch tĩnh toàn bộ Database Models..."
        &  -m py_compile src/db/models/*.py
        Write-Host "2/3. Đối soát Hợp đồng Dữ liệu Đa tầng (Cross-Layer Contract Parity)..."
        &  scripts/verify_contracts.py
        Write-Host "3/3. Kiểm tra tính toàn vẹn Frontend Mock..."
        if (Test-Path "src/frontend") {
            Write-Host "✔ Frontend Web sẵn sàng kết nối Live API." -ForegroundColor Green
        }
        Write-Host "✅ [WAVE 1 HANDSHAKE PASSED] Database models & Mock contracts sẵn sàng để Wave 2 kết nối!" -ForegroundColor Green
    }
    "test-wave1-handshake" {
        &  handshake
    }
    "clean" {
        Write-Host "🧹 Đang dọn dẹp các tệp tạm..." -ForegroundColor Yellow
        Get-ChildItem -Path . -Include __pycache__, .pytest_cache, .ruff_cache -Recurse -Directory -Force | Remove-Item -Recurse -Force
        Get-ChildItem -Path . -Include *.pyc -Recurse -File -Force | Remove-Item -Force
        Write-Host "✅ Dọn dẹp hoàn tất!" -ForegroundColor Green
    }
    "test-output" {
        Write-Host "🧪 [OUTPUT PROJECT] Đang chạy kiểm thử trên workspaces/output_project..." -ForegroundColor Yellow
        &  -m pytest workspaces/output_project/backend/tests -v
    }
    "run-output-backend" {
         = Get-ChildItem -Path "workspaces/output_project" -Directory -Recurse -Depth 2 -Filter "backend" | Select-Object -First 1
        if () {
            Write-Host "🚀 [OUTPUT PROJECT] Khởi chạy FastAPI Server tại http://localhost:8000..." -ForegroundColor Green
            Push-Location .FullName
            /Users/hunterdo/Documents/Python Project/Team-DevYTHONPATH = "."
            &  -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
            Pop-Location
        } else {
            Write-Host "⚠️ Chưa tìm thấy Backend trong workspaces/output_project/ để khởi chạy." -ForegroundColor Yellow
        }
    }
    "run-output-frontend" {
         = Get-ChildItem -Path "workspaces/output_project" -Directory -Recurse -Depth 2 -Filter "frontend" | Select-Object -First 1
        if () {
            Write-Host "🌐 [OUTPUT PROJECT] Khởi chạy Frontend..." -ForegroundColor Green
            Push-Location .FullName
            if (Test-Path "setup_dev.sh") {
                bash setup_dev.sh
            } elseif (Test-Path "package.json") {
                npm run dev
            }
            Pop-Location
        } else {
            Write-Host "⚠️ Chưa tìm thấy Frontend trong workspaces/output_project/ để khởi chạy." -ForegroundColor Yellow
        }
    }
    "docker-output-build" {
         = Get-ChildItem -Path "workspaces/output_project" -Directory -Recurse -Depth 2 -Filter "infra" | Select-Object -First 1
        if ( -and (Test-Path (Join-Path .FullName "docker-compose.yml"))) {
            Write-Host "🐳 [OUTPUT PROJECT] Đang đóng gói Docker Compose Images..." -ForegroundColor Cyan
            docker compose -f (Join-Path .FullName "docker-compose.yml") build
        } else {
            Write-Host "⚠️ Chưa tìm thấy infra/docker-compose.yml trong workspaces/output_project/." -ForegroundColor Yellow
        }
    }
    "docker-output-up" {
         = Get-ChildItem -Path "workspaces/output_project" -Directory -Recurse -Depth 2 -Filter "infra" | Select-Object -First 1
        if ( -and (Test-Path (Join-Path .FullName "docker-compose.yml"))) {
            Write-Host "🐳 [OUTPUT PROJECT] Đang khởi động Docker Containers..." -ForegroundColor Cyan
            docker compose -f (Join-Path .FullName "docker-compose.yml") up -d
            Write-Host "✔ Hệ thống multi-container đang chạy ngầm (Web :80, API :8000, DB :5432)!" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Chưa tìm thấy infra/docker-compose.yml trong workspaces/output_project/." -ForegroundColor Yellow
        }
    }
    "docker-output-down" {
         = Get-ChildItem -Path "workspaces/output_project" -Directory -Recurse -Depth 2 -Filter "infra" | Select-Object -First 1
        if ( -and (Test-Path (Join-Path .FullName "docker-compose.yml"))) {
            docker compose -f (Join-Path .FullName "docker-compose.yml") down
            Write-Host "✔ Đã dừng toàn bộ containers của Output Project!" -ForegroundColor Green
        }
    }
    "docker-output-logs" {
         = Get-ChildItem -Path "workspaces/output_project" -Directory -Recurse -Depth 2 -Filter "infra" | Select-Object -First 1
        if ( -and (Test-Path (Join-Path .FullName "docker-compose.yml"))) {
            docker compose -f (Join-Path .FullName "docker-compose.yml") logs -f
        }
    }
    "clean-output" {
        Write-Host "📦 Đang sao lưu và dọn sạch workspaces/output_project/ và workspaces/artifacts/..." -ForegroundColor Yellow
        .un.ps1 clean-project
    }
    "lean-workspace" {
        Write-Host "🎯 [LEAN WORKSPACE] Đã kích hoạt chế độ In-Place Vibe Coding tinh gọn!" -ForegroundColor Green
        .un.ps1 clean-output
    }
    default {
        Show-Help
    }
}
