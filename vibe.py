#!/usr/bin/env python3
"""
vibe.py — Trình Điều Khiển Dòng Lệnh Hợp Nhất (AI-Vibe-Coding Unified CLI)
Chuyển hóa môi trường Antigravity 2.0 thành một công ty phần mềm AI vận hành 1-chạm.

Cách sử dụng:
    vibe                  : Mở bảng điều khiển tổng quan và trợ giúp trực quan
    vibe dev              : Khởi động hệ thống phát triển Fullstack (FastAPI + Web)
    vibe test             : Kích hoạt toàn diện Bộ kiểm thử tự động 5 tầng (Smoke Test)
    vibe task "<mô tả>"  : Kích hoạt Tactical Fast-Track Squad xử lý micro-task / bugfix
    vibe new "<dự án>"   : Kích hoạt Chu trình 5 Sub-Teams phát triển dự án mới (SDLC)
    vibe contract         : Kiểm tra và đối chiếu đồng bộ Hợp đồng Dữ liệu Đa tầng (AST)
    vibe heal             : Vá lỗi tự động ngoại tuyến theo luật Heuristics (0 Token)
    vibe fix-env          : Sửa lỗi shebang đường dẫn môi trường ảo .venv
    vibe status           : Kiểm tra trạng thái sức khỏe, Checkpoint và Model Routing
"""

import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path

# Đảm bảo console UTF-8 trên Windows
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT_DIR / "scripts"

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None


def get_python_bin() -> str:
    """Tự động phát hiện Python trong virtualenv."""
    is_windows = platform.system() == "Windows"
    rel_path = "Scripts/python.exe" if is_windows else "bin/python"
    candidate = ROOT_DIR / ".venv" / rel_path
    return str(candidate) if candidate.exists() else sys.executable


def run_script(script_name: str, args: list[str] = None) -> int:
    """Thực thi một script Python trong scripts/ với virtualenv hiện tại."""
    python_bin = get_python_bin()
    target_script = SCRIPTS_DIR / script_name
    if not target_script.exists():
        target_script = ROOT_DIR / script_name

    cmd = [python_bin, str(target_script)] + (args or [])

    env = os.environ.copy()
    src_path = str(ROOT_DIR / "src")
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{src_path}{os.pathsep}{existing_pythonpath}" if existing_pythonpath else src_path

    try:
        res = subprocess.run(cmd, cwd=str(ROOT_DIR), env=env)
        return res.returncode
    except KeyboardInterrupt:
        print("\n🛑 Tiến trình bị gián đoạn bởi người dùng.")
        return 130


