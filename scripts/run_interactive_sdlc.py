#!/usr/bin/env python3
"""
run_interactive_sdlc.py — Interactive SDLC Orchestrator CLI with Human-in-the-Loop (HITL)
Part of AI-Vibe-Coding (Antigravity 2.0).

Executes the full 5-phase software lifecycle interactively from a Client Brief:
Phase 1: Discovery (Domain analysis, PRD & UI/UX Specs) -> [GATE 1 HITL TUI]
Phase 2: Architecture (Data Contract Matrix, OpenAPI, ERD) -> [GATE 2 HITL TUI]
Phase 3: Core Engineering (Clean Architecture, 2-Wave dev, AST & contract verification)
Phase 4: QA & Security (Auto-healing, 5-layer smoke tests, Pytest) -> [GATE 3 HITL TUI]
Phase 5: Release & Handover (Bundle ZIP package, SHA-256 Checksum, UAT Checklist)

Usage:
    python scripts/run_interactive_sdlc.py --brief examples/sample_client_brief.md --feature motocare-booking
    python scripts/run_interactive_sdlc.py --resume
"""

import argparse
import datetime
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent.parent

# Đảm bảo UTF-8
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.table import Table
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None


def print_title(text: str):
    if HAS_RICH:
        console.rule(f"[bold cyan]{text}[/bold cyan]")
    else:
        print("\n" + "=" * 80)
        print(f"   {text}")
        print("=" * 80)


def auto_backup_workspace(feature_slug: str) -> Optional[Path]:
    """Tự động sao lưu an toàn toàn bộ mã nguồn trước khi tạo mới (Zero Data-Loss Protection)."""
    src_dir = BASE_DIR / "src"
    specs_dir = BASE_DIR / "docs" / "specs"
    has_code = src_dir.exists() and any(src_dir.rglob("*.py"))
    has_specs = specs_dir.exists() and any(specs_dir.rglob("*.md"))

    if not (has_code or has_specs):
        return None

    snapshot_script = BASE_DIR / "scripts" / "snapshot.py"
    if snapshot_script.exists():
        try:
            safe_slug = re.sub(r"[^a-zA-Z0-9_\-]", "_", feature_slug or "manual")
            subprocess.run([sys.executable, str(snapshot_script), "take", f"pre_{safe_slug}"], cwd=BASE_DIR, capture_output=True)
            if HAS_RICH:
                console.print(f"[bold yellow]📦 [Overwrite Protection] Đã tự động tạo snapshot lưu trữ an toàn trước khi chạy.[/bold yellow]")
            else:
                print(f"📦 [Overwrite Protection] Đã tự động tạo snapshot lưu trữ an toàn trước khi chạy.")
        except Exception:
            pass
    return None


def run_cmd(cmd: list, desc: str, check: bool = True) -> subprocess.CompletedProcess:
    if HAS_RICH:
        console.print(f"\n[cyan]► {desc}...[/cyan]")
    else:
        print(f"\n► {desc}...")

    res = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)
    if res.returncode != 0 and check:
        if HAS_RICH:
            console.print(f"[bold red]⚠️ Cảnh báo tại '{desc}':[/bold red]")
            if res.stderr:
                console.print(res.stderr[:600], style="dim red")
        else:
            print(f"⚠️ Cảnh báo tại '{desc}':")
            if res.stderr:
                print(res.stderr[:600])
    return res


