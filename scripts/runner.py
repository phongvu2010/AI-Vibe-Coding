#!/usr/bin/env python3
"""
runner.py — End-to-End Async SDLC Multi-Agent Orchestrator
Part of AI-Vibe-Coding (Antigravity 2.0).

Executes the full 5-phase lifecycle connecting LLM AgentFactory with Antigravity 2.0:
Phase 1: Discovery & Solutions (Account Lead, Lead BA, UI/UX Designer) -> [GATE 1 HITL]
Phase 2: Architecture & Planning (System Architect, Security Architect, Tech Planner) -> [GATE 2 HITL]
Phase 3: Core Engineering & 2-Wave dev (Adaptive Code Synthesizer, AST verification)
Phase 4: QA & Security Audit (PyTest, Coverage >= 80%, Alembic Drift, Auto-Healing) -> [GATE 3 HITL]
Phase 5: Release & Client Handover (ZIP Package, SHA-256 Checksum, UAT Checklist, User Manual)

Usage:
    python scripts/runner.py --project "MotoCare_Upgrade" --brief examples/sample_client_brief.md
    python scripts/runner.py --project "MotoCare_Upgrade" --resume
    python scripts/runner.py --project "MotoCare_Upgrade" --backup
"""

import argparse
import asyncio
import os
import re
import sys
from pathlib import Path
from typing import Optional
import yaml

# Đảm bảo UTF-8
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

BASE_DIR = _SCRIPTS_DIR.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from dotenv import load_dotenv
    if (BASE_DIR / ".env").exists():
        load_dotenv(BASE_DIR / ".env")
except ImportError:
    load_dotenv = None

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

try:
    from state import SDLCState, SDLCPhase, GateDecisionStatus
    from hitl import HITLManager
    from agent_factory import AgentFactory
    from persistence import StatePersistence
    from workflows.discovery_phase import run_discovery_phase
    from workflows.architecture_phase import run_architecture_phase
    from workflows.engineering_phase import run_engineering_phase
    from workflows.qa_phase import run_qa_phase
    from workflows.release_phase import run_release_phase
except ImportError:
    from scripts.state import SDLCState, SDLCPhase, GateDecisionStatus
    from scripts.hitl import HITLManager
    from scripts.agent_factory import AgentFactory
    from scripts.persistence import StatePersistence
    from scripts.workflows.discovery_phase import run_discovery_phase
    from scripts.workflows.architecture_phase import run_architecture_phase
    from scripts.workflows.engineering_phase import run_engineering_phase
    from scripts.workflows.qa_phase import run_qa_phase
    from scripts.workflows.release_phase import run_release_phase

console = Console()


