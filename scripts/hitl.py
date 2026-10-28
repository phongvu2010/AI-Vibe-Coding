"""
hitl.py — Human-in-the-Loop (HITL) Quality Gate & Review Manager
Part of AI-Vibe-Coding (Antigravity 2.0).
"""

import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

try:
    from state import GateDecision, GateDecisionStatus
except ImportError:
    from scripts.state import GateDecision, GateDecisionStatus

console = Console()


class HITLManager:
    """Quản lý các điểm chốt chặn Human-in-the-Loop (HITL) tích hợp Antigravity 2.0 Artifacts."""

    def __init__(self, hitl_config: Dict[str, Any], enabled: bool = True, artifacts_dir: Optional[Path] = None):
        self.config = hitl_config.get("hitl_gates", {}) or hitl_config.get("quality_gates", {})
        self.enabled = enabled
        self.artifacts_dir = artifacts_dir or Path("workspaces/artifacts")

    def _generate_interactive_artifact(
        self,
        gate_key: str,
        gate_name: str,
        role: str,
        desc: str,
        artifacts_paths: List[str],
        state_summary: str,
        decision: Optional[GateDecision] = None
    ) -> Path:
        """Sinh tài liệu Markdown Review tương tác để hiển thị trực quan trên Antigravity IDE."""
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        review_doc_path = self.artifacts_dir / f"review_{gate_key}.md"

        artifact_rows = []
        for idx, path_str in enumerate(artifacts_paths, 1):
            p = Path(path_str)
            exists = p.exists()
            status_icon = "✅ Sẵn sàng" if exists else "❌ Chưa tìm thấy"
            size_str = f"{p.stat().st_size:,} bytes" if exists else "N/A"
            abs_url = f"file://{p.resolve()}"
            artifact_rows.append(f"| {idx} | [{p.name}]({abs_url}) | `{p}` | {size_str} | {status_icon} |")

        table_md = "\n".join(artifact_rows)
        decision_status_md = ""
        if decision:
            decision_status_md = f"""
---

## 📋 KẾT QUẢ PHÊ DUYỆT (DECISION LOG)
- **Trạng thái:** **{decision.status.value.upper()}**
- **Người ký duyệt:** `{decision.reviewer}`
- **Thời gian:** `{decision.timestamp}`
- **Ghi chú / Feedback:**
> {decision.feedback}
"""

        content = f"""# 🚦 CHỐT CHẶN KIỂM SOÁT CHẤT LƯỢNG: {gate_name.upper()}
> [!IMPORTANT]
> **Vai trò người phê duyệt yêu cầu:** `{role}`  
> **Mục tiêu chốt chặn:** {desc}

{state_summary}

---

## 📂 DANH SÁCH ARTIFACTS CẦN THẨM ĐỊNH

| STT | Tập Tin / Tài Liệu | Đường Dẫn Tuyệt Đối | Dung Lượng | Trạng Thái |
|---|---|---|---|---|
{table_md}

---

## 🎯 TIÊU CHÍ NGHIỆM THU (GATE EXIT CRITERIA)
- [x] Tài liệu tuân thủ chuẩn cấu trúc và phân tầng Clean Architecture.
- [x] Không vi phạm Security Guardrails (Zero Hardcoded Secrets).
- [x] Tương thích tối đa với năng lực review của Tech Lead (FastAPI, Next.js, React Native).

{decision_status_md}
"""
        review_doc_path.write_text(content, encoding="utf-8")
        return review_doc_path

    GATE_ALIASES = {
        "gate_1_prd": ["gate_1_prd", "gate_1_client_signoff", "gate_1_prd_approval"],
        "gate_1_client_signoff": ["gate_1_client_signoff", "gate_1_prd", "gate_1_prd_approval"],
        "gate_2_architecture": ["gate_2_architecture", "gate_2_architecture_signoff"],
        "gate_2_architecture_signoff": ["gate_2_architecture_signoff", "gate_2_architecture"],
        "gate_3_deploy": ["gate_3_deploy", "gate_3_production_readiness", "gate_3_deploy_signoff"],
        "gate_3_production_readiness": ["gate_3_production_readiness", "gate_3_deploy", "gate_3_deploy_signoff"],
    }

    def conduct_gate_review(
        self,
        gate_key: str,
        artifacts_paths: List[str],
        state_summary: str = ""
    ) -> GateDecision:
        gate_info = None
        aliases = self.GATE_ALIASES.get(gate_key, [gate_key])
        for alias in aliases:
            if alias in self.config:
                gate_info = self.config[alias]
                break

        if not gate_info:
            gate_info = {
                "name": gate_key,
                "role_required": "Tech Lead / Human Reviewer",
                "description": "Review artifacts before proceeding."
            }

        gate_name = gate_info.get("name", gate_key)
        role = gate_info.get("role_required", gate_info.get("approver", "Tech Lead"))
        desc = gate_info.get("description", "")

        # 1. Sinh file artifact review cho Antigravity 2.0 IDE
        review_doc = self._generate_interactive_artifact(
            gate_key=gate_key,
            gate_name=gate_name,
            role=role,
            desc=desc,
            artifacts_paths=artifacts_paths,
            state_summary=state_summary
        )

        console.print()
        console.rule(f"[bold yellow]HUMAN-IN-THE-LOOP QUALITY GATE: {gate_name}[/bold yellow]")

        table = Table(title="Danh sách Artifacts cần Phê duyệt", border_style="cyan")
        table.add_column("STT", justify="center", style="cyan")
        table.add_column("Loại Tài Liệu / File", style="white")
        table.add_column("Đường Dẫn Thực Tế", style="green")
        table.add_column("Trạng Thái Tồn Tại", justify="center")

        for idx, path_str in enumerate(artifacts_paths, 1):
            p = Path(path_str)
            exists = "[bold green]✓ Sẵn sàng[/bold green]" if p.exists() else "[bold red]✗ Chưa thấy[/bold red]"
            table.add_row(str(idx), p.name, str(p), exists)

        console.print(Panel(
            f"[bold]Vai trò người phê duyệt:[/bold] {role}\n"
            f"[italic]{desc}[/italic]\n\n"
            f"[bold cyan]Artifact Review Markdown:[/bold cyan] {review_doc}\n\n"
            f"{state_summary}",
            title="[bold yellow]Thông Tin Gate[/bold yellow]",
            border_style="yellow"
        ))
        console.print(table)

        if not self.enabled:
            console.print("[bold green][AUTO-BYPASS] Chế độ HITL_ENABLED=false: Tự động phê duyệt chốt chặn.[/bold green]")
            decision = GateDecision(
                gate_id=gate_key,
                reviewer=f"Automated System ({role})",
                status=GateDecisionStatus.APPROVED,
                feedback="Auto-approved via non-interactive mode."
            )
            self._generate_interactive_artifact(gate_key, gate_name, role, desc, artifacts_paths, state_summary, decision)
            return decision

        while True:
            console.print("\n[bold cyan]LỰA CHỌN CỦA BẠN (Tech Lead / Reviewer):[/bold cyan]")
            console.print("  [1] [bold green]PHÊ DUYỆT (Approve)[/bold green] -> Chuyển tiếp sang Sub-Team tiếp theo")
            console.print("  [2] [bold yellow]YÊU CẦU SỬA ĐỔI (Request Revision)[/bold yellow] -> Nhập phản hồi để AI Auto-Healing sửa lại")
            console.print("  [3] [bold red]TỪ CHỐI / DỪNG DỰ ÁN (Reject & Abort)[/bold red]")
            console.print("  [p] [bold magenta]XEM TRỰC TIẾP ARTIFACTS (Terminal Preview)[/bold magenta] -> Đọc nhanh nội dung tài liệu")

            choice = Prompt.ask("Vui lòng chọn", choices=["1", "2", "3", "p", "P"], default="1").lower()

            if choice == "p":
                console.print("\n" + "=" * 70)
                console.print(f"[bold magenta]📖 PREVIEW ARTIFACTS CỦA CHỐT CHẶN: {gate_name}[/bold magenta]")
                console.print("=" * 70)
                from rich.markdown import Markdown
                found_any = False
                for p_str in artifacts_paths:
                    p = Path(p_str)
                    if p.exists() and p.is_file() and p.suffix in (".md", ".json", ".yaml", ".yml"):
                        found_any = True
                        content = p.read_text(encoding="utf-8", errors="ignore")
                        preview_text = content[:1500] + ("\n... [Đã cắt bớt để tối ưu hiển thị terminal]" if len(content) > 1500 else "")
                        if p.suffix == ".md":
                            console.print(Panel(Markdown(preview_text), title=f"[cyan]{p.name}[/cyan]", border_style="cyan"))
                        else:
                            console.print(Panel(preview_text, title=f"[cyan]{p.name}[/cyan]", border_style="cyan"))
                if not found_any:
                    console.print("[yellow]Chưa có file artifact văn bản nào sẵn sàng để preview.[/yellow]")
                continue

            if choice == "1":
                feedback = Prompt.ask("Nhập ghi chú phê duyệt (nếu có)", default="Đã phê duyệt, đạt tiêu chuẩn kỹ thuật.")
                decision = GateDecision(
                    gate_id=gate_key,
                    reviewer=role,
                    status=GateDecisionStatus.APPROVED,
                    feedback=feedback
                )
                break
            elif choice == "2":
                feedback = Prompt.ask("[bold yellow]Nhập nội dung yêu cầu sửa đổi chi tiết cho AI[/bold yellow]")
                decision = GateDecision(
                    gate_id=gate_key,
                    reviewer=role,
                    status=GateDecisionStatus.REVISION_REQUESTED,
                    feedback=feedback
                )
                break
            else:
                feedback = Prompt.ask("[bold red]Lý do từ chối dự án[/bold red]", default="Dự án không đạt tiêu chuẩn kỹ thuật.")
                decision = GateDecision(
                    gate_id=gate_key,
                    reviewer=role,
                    status=GateDecisionStatus.REJECTED,
                    feedback=feedback
                )
                break

        # Cập nhật kết quả quyết định vào artifact markdown
        self._generate_interactive_artifact(gate_key, gate_name, role, desc, artifacts_paths, state_summary, decision)
        return decision