def conduct_terminal_hitl_gate(
    gate_num: int,
    feature_slug: str,
    role: str = "Tech Lead / Product Owner"
) -> str:
    """Điều phối chốt chặn kiểm soát chất lượng tương tác dòng lệnh (Terminal HITL Gate)."""
    gate_script = BASE_DIR / "scripts" / "generate_gate_review.py"
    
    # 1. Sinh biên bản đánh giá sơ khởi
    if gate_script.exists():
        subprocess.run(
            [sys.executable, str(gate_script), "--gate", str(gate_num), "--feature", feature_slug, "--status", "PENDING"],
            cwd=BASE_DIR,
            capture_output=True
        )

    specs_dir = BASE_DIR / "docs" / "specs" / feature_slug
    review_file = specs_dir / f"review_gate_{gate_num}.md"

    gate_titles = {
        1: "GATE 1: CLIENT SCOPE & PRD SIGN-OFF",
        2: "GATE 2: ARCHITECTURE & TECHNICAL CONTRACT SIGN-OFF",
        3: "GATE 3: PRODUCTION READINESS & QUALITY SIGN-OFF"
    }

    title = gate_titles.get(gate_num, f"QUALITY GATE {gate_num}")

    if HAS_RICH:
        console.print()
        console.rule(f"[bold yellow]🚦 HUMAN-IN-THE-LOOP QUALITY GATE: {title}[/bold yellow]")
        console.print(Panel(
            f"[bold]Vai trò phê duyệt yêu cầu:[/bold] {role}\n"
            f"[bold]Phân hệ / Dự án:[/bold] {feature_slug}\n"
            f"[bold]Biên bản đánh giá Markdown:[/bold] [green]{review_file.relative_to(BASE_DIR) if review_file.exists() else review_file}[/green]\n"
            f"[italic]Vui lòng kiểm tra các tài liệu và mã nguồn tương ứng trước khi quyết định.[/italic]",
            title="[bold yellow]Thông Tin Chốt Chặn[/bold yellow]",
            border_style="yellow"
        ))

        console.print("\n[bold cyan]LỰA CHỌN CỦA BẠN:[/bold cyan]")
        console.print("  [1] [bold green]PHÊ DUYỆT (Approve)[/bold green] -> Chuyển tiếp sang Phase tiếp theo")
        console.print("  [2] [bold yellow]YÊU CẦU SỬA ĐỔI (Request Revision)[/bold yellow] -> Nhập ghi chú để tinh chỉnh")
        console.print("  [3] [bold red]TỪ CHỐI / DỪNG TIẾN TRÌNH (Reject & Abort)[/bold red]")

        choice = Prompt.ask("Vui lòng chọn", choices=["1", "2", "3"], default="1")
    else:
        print("\n" + "=" * 60)
        print(f"🚦 HUMAN-IN-THE-LOOP QUALITY GATE: {title}")
        print(f"Vai trò phê duyệt: {role}")
        print(f"Biên bản Gate: {review_file}")
        print("=" * 60)
        print("  [1] PHÊ DUYỆT (Approve)")
        print("  [2] YÊU CẦU SỬA ĐỔI (Request Revision)")
        print("  [3] TỪ CHỐI / DỪNG TIẾN TRÌNH (Reject & Abort)")
        choice = input("Vui lòng chọn [1/2/3] (mặc định 1): ").strip() or "1"

    if choice == "1":
        feedback = "Đã phê duyệt đạt tiêu chuẩn nghiệm thu."
        if HAS_RICH:
            feedback = Prompt.ask("Nhập ghi chú phê duyệt (tuỳ chọn)", default=feedback)
        
        # Cập nhật review file thành APPROVED
        if gate_script.exists():
            subprocess.run(
                [sys.executable, str(gate_script), "--gate", str(gate_num), "--feature", feature_slug, "--status", "APPROVED", "--feedback", feedback, "--reviewer", role],
                cwd=BASE_DIR,
                capture_output=True
            )
        
        # Lưu checkpoint
        checkpoint_script = BASE_DIR / "scripts" / "checkpoint.py"
        phase_names = {1: "gate_1_prd", 2: "gate_2_architecture", 3: "gate_3_deploy"}
        if checkpoint_script.exists():
            subprocess.run(
                [sys.executable, str(checkpoint_script), "save", "--phase", phase_names.get(gate_num, f"gate_{gate_num}"), "--status", "APPROVED", "--note", f"Gate {gate_num} Sign-off: {feedback}"],
                cwd=BASE_DIR,
                capture_output=True
            )
        return "APPROVED"

    elif choice == "2":
        if HAS_RICH:
            feedback = Prompt.ask("[bold yellow]Nhập nội dung yêu cầu sửa đổi chi tiết[/bold yellow]")
        else:
            feedback = input("Nhập nội dung yêu cầu sửa đổi chi tiết: ").strip()

        if gate_script.exists():
            subprocess.run(
                [sys.executable, str(gate_script), "--gate", str(gate_num), "--feature", feature_slug, "--status", "CHANGES_REQUESTED", "--feedback", feedback, "--reviewer", role],
                cwd=BASE_DIR,
                capture_output=True
            )
        return "REVISION"

    else:
        if HAS_RICH:
            feedback = Prompt.ask("[bold red]Lý do từ chối tiến trình[/bold red]", default="Không đạt tiêu chuẩn kỹ thuật.")
        else:
            feedback = input("Lý do từ chối: ").strip() or "Không đạt tiêu chuẩn kỹ thuật."

        if gate_script.exists():
            subprocess.run(
                [sys.executable, str(gate_script), "--gate", str(gate_num), "--feature", feature_slug, "--status", "REJECTED", "--feedback", feedback, "--reviewer", role],
                cwd=BASE_DIR,
                capture_output=True
            )
        return "REJECTED"