class SDLCOrchestrator:
    """Bộ điều phối chu trình phần mềm toàn diện với Google Antigravity SDK & HITL."""

    def __init__(
        self,
        base_dir: Path,
        hitl_enabled: bool = True,
        output_dir: Optional[Path] = None,
        isolated: bool = False
    ):
        self.base_dir = base_dir
        if load_dotenv and (base_dir / ".env").exists():
            load_dotenv(base_dir / ".env")
        self.config_dir = base_dir / "config"
        self.artifacts_dir = base_dir / "workspaces" / "artifacts"
        self.isolated = isolated

        if output_dir:
            self.output_project_dir = Path(output_dir)
        elif isolated:
            self.output_project_dir = base_dir / "workspaces" / "output_project"
        else:
            self.output_project_dir = base_dir / "workspaces" / "output_project"

        self.checkpoints_dir = base_dir / "dist" / "checkpoints"
        
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        self.output_project_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)

        # Đọc cấu hình
        self.tech_profile = self._load_yaml(self.config_dir / "tech_lead_profile.yaml")
        hitl_cfg = self._load_yaml(self.config_dir / "quality_gates.yaml") or self._load_yaml(self.config_dir / "hitl_gates.yaml")
        self.hitl_config = hitl_cfg
        
        env_hitl = os.getenv("HITL_ENABLED", "true").lower() in ("true", "1", "yes")
        final_hitl = hitl_enabled and env_hitl

        self.hitl_manager = HITLManager(self.hitl_config, enabled=final_hitl, artifacts_dir=self.artifacts_dir)
        self.persistence = StatePersistence(self.checkpoints_dir)
        self.factory = AgentFactory(self.base_dir)

    def _load_yaml(self, path: Path) -> dict:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        return {}

    def backup_current_workspace(self, custom_name: Optional[str] = None) -> Optional[Path]:
        """Tự động sao lưu toàn diện cả mã nguồn (output_project & src/) và toàn bộ artifacts trước khi tạo mới (Zero Data-Loss Protection)."""
        backend_dir = self.output_project_dir / "backend"
        frontend_dir = self.output_project_dir / "frontend"
        src_dir = self.base_dir / "src"
        has_src = src_dir.exists() and any(src_dir.rglob("*.py"))
        has_output = (backend_dir.exists() and any(backend_dir.iterdir())) or (frontend_dir.exists() and any(frontend_dir.iterdir()))
        has_artifacts = any(self.artifacts_dir.glob("*/*"))
        if not (has_output or has_artifacts or has_src):
            return None

        readme_path = self.output_project_dir / "README.md"
        prev_name = custom_name or "previous_project"
        if not custom_name and readme_path.exists():
            try:
                first_line = readme_path.read_text(encoding="utf-8").splitlines()[0]
                extracted = re.sub(r"[^a-zA-Z0-9_\-]", "", first_line.replace("#", "").strip())
                if extracted and "WORKSPACE" not in extracted:
                    prev_name = extracted
            except Exception:
                prev_name = "previous_project"

        from datetime import datetime
        import shutil
        import zipfile
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.base_dir / "dist" / "backups" / f"{prev_name}_{ts}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        ws_backups = self.base_dir / "workspaces" / "backups"
        ws_backups.mkdir(parents=True, exist_ok=True)
        backup_zip = ws_backups / f"backup_{prev_name}_{ts}.zip"

        try:
            if has_output:
                shutil.copytree(self.output_project_dir, backup_dir / "output_project", dirs_exist_ok=True)
            if has_src and not self.isolated:
                # Sao lưu phân vùng src nếu đang ở chế độ làm việc chung
                shutil.copytree(src_dir, backup_dir / "src", dirs_exist_ok=True, ignore=shutil.ignore_patterns("node_modules", ".next", "__pycache__"))
            if has_artifacts:
                shutil.copytree(self.artifacts_dir, backup_dir / "artifacts", dirs_exist_ok=True)

            with zipfile.ZipFile(backup_zip, "w", zipfile.ZIP_DEFLATED) as zf:
                for root_p, _, files_p in os.walk(backup_dir):
                    for file_p in files_p:
                        full_p = Path(root_p) / file_p
                        rel_p = full_p.relative_to(backup_dir)
                        zf.write(full_p, rel_p)

            console.print(f"[bold yellow]📦 [Overwrite Protection] Đã tự động sao lưu dự án và artifacts vào:[/bold yellow] [dim]{backup_dir}[/dim] & [cyan]{backup_zip.name}[/cyan]")
            return backup_dir
        except Exception as e:
            console.print(f"[dim yellow]Warning sao lưu output_project & artifacts: {e}[/dim yellow]")
            return None

    def _backup_existing_output_if_needed(self, new_project_name: str):
        """Tự động sao lưu dự án cũ trước khi bắt đầu dự án mới nếu tên khác nhau."""
        readme_path = self.output_project_dir / "README.md"
        prev_name = "previous_project"
        if readme_path.exists():
            try:
                first_line = readme_path.read_text(encoding="utf-8").splitlines()[0]
                extracted = re.sub(r"[^a-zA-Z0-9_\-]", "", first_line.replace("#", "").strip())
                if extracted and "WORKSPACE" not in extracted:
                    prev_name = extracted
            except Exception:
                prev_name = "previous_project"

        if prev_name.lower().replace("_", "") == new_project_name.lower().replace("_", ""):
            return

        self.backup_current_workspace(custom_name=prev_name)

    async def execute_lifecycle(
        self,
        project_name: str,
        raw_requirements: str,
        resume: bool = False,
        platform: str = "auto"
    ) -> SDLCState:
        if not resume:
            self._backup_existing_output_if_needed(project_name)
        platform_label = {
            "web": "Web Portal (React Vite / Next.js)",
            "mobile": "Mobile App (React Native Expo)",
            "auto": "Tự động phát hiện qua Brief (Auto-detect)"
        }.get(platform.lower(), platform.upper())

        console.print(Panel(
            f"[bold green]KHỞI ĐỘNG HỆ THỐNG AI-VIBE-CODING MULTI-AGENTS SDLC[/bold green]\n"
            f"[bold]Dự án:[/bold] {project_name}\n"
            f"[bold]Nền tảng Frontend:[/bold] {platform_label}\n"
            f"[bold]Tech Lead Stack:[/bold] Python/FastAPI + Next.js / React Native Expo\n"
            f"[bold]Phân bổ Mô hình AI:[/bold] Dynamic Cost Routing (Pro / Flash / Flash-Lite)\n"
            f"[bold]Lộ trình:[/bold] 5 Pha phát triển hoàn chỉnh (DAG Engine, Auto-Healing, Release Bundler)\n"
            f"[bold]Chế độ:[/bold] {'Khôi phục phiên làm việc (Resume)' if resume else 'Khởi tạo mới'}",
            title="[bold cyan]Google Antigravity SDK Orchestrator[/bold cyan]",
            border_style="cyan"
        ))

        state: SDLCState
        if resume:
            loaded_state = self.persistence.load_checkpoint(project_name)
            if loaded_state:
                state = loaded_state
                if platform != "auto":
                    state.platform = platform
            else:
                console.print(f"[bold yellow]Không tìm thấy checkpoint cho '{project_name}'. Khởi tạo mới.[/bold yellow]")
                state = SDLCState(
                    project_name=project_name,
                    raw_requirements=raw_requirements,
                    tech_lead_profile=self.tech_profile,
                    platform=platform
                )
        else:
            state = SDLCState(
                project_name=project_name,
                raw_requirements=raw_requirements,
                tech_lead_profile=self.tech_profile,
                platform=platform
            )

        # =========================================================================
        # GIAI ĐOẠN 1: DISCOVERY & GATE 1 (PRD APPROVAL)
        # =========================================================================
        if state.current_phase in (SDLCPhase.INITIALIZATION, SDLCPhase.DISCOVERY, SDLCPhase.GATE_1_PRD):
            p1_start = datetime.now()
            revision_feedback_gate1 = ""
            while True:
                state = await run_discovery_phase(
                    state=state,
                    factory=self.factory,
                    output_dir=self.artifacts_dir,
                    revision_feedback=revision_feedback_gate1
                )

                gate_decision = self.hitl_manager.conduct_gate_review(
                    gate_key="gate_1_prd",
                    artifacts_paths=[
                        state.artifacts["PRD"],
                        state.artifacts["clarification_qna"],
                        state.artifacts["user_stories"],
                        state.artifacts.get("ui_ux_specs", "")
                    ],
                    state_summary=f"Dự án: {project_name} | Đã bóc tách yêu cầu, PRD chuẩn SMART, User Stories (Gherkin) và UI/UX Flow."
                )
                state.gate_decisions["gate_1_prd"] = gate_decision
                self.persistence.save_checkpoint(state)

                if gate_decision.status == GateDecisionStatus.APPROVED:
                    console.print("[bold green]✓ GATE 1 APPROVED: Chấp thuận PRD. Tiếp tục sang giai đoạn Kiến trúc.[/bold green]")
                    break
                elif gate_decision.status == GateDecisionStatus.REVISION_REQUESTED:
                    console.print(f"[bold yellow]⟳ GATE 1 REVISION REQUESTED: {gate_decision.feedback}[/bold yellow]")
                    revision_feedback_gate1 = gate_decision.feedback or ""
                else:
                    console.print("[bold red]✗ GATE 1 REJECTED: Quy trình bị dừng theo yêu cầu của Reviewer.[/bold red]")
                    state.current_phase = SDLCPhase.FAILED
                    self.persistence.save_checkpoint(state)
                    return state

            p1_duration = (datetime.now() - p1_start).total_seconds()
            state.phase_timings["Phase 1: Discovery & Solutions"] = {
                "started_at": p1_start.isoformat(),
                "completed_at": datetime.now().isoformat(),
                "duration_seconds": round(p1_duration, 2),
                "subteam": "Sub-Team 1 (account-lead + lead-ba + uiux-designer)"
            }

        # =========================================================================
        # GIAI ĐOẠN 2: ARCHITECTURE & GATE 2 (ARCHITECTURE & API SIGN-OFF)
        # =========================================================================
        if state.current_phase in (SDLCPhase.GATE_1_PRD, SDLCPhase.ARCHITECTURE, SDLCPhase.GATE_2_ARCHITECTURE):
            p2_start = datetime.now()
            revision_feedback_gate2 = ""
            while True:
                state = await run_architecture_phase(
                    state=state,
                    factory=self.factory,
                    output_dir=self.artifacts_dir,
                    revision_feedback=revision_feedback_gate2
                )

                gate_decision = self.hitl_manager.conduct_gate_review(
                    gate_key="gate_2_architecture",
                    artifacts_paths=[
                        state.artifacts["architecture_design"],
                        state.artifacts["openapi"],
                        state.artifacts["erd"],
                        state.artifacts.get("security_architecture", ""),
                        state.artifacts["tasks_dag"]
                    ],
                    state_summary=(
                        f"Tech Stack đề xuất: {state.selected_tech_stack.get('backend_framework')} & "
                        f"{state.selected_tech_stack.get('frontend_mobile')}\n"
                        f"Bảo mật: STRIDE Threat Model & Ma trận RBAC.\n"
                        f"Đã ưu tiên theo sở trường review của Tech Lead."
                    )
                )
                state.gate_decisions["gate_2_architecture"] = gate_decision
                self.persistence.save_checkpoint(state)

                if gate_decision.status == GateDecisionStatus.APPROVED:
                    console.print("[bold green]✓ GATE 2 APPROVED: Chấp thuận Kiến trúc & API Contract. Bắt đầu viết mã nguồn.[/bold green]")
                    break
                elif gate_decision.status == GateDecisionStatus.REVISION_REQUESTED:
                    console.print(f"[bold yellow]⟳ GATE 2 REVISION REQUESTED: {gate_decision.feedback}[/bold yellow]")
                    revision_feedback_gate2 = gate_decision.feedback or ""
                else:
                    console.print("[bold red]✗ GATE 2 REJECTED: Dừng dự án ở khâu Kiến trúc.[/bold red]")
                    state.current_phase = SDLCPhase.FAILED
                    self.persistence.save_checkpoint(state)
                    return state

            p2_duration = (datetime.now() - p2_start).total_seconds()
            state.phase_timings["Phase 2: Architecture & Planning"] = {
                "started_at": p2_start.isoformat(),
                "completed_at": datetime.now().isoformat(),
                "duration_seconds": round(p2_duration, 2),
                "subteam": "Sub-Team 2 (system-architect + security-architect + tech-planner)"
            }

        # =========================================================================
        # GIAI ĐOẠN 3: CORE ENGINEERING & QA FEEDBACK (AUTO-HEALING LOOP)
        # =========================================================================
        if state.current_phase in (SDLCPhase.GATE_2_ARCHITECTURE, SDLCPhase.ENGINEERING, SDLCPhase.QA_VERIFICATION, SDLCPhase.GATE_3_DEPLOY):
            p3_start = datetime.now()
            state = await run_engineering_phase(
                state=state,
                factory=self.factory,
                project_workspace=self.output_project_dir
            )
            self.persistence.save_checkpoint(state)
            p3_duration = (datetime.now() - p3_start).total_seconds()
            state.phase_timings["Phase 3: Core Engineering"] = {
                "started_at": p3_start.isoformat(),
                "completed_at": datetime.now().isoformat(),
                "duration_seconds": round(p3_duration, 2),
                "subteam": "Sub-Team 3 (db-dev + frontend-dev + backend-dev + devops-engineer)"
            }

            p4_start = datetime.now()
            while True:
                state = await run_qa_phase(
                    state=state,
                    factory=self.factory,
                    output_dir=self.artifacts_dir
                )

                gate_decision = self.hitl_manager.conduct_gate_review(
                    gate_key="gate_3_deploy",
                    artifacts_paths=[
                        state.artifacts["code_review_report"],
                        state.artifacts["test_summary"],
                        state.artifacts["security_audit_report"]
                    ],
                    state_summary="Tất cả test suite và kiểm tra an toàn bảo mật đã hoàn tất. Yêu cầu cấp phép Deploy & Bàn giao."
                )
                state.gate_decisions["gate_3_deploy"] = gate_decision
                self.persistence.save_checkpoint(state)

                if gate_decision.status == GateDecisionStatus.APPROVED:
                    console.print("[bold green]✓ GATE 3 APPROVED: Cấp phép triển khai & bàn giao chính thức cho khách hàng.[/bold green]")
                    break
                elif gate_decision.status == GateDecisionStatus.REVISION_REQUESTED:
                    console.print(f"[bold yellow]⟳ GATE 3 REVISION REQUESTED (Auto-healing): {gate_decision.feedback}[/bold yellow]")
                    state = await run_engineering_phase(
                        state=state,
                        factory=self.factory,
                        project_workspace=self.output_project_dir,
                        review_feedback=gate_decision.feedback or ""
                    )
                else:
                    console.print("[bold red]✗ GATE 3 REJECTED: Từ chối deploy sản phẩm.[/bold red]")
                    state.current_phase = SDLCPhase.FAILED
                    self.persistence.save_checkpoint(state)
                    return state

            p4_duration = (datetime.now() - p4_start).total_seconds()
            state.phase_timings["Phase 4: QA & Security Audit"] = {
                "started_at": p4_start.isoformat(),
                "completed_at": datetime.now().isoformat(),
                "duration_seconds": round(p4_duration, 2),
                "subteam": "Sub-Team 4 (qa-tester + code-reviewer)"
            }

        # =========================================================================
        # GIAI ĐOẠN 4: RELEASE, DOCUMENTATION & CLIENT HANDOVER AUTOMATION
        # =========================================================================
        p5_start = datetime.now()
        state = await run_release_phase(
            state=state,
            factory=self.factory,
            output_dir=self.artifacts_dir,
            project_workspace=self.output_project_dir
        )
        self.persistence.save_checkpoint(state)
        p5_duration = (datetime.now() - p5_start).total_seconds()
        state.phase_timings["Phase 5: Release & Handover"] = {
            "started_at": p5_start.isoformat(),
            "completed_at": datetime.now().isoformat(),
            "duration_seconds": round(p5_duration, 2),
            "subteam": "Sub-Team 5 (release-engineer + tech-writer + handover-lead)"
        }

        # Hoàn tất
        self._print_final_summary(state)
        return state

    def _print_final_summary(self, state: SDLCState):
        console.print()
        console.rule("[bold green]TỔNG KẾT BÀN GIAO THÀNH PHẨM (SDLC COMPLETED)[/bold green]")

        table = Table(title="Danh Sách Sản Phẩm Đã Bàn Giao", border_style="green")
        table.add_column("Hạng Mục", style="cyan")
        table.add_column("Vị Trí File / Thư Mục", style="white")

        for key, path in state.artifacts.items():
            table.add_row(key, path)

        console.print(table)

        # Bảng đo lường hiệu năng & thời gian thực thi (Telemetry Metrics)
        if state.phase_timings:
            timing_table = Table(title="Chỉ Số Hiệu Năng Thực Thi (Phase Execution Telemetry & Timers)", border_style="yellow")
            timing_table.add_column("Giai Đoạn SDLC", style="cyan")
            timing_table.add_column("Sub-Team Phụ Trách", style="magenta")
            timing_table.add_column("Thời Gian (giây)", justify="right", style="green")

            total_seconds = 0.0
            for phase_name, p_data in state.phase_timings.items():
                dur = p_data.get("duration_seconds", 0.0)
                total_seconds += dur
                timing_table.add_row(phase_name, p_data.get("subteam", "N/A"), f"{dur:.2f}s")
            timing_table.add_row("[bold]TỔNG THỜI GIAN VẬN HÀNH[/bold]", "[bold]Toàn bộ 5 Sub-Teams[/bold]", f"[bold green]{total_seconds:.2f}s[/bold green]")
            console.print(timing_table)

        console.print(Panel(
            "[bold green]✔ Dự án đã được chuyển giao thành công qua cả 5 Giai đoạn lộ trình![/bold green]\n"
            "• Gói phân phối ZIP: [bold]workspaces/artifacts/05_handover/[/bold] hoặc [bold]dist/releases/[/bold]\n"
            "• Bảng nghiệm thu UAT: [bold]UAT_CHECKLIST.md[/bold]\n"
            f"• Mã nguồn đã kiểm thử: [bold]{self.output_project_dir}[/bold]",
            title="[bold yellow]Hoàn Thành Toàn Diện[/bold yellow]",
            border_style="green"
        ))