def main(argv=None):
    import argparse
    import yaml

    parser = argparse.ArgumentParser(description="Human-in-the-Loop Quality Gate Reviewer for AI-Vibe-Coding")
    parser.add_argument("--gate", choices=["gate_1_prd", "gate_2_architecture", "gate_3_deploy", "1", "2", "3"], default="gate_1_prd", help="Gate ID to review")
    parser.add_argument("--feature", default="motocare-booking", help="Feature slug to review")
    parser.add_argument("--auto-bypass", action="store_true", help="Bypass interactive prompt")
    args = parser.parse_args(argv)

    gate_map = {"1": "gate_1_prd", "2": "gate_2_architecture", "3": "gate_3_deploy"}
    gate_key = gate_map.get(args.gate, args.gate)

    config_path = Path("config/hitl_gates.yaml")
    config = {}
    if config_path.exists():
        with open(config_path, encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

    manager = HITLManager(config, enabled=not args.auto_bypass)
    sample_artifacts = [
        f"docs/specs/{args.feature}/prd.md",
        f"docs/specs/{args.feature}/plan.md",
        f"docs/specs/{args.feature}/test-report.md",
    ]
    decision = manager.conduct_gate_review(gate_key, sample_artifacts, f"Review requested for feature: {args.feature}")
    console.print(f"[bold green]✔ Kết quả phê duyệt:[/bold green] {decision.status.value}")


if __name__ == "__main__":
    main()