def show_dashboard():
    """Hiển thị Dashboard chỉ huy trực quan."""
    if HAS_RICH:
        banner = """[bold cyan]
   █████╗ ██╗      ██╗   ██╗██╗██████╗ ███████╗     ██████╗ ██████╗ ██████╗ ██╗███╗   ██╗ ██████╗ 
  ██╔══██╗██║      ██║   ██║██║██╔══██╗██╔════╝    ██╔════╝██╔═══██╗██╔══██╗██║████╗  ██║██╔════╝ 
  ███████║██║█████╗██║   ██║██║██████╔╝█████╗      ██║     ██║   ██║██║  ██║██║██╔██╗ ██║██║  ███╗
  ██╔══██║██║╚════╝╚██╗ ██╔╝██║██╔══██╗██╔══╝      ██║     ██║   ██║██║  ██║██║██║╚██╗██║██║   ██║
  ██║  ██║██║       ╚████╔╝ ██║██████╔╝███████╗    ╚██████╗╚██████╔╝██████╔╝██║██║ ╚████║╚██████╔╝
  ╚═╝  ╚═╝╚═╝        ╚═══╝  ╚═╝╚═════╝ ╚══════╝     ╚═════╝ ╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
        [/bold cyan]
        [bold green]Hệ Thống Công Ty Phần Mềm AI Toàn Năng trên Nền Tảng Antigravity 2.0[/bold green]
        """
        console.print(banner)

        table = Table(title="Danh Sách Lệnh Thao Tác Nhanh (Unified Vibe CLI)", border_style="cyan")
        table.add_column("Lệnh thực thi", style="bold yellow", width=28)
        table.add_column("Mô tả chức năng", style="white")
        table.add_column("Cơ chế bảo vệ / Sub-Team", style="green")

        table.add_row("vibe dev", "Khởi chạy toàn bộ hệ thống phát triển Fullstack", "FastAPI :8000 + Web :3000")
        table.add_row("vibe test", "Kiểm thử tự động 5 tầng 1-chạm (Smoke Test)", "Ruff + Contract + Alembic + Pytest + TS")
        table.add_row("vibe task \"<mô tả>\"", "Làn chạy cao tốc cho Micro-Tasks & Bugfix", "Tactical Fast-Track Squad (Impact Analysis)")
        table.add_row("vibe new \"<tên>\"", "Khởi chạy quy trình phát triển dự án mới", "5 Sub-Teams (15 Agents) qua 3 HITL Gates")
        table.add_row("vibe contract", "Xác thực và đối chiếu Hợp đồng Dữ liệu Đa tầng", "AST Cross-Layer Matching (100% snake_case)")
        table.add_row("vibe heal", "Vá lỗi tự động Heuristic ngoại tuyến (0 Token)", "Secrets, datetime.now, Pydantic v2, CORS")
        table.add_row("vibe fix-env", "Tự động sửa shebang đường dẫn môi trường .venv", "Cross-Platform Relocation Fixer")
        table.add_row("vibe status", "Xem sức khỏe dự án, Checkpoints & Model Tiers", "State Synchronizer & Verification Trail")

        console.print(table)
        console.print("\n[dim]💡 Mẹo: Bạn cũng có thể dùng `make <target>` hoặc `.\\run.ps1 <command>` trên Windows.[/dim]\n")
    else:
        print("========================================================================")
        print("                 AI-VIBE-CODING UNIFIED COMMAND LINE                    ")
        print("========================================================================")
        print("  vibe dev              : Khởi chạy toàn bộ hệ thống Fullstack")
        print("  vibe test             : Kiểm thử tự động 5 tầng 1-chạm (Smoke Test)")
        print("  vibe task \"<mô tả>\"   : Kích hoạt Fast-Track Squad cho micro-task/bugfix")
        print("  vibe new \"<tên>\"      : Khởi chạy quy trình 5 Sub-Teams cho dự án mới")
        print("  vibe contract         : Kiểm tra đối chiếu Hợp đồng Dữ liệu Đa tầng")
        print("  vibe heal             : Tự động vá lỗi Heuristic 0-Token")
        print("  vibe fix-env          : Sửa lỗi shebang đường dẫn .venv")
        print("  vibe status           : Xem sức khỏe dự án & Checkpoints")
        print("========================================================================\n")


def main():
    if len(sys.argv) <= 1 or sys.argv[1].lower() in ["help", "-h", "--help"]:
        show_dashboard()
        return 0

    command = sys.argv[1].lower()
    extra_args = sys.argv[2:]

    if command == "dev":
        return run_script("start_dev.py", extra_args)

    elif command in ["test", "smoke"]:
        return run_script("smoke_test.py", extra_args)

    elif command in ["task", "fast-track", "fix"]:
        if not extra_args:
            print("❌ Vui lòng cung cấp mô tả task. Ví dụ: vibe task \"Sửa validation email trong UserService\"")
            return 1
        # Nếu truyền chuỗi trực tiếp mà không có flag --task
        if not any(a.startswith("--task") for a in extra_args):
            return run_script("fast_track.py", ["--task", extra_args[0]] + extra_args[1:])
        return run_script("fast_track.py", extra_args)

    elif command in ["new", "sdlc", "project"]:
        if not extra_args:
            print("❌ Vui lòng cung cấp tên dự án. Ví dụ: vibe new \"ECommerce_Portal\"")
            return 1
        if not any(a.startswith("--project") for a in extra_args):
            return run_script("runner.py", ["--project", extra_args[0]] + extra_args[1:])
        return run_script("runner.py", extra_args)

    elif command in ["contract", "contracts", "verify-contracts"]:
        return run_script("verify_contracts.py", extra_args)

    elif command in ["heal", "auto-heal"]:
        return run_script("auto_heal_heuristics.py", ["--apply"] + extra_args)

    elif command in ["fix-env", "fix_venv"]:
        return run_script("fix_venv.py", extra_args)

    elif command in ["status", "check"]:
        return run_script("sync_state.py", ["--check-only"] + extra_args)

    elif command in ["sync"]:
        return run_script("sync_state.py", extra_args)

    elif command in ["bundle", "release"]:
        return run_script("bundle_release.py", extra_args)

    else:
        print(f"❌ Không nhận diện được lệnh: '{command}'")
        print("   Gõ 'vibe' hoặc 'vibe help' để xem danh sách các lệnh hỗ trợ.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