def main():
    parser = argparse.ArgumentParser(description="AI-Vibe-Coding SDLC Multi-Agent Orchestrator")
    parser.add_argument("--project", default="MotoCare_SmartApp", help="Tên dự án phần mềm")
    parser.add_argument("-f", "--brief", "--input-file", dest="input_file", help="Đường dẫn file chứa yêu cầu thô từ khách hàng (.txt hoặc .md)")
    parser.add_argument("--requirements", help="Chuỗi văn bản yêu cầu thô truyền trực tiếp qua dòng lệnh")
    parser.add_argument("--resume", action="store_true", help="Khôi phục phiên làm việc từ Checkpoint gần nhất")
    parser.add_argument("--no-hitl", action="store_true", help="Tự động bypass các cổng HITL (Dành cho CI/CD test)")
    parser.add_argument("--backup", action="store_true", help="Sao lưu snapshot toàn diện output_project và artifacts hiện tại")
    parser.add_argument("--isolated", action="store_true", help="Chạy ở chế độ Greenfield độc lập trong workspaces/output_project/ (không sửa trực tiếp src/)")
    parser.add_argument("--workspace", help="Chỉ định thư mục workspace đích tùy chỉnh")
    parser.add_argument(
        "--platform",
        choices=["auto", "web", "mobile"],
        default="auto",
        help="Chỉ định nền tảng Frontend mục tiêu (auto: tự nhận diện qua Brief, web: React Vite/Next.js Web Portal, mobile: React Native Expo)"
    )
    args = parser.parse_args()

    orchestrator = SDLCOrchestrator(
        base_dir=BASE_DIR,
        hitl_enabled=not args.no_hitl,
        output_dir=Path(args.workspace) if args.workspace else None,
        isolated=args.isolated
    )

    if args.backup:
        backup_path = orchestrator.backup_current_workspace(custom_name=args.project)
        if backup_path:
            console.print(f"[bold green]✔ Đã tạo bản sao lưu snapshot thành công tại:[/bold green] [white]{backup_path}[/white]")
        else:
            console.print("[dim yellow]ℹ️  Không có mã nguồn hoặc artifacts nào cần sao lưu (thư mục đang trống).[/dim yellow]")
        return

    raw_req = ""
    if args.input_file:
        input_path = Path(args.input_file)
        if not input_path.is_absolute():
            input_path = BASE_DIR / input_path
        if input_path.exists():
            raw_req = input_path.read_text(encoding="utf-8")
            console.print(f"[bold cyan]Đã nạp yêu cầu thô từ file:[/bold cyan] {input_path}")
        else:
            console.print(f"[bold red]Lỗi: Không tìm thấy file {input_path}[/bold red]")
            sys.exit(1)
    elif args.requirements:
        raw_req = args.requirements
    else:
        sample_path = BASE_DIR / "examples" / "sample_client_brief.md"
        if sample_path.exists():
            raw_req = sample_path.read_text(encoding="utf-8")
        else:
            raw_req = "Dự án đặt lịch dịch vụ thông minh với quản trị viên và khách hàng."

    asyncio.run(orchestrator.execute_lifecycle(
        project_name=args.project,
        raw_requirements=raw_req,
        resume=args.resume,
        platform=args.platform
    ))


if __name__ == "__main__":
    main()
