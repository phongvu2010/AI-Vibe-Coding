import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

import os
import json
import re
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from state import SDLCState, SDLCPhase
from agent_factory import AgentFactory
from dag_engine import DAGExecutionEngine
from synthesis_engine import DomainAnalyzer, AdaptiveCodeSynthesizer

console = Console()


async def run_engineering_phase(
    state: SDLCState,
    factory: AgentFactory,
    project_workspace: Path,
    review_feedback: str = ""
) -> SDLCState:
    """Thực thi chuyên sâu Sub-Team 3: Core Engineering kết nối với DAG Execution Engine & SQLAlchemy 2.0."""
    console.print("\n[bold cyan]▶ ĐANG CHẠY CHUYÊN SÂU SUB-TEAM 3: CORE ENGINEERING & IMPLEMENTATION[/bold cyan]")

    project_workspace.mkdir(parents=True, exist_ok=True)
    backend_dir = project_workspace / "backend"
    frontend_dir = project_workspace / "frontend"
    infra_dir = project_workspace / "infra"

    backend_dir.mkdir(parents=True, exist_ok=True)
    frontend_dir.mkdir(parents=True, exist_ok=True)
    infra_dir.mkdir(parents=True, exist_ok=True)

    synthesizer = AdaptiveCodeSynthesizer(project_workspace)

    # 1. Xử lý phản hồi Auto-Healing nếu có feedback từ Reviewer / QA
    if review_feedback:
        console.print(Panel(
            f"[bold yellow]⟳ ĐANG KÍCH HOẠT AUTO-HEALING SỬA ĐỔI MÃ NGUỒN THEO PHẢN HỒI:[/bold yellow]\n{review_feedback}",
            title="[bold red]Auto-Healing Loop In Progress[/bold red]",
            border_style="yellow"
        ))
        from auto_healing import AutoHealingCoordinator, DefectTicket
        target_heal_file = "backend/app/routers/orders.py" if ("order" in review_feedback.lower() or "slot" in review_feedback.lower() or "capacity" in review_feedback.lower()) else "backend/app/core/config.py"
        feedback_defect = DefectTicket(
            id="DEF-HITL-REVISION",
            target_team="backend",
            file_path=target_heal_file,
            severity="HIGH",
            issue_description=review_feedback,
            suggested_fix=f"Cập nhật mã nguồn theo yêu cầu của Reviewer: {review_feedback}"
        )
        coordinator = AutoHealingCoordinator(max_iterations=1)
        await coordinator.execute_healing(feedback_defect, factory, project_workspace)

    # 2. Phân tích DAG Tasks
    tasks_dag_path = Path(state.artifacts.get("tasks_dag", ""))
    tasks_data = []
    if tasks_dag_path.exists():
        try:
            tasks_data = json.loads(tasks_dag_path.read_text(encoding="utf-8"))
        except Exception:
            tasks_data = []

    if tasks_data:
        dag_engine = DAGExecutionEngine(tasks_data)
        waves = dag_engine.get_execution_waves()
        console.print(f"  [bold yellow]• Động cơ DAG phát hiện {len(waves)} Execution Waves cần thực thi:[/bold yellow]")
        role_map = {
            "backend": "backend_engineer",
            "frontend": "frontend_engineer",
            "devops": "devops_engineer"
        }
        for idx, wave in enumerate(waves, start=1):
            wave_tasks_info = []
            for t in wave:
                team_key = str(t.get("team", "backend")).lower()
                sub_role = role_map.get(team_key, "backend_engineer")
                model_id, tier = factory.model_router.get_model_for_team("engineering_team", subagent_role=sub_role)
                wave_tasks_info.append(f"{t.get('id', 'TASK')} [{sub_role}:{tier.upper()}]")
            console.print(f"    [dim]↳ Wave {idx}: {', '.join(wave_tasks_info)}[/dim]")
    else:
        waves = []

    # 3. Phân tích ngữ cảnh domain thích ứng kết hợp cờ platform chỉ định
    target_platform = getattr(state, "platform", "auto")
    domain_info = DomainAnalyzer.analyze(
        state.raw_requirements,
        project_name=state.project_name,
        platform=target_platform
    )

    # =========================================================================
    # WAVE 1 & 2: CORE CONFIG, DATABASE, REPOSITORIES & SERVICES (HYBRID SYNTHESIS)
    # =========================================================================
    be_model, be_tier = factory.model_router.get_model_for_team("engineering_team", subagent_role="backend_engineer")
    console.print(f"  [bold cyan]► Wave 1 & 2: Sinh mã nguồn Clean Architecture Hybrid (SQLAlchemy 2.0 + Deep LLM [{be_model} | {be_tier.upper()}])...[/bold cyan]")
    arch_parts = []
    for key, label in [
        ("architecture_design", "ARCHITECTURE DESIGN"),
        ("openapi_spec", "OPENAPI 3.0.3 SPECIFICATION"),
        ("erd_diagram", "MERMAID ERD SCHEMA")
    ]:
        art_path_str = state.artifacts.get(key, "")
        if art_path_str:
            art_path = Path(art_path_str)
            if art_path.exists():
                try:
                    arch_parts.append(f"=== {label} ===\n{art_path.read_text(encoding='utf-8')}")
                except Exception:
                    pass
    arch_doc = "\n\n".join(arch_parts)

    await synthesizer.synthesize_backend_hybrid(
        domain_info=domain_info,
        raw_requirements=state.raw_requirements,
        architecture_design=arch_doc,
        agent_factory=factory
    )

    # =========================================================================
    # WAVE 3: ROUTERS & FRONTEND (REACT NATIVE MOBILE HOẶC REACT VITE/NEXT.JS WEB)
    # =========================================================================
    fe_model, fe_tier = factory.model_router.get_model_for_team("engineering_team", subagent_role="frontend_engineer")
    target_override = target_platform if target_platform in ("web", "mobile") else None
    fe_target = target_override or domain_info.get("frontend_target", "mobile")
    fe_label = "Web Portal (React Vite / Next.js TypeScript)" if fe_target == "web" else "Mobile App (React Native TypeScript)"
    console.print(f"  [bold cyan]► Wave 3: Thiết lập Routers API & Giao diện {fe_label} [{fe_model} | {fe_tier.upper()}]...[/bold cyan]")
    synthesizer.synthesize_frontend(domain_info, target_override=target_override)

    # =========================================================================
    # WAVE 4: DEVOPS INFRASTRUCTURE (MULTI-STAGE DOCKERFILE & DOCKER-COMPOSE)
    # =========================================================================
    do_model, do_tier = factory.model_router.get_model_for_team("engineering_team", subagent_role="devops_engineer")
    console.print(f"  [bold cyan]► Wave 4: Thiết lập Hạ tầng DevOps Multi-Stage Dockerfile ({fe_label} Nginx + FastAPI + PostgreSQL) [{do_model} | {do_tier.upper()}]...[/bold cyan]")
    synthesizer.synthesize_infra(state.project_name, frontend_target=fe_target)

    # Lưu artifacts
    state.artifacts["backend_source"] = str(backend_dir)
    state.artifacts["frontend_source"] = str(frontend_dir)
    state.artifacts["infra_source"] = str(infra_dir)
    state.current_phase = SDLCPhase.ENGINEERING

    console.print("  [bold green]✓ Sub-Team 3 hoàn thành toàn bộ mã nguồn Clean Architecture theo DAG Waves![/bold green]")
    return state