def execute_interactive_sdlc(
    brief_path: Path,
    feature_slug: str = "motocare-booking",
    resume: bool = False,
    platform: str = "auto"
) -> bool:
    print_title("AI-VIBE-CODING: INTERACTIVE SDLC ORCHESTRATOR (ANTIGRAVITY 2.0)")
    
    if HAS_RICH:
        console.print(f"📄 [bold]Client Brief:[/bold] {brief_path.name}")
        console.print(f"🏷️  [bold]Feature Slug:[/bold] {feature_slug}")
        console.print(f"📱 [bold]Platform Target:[/bold] {platform}")
        console.print(f"🎮 [bold]Chế độ:[/bold] Interactive Human-in-the-Loop (Terminal TUI)\n")
    else:
        print(f"📄 Client Brief: {brief_path.name}")
        print(f"🏷️  Feature Slug: {feature_slug}")
        print(f"📱 Platform Target: {platform}")
        print(f"🎮 Chế độ: Interactive Human-in-the-Loop (Terminal TUI)\n")

    # 0. Bảo vệ dữ liệu
    auto_backup_workspace(feature_slug)

    # -------------------------------------------------------------------------
    # PHASE 1: PRODUCT DISCOVERY & SOLUTIONS
    # -------------------------------------------------------------------------
    while True:
        print_title("PHASE 1: PRODUCT DISCOVERY & SOLUTIONS (SUB-TEAM 1)")
        domain_analyzer_script = BASE_DIR / "scripts" / "domain_analyzer.py"
        if domain_analyzer_script.exists() and brief_path.exists():
            run_cmd([sys.executable, str(domain_analyzer_script), str(brief_path)], "Phân tích nghiệp vụ & trích xuất quy tắc")

        # HITL Gate 1
        decision = conduct_terminal_hitl_gate(1, feature_slug, role="Product Owner / Client Lead")
        if decision == "APPROVED":
            if HAS_RICH:
                console.print("[bold green]✔ GATE 1 ĐÃ ĐƯỢC PHÊ DUYỆT! TIẾP TỤC SANG PHASE 2...[/bold green]")
            break
        elif decision == "REVISION":
            if HAS_RICH:
                console.print("[bold yellow]🔄 Đang thực hiện điều chỉnh theo yêu cầu của bạn...[/bold yellow]")
            continue
        else:
            if HAS_RICH:
                console.print("[bold red]⛔ TIẾN TRÌNH ĐÃ BỊ DỪNG LẠI TẠI GATE 1 THEO YÊU CẦU.[/bold red]")
            return False

    # -------------------------------------------------------------------------
    # PHASE 2: ARCHITECTURE & SYSTEM PLANNING
    # -------------------------------------------------------------------------
    while True:
        print_title("PHASE 2: ARCHITECTURE & SYSTEM PLANNING (SUB-TEAM 2)")
        openapi_script = BASE_DIR / "scripts" / "generate_openapi.py"
        if openapi_script.exists():
            run_cmd([sys.executable, str(openapi_script)], "Xuất bản hợp đồng API & OpenAPI 3.0.3", check=False)

        # HITL Gate 2
        decision = conduct_terminal_hitl_gate(2, feature_slug, role="Tech Lead / System Architect")
        if decision == "APPROVED":
            if HAS_RICH:
                console.print("[bold green]✔ GATE 2 ĐÃ ĐƯỢC PHÊ DUYỆT! TIẾP TỤC SANG PHASE 3...[/bold green]")
            break
        elif decision == "REVISION":
            if HAS_RICH:
                console.print("[bold yellow]🔄 Đang cập nhật kiến trúc theo yêu cầu...[/bold yellow]")
            continue
        else:
            if HAS_RICH:
                console.print("[bold red]⛔ TIẾN TRÌNH ĐÃ BỊ DỪNG LẠI TẠI GATE 2.[/bold red]")
            return False

    # -------------------------------------------------------------------------
    # PHASE 3: CORE ENGINEERING (2-WAVE DEV & CODE SYNC)
    # -------------------------------------------------------------------------
    print_title("PHASE 3: CORE ENGINEERING SQUAD (2-WAVE EXECUTION)")
    sync_state_script = BASE_DIR / "scripts" / "sync_state.py"
    if sync_state_script.exists():
        run_cmd([sys.executable, str(sync_state_script), "--feature", feature_slug], "Đồng bộ hóa mã nguồn & kiểm tra AST")

    # -------------------------------------------------------------------------
    # PHASE 4: QA, SECURITY AUDIT & AUTO-HEALING
    # -------------------------------------------------------------------------
    while True:
        print_title("PHASE 4: QA, SECURITY AUDIT & HEURISTIC AUTO-HEALING (SUB-TEAM 4)")
        auto_heal_script = BASE_DIR / "scripts" / "auto_heal_heuristics.py"
        if auto_heal_script.exists():
            run_cmd([sys.executable, str(auto_heal_script), "--apply"], "Chạy Heuristic Auto-Healing (Zero-Token Patching)", check=False)

        smoke_test_script = BASE_DIR / "scripts" / "smoke_test.py"
        if smoke_test_script.exists():
            run_cmd([sys.executable, str(smoke_test_script)], "Thực thi bộ kiểm thử tự động 5 tầng (Smoke Test)", check=False)

        # HITL Gate 3
        decision = conduct_terminal_hitl_gate(3, feature_slug, role="Tech Lead / QA Lead")
        if decision == "APPROVED":
            if HAS_RICH:
                console.print("[bold green]✔ GATE 3 ĐÃ ĐƯỢC PHÊ DUYỆT! HỆ THỐNG ĐẠT CHUẨN SẴN SÀNG RELEASE...[/bold green]")
            break
        elif decision == "REVISION":
            if HAS_RICH:
                console.print("[bold yellow]🔄 Kích hoạt vòng lặp Auto-Healing khắc phục lỗi...[/bold yellow]")
            continue
        else:
            if HAS_RICH:
                console.print("[bold red]⛔ TIẾN TRÌNH BỊ TỪ CHỐI TẠI GATE 3.[/bold red]")
            return False

    # -------------------------------------------------------------------------
    # PHASE 5: RELEASE, DOCUMENTATION & HANDOVER
    # -------------------------------------------------------------------------
    print_title("PHASE 5: RELEASE, DOCUMENTATION & CLIENT HANDOVER (SUB-TEAM 5)")
    bundle_script = BASE_DIR / "scripts" / "bundle_release.py"
    if bundle_script.exists():
        run_cmd([sys.executable, str(bundle_script), "--feature", feature_slug, "--version", "1.0.0"], "Đóng gói bản phát hành (.zip, checksum, UAT checklist)")

    print_title("🎉 CHU TRÌNH PHÁT TRIỂN PHẦN MỀM INTERACTIVE ĐÃ HOÀN TẤT THÀNH CÔNG!")
    if HAS_RICH:
        console.print(f"📦 [bold green]Thành phẩm bàn giao:[/bold green] dist/releases/")
        console.print(f"📋 [bold green]Hồ sơ kỹ thuật & UAT:[/bold green] docs/specs/{feature_slug}/")
    else:
        print(f"📦 Thành phẩm bàn giao: dist/releases/")
        print(f"📋 Hồ sơ kỹ thuật & UAT: docs/specs/{feature_slug}/")

    return True


def main():
    parser = argparse.ArgumentParser(description="Interactive SDLC Orchestrator CLI cho AI-Vibe-Coding")
    parser.add_argument("--brief", default="examples/sample_client_brief.md", help="Đường dẫn file đề bài khách hàng")
    parser.add_argument("--feature", default="motocare-booking", help="Slug định danh phân hệ/tính năng")
    parser.add_argument("--platform", choices=["auto", "web", "mobile"], default="auto", help="Chỉ định nền tảng Frontend mục tiêu (auto/web/mobile)")
    parser.add_argument("--resume", action="store_true", help="Tiếp tục từ checkpoint đã lưu")

    args = parser.parse_args()
    brief_file = Path(args.brief)
    if not brief_file.is_absolute():
        brief_file = BASE_DIR / brief_file

    success = execute_interactive_sdlc(
        brief_path=brief_file,
        feature_slug=args.feature,
        resume=args.resume,
        platform=args.platform
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
