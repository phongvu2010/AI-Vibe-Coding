#!/usr/bin/env python3
"""
auto_healing.py — Điều Phối Vòng Lặp Tự Sửa Lỗi Có Cấu Trúc (Auto-Healing Coordinator)
Thuộc hệ thống AI-Vibe-Coding (Antigravity 2.0).

Chức năng:
1. Tiếp nhận DefectTicket có cấu trúc từ QA Tester hoặc Tech Lead Review Gate.
2. Kết hợp 2 tầng xử lý bản vá:
   - Tầng 1: Heuristic Rule-Based Patcher (Zero Token, cực nhanh qua `auto_heal_heuristics.py`).
   - Tầng 2: LLM-Powered Targeted Patcher (Gọi Agent tái tạo bản vá thích ứng cho mã nguồn).
3. Tự động kiểm thử lại sau mỗi lần áp bản vá, tối đa 3 vòng lặp (Circuit Breaker).
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    console = Console()
except ImportError:
    class DummyConsole:
        def print(self, *args, **kwargs):
            clean = [re.sub(r"\[.*?\]", "", str(a)) for a in args]
            print(*clean)
    console = DummyConsole()
    class DummyPanel:
        def __init__(self, content, title="", border_style=""):
            self.content = content
            self.title = title
        def __str__(self):
            return f"=== {self.title} ===\n{self.content}\n"
    Panel = DummyPanel

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "scripts"))

from schemas import DefectTicket, QAEvaluationResult
try:
    from auto_heal_heuristics import HeuristicAutoPatcher
except ImportError:
    HeuristicAutoPatcher = None


class AutoHealingCoordinator:
    """Điều phối vòng lặp tự động sửa lỗi (Auto-Healing Loop) giữa QA và Dev Squads."""

    def __init__(self, max_iterations: int = 3):
        self.max_iterations = max_iterations
        self.heuristic_patcher = HeuristicAutoPatcher(ROOT_DIR) if HeuristicAutoPatcher else None

    def format_fix_prompt_for_dev(self, defect: DefectTicket, file_content: str) -> str:
        """Đóng gói defect ticket kèm stack trace và mã nguồn thành prompt cho Dev Agent."""
        critical_notice = ""
        if getattr(defect, "severity", "").upper() == "CRITICAL":
            critical_notice = "\n🚨 CẢNH BÁO MỨC ĐỘ CRITICAL: Lỗi này là Blocker bảo mật hoặc rủi ro nghiêm trọng. Bắt buộc xử lý ngay lập tức (nạp biến bí mật vào .env, vá SQL Injection hoặc khắc phục Auth/RBAC)!\n"

        return f"""BẠN LÀ SENIOR ENGINEER THUỘC DEV SQUAD ({defect.target_team.upper()}).
Hệ thống kiểm thử tự động (PyTest / Security Audit) vừa phát hiện lỗi trong file: `{defect.file_path}`.{critical_notice}

🚨 THÔNG TIN DEFECT TICKET:
- Mã lỗi: {defect.id}
- Mức độ nghiêm trọng: {defect.severity}
- Phân đội phụ trách: {defect.target_team.upper()}
- Gợi ý khắc phục: {defect.suggested_fix}

💥 CHI TIẾT LỖI & STACK TRACE TỪ TEST RUNNER:
--------------------------------------------------------------------------------
{defect.stack_trace or defect.issue_description}
--------------------------------------------------------------------------------

📜 MÃ NGUỒN HIỆN TẠI CỦA FILE `{defect.file_path}`:
```python
{file_content}
```

NHIỆM VỤ CỦA BẠN:
1. Đọc và phân tích kỹ stack trace để xác định chính xác dòng bị lỗi hoặc điều kiện assertion thất bại.
2. Viết lại TOÀN BỘ file `{defect.file_path}` đã sửa lỗi, tuân thủ Clean Architecture, Pydantic v2, SQLAlchemy 2.0 và casing `snake_case`.
3. Chỉ trả về mã nguồn hoàn chỉnh đã sửa trong một khối mã Markdown duy nhất dạng:
```python
# Toàn bộ mã nguồn hoàn chỉnh của file
```
Không đưa ra giải thích dài dòng bên ngoài khối mã Markdown để hệ thống có thể tự động áp bản vá.
"""

    async def execute_healing(
        self,
        defect: DefectTicket,
        agent_factory: Any,
        workspace_dir: Path
    ) -> bool:
        """Thực thi sửa lỗi: ưu tiên Heuristic Patcher -> fallback sang LLM Agent."""
        target_file = workspace_dir / defect.file_path
        if not target_file.exists():
            console.print(f"  [bold red]✗ Không tìm thấy file {target_file} để Auto-Healing.[/bold red]")
            return False

        original_content = target_file.read_text(encoding="utf-8")
        patched_code: Optional[str] = None

        # 1. Thử Heuristic Patcher trước (Zero Token, siêu tốc < 50ms)
        if self.heuristic_patcher:
            try:
                candidate, patched = self.heuristic_patcher.patch_file_content(original_content, defect.file_path)
                if patched:
                    patched_code = candidate
                    console.print(f"  [bold green]✓ Heuristic Patcher đã tự động vá lỗi theo quy tắc tiền định![/bold green]")
            except Exception as e:
                console.print(f"  [dim yellow]Heuristic patcher warning: {e}[/dim yellow]")

        # 2. Thử gọi LLM Agent nếu Heuristic chưa giải quyết được
        if not patched_code and agent_factory:
            try:
                console.print(f"  [bold yellow]⟳ Đang gửi Defect {defect.id} tới Dev Squad ({defect.target_team})...[/bold yellow]")
                prompt = self.format_fix_prompt_for_dev(defect, original_content)
                agent = agent_factory.create_engineering_team(workspace_dir=workspace_dir)
                async with agent:
                    resp = await agent.chat(prompt)
                    resp_text = await resp.text()

                code_match = re.search(r"```(?:python|typescript|tsx)?\s*\n(.*?)\n```", resp_text, re.DOTALL)
                if code_match:
                    candidate_code = code_match.group(1).strip()
                    if defect.file_path.endswith(".py"):
                        compile(candidate_code, target_file.name, "exec")
                    patched_code = candidate_code
                    console.print("  [bold green]✓ Dev Squad LLM đã sinh bản vá mới thành công![/bold green]")
            except Exception as e:
                console.print(f"  [dim yellow]Chuyển tiếp sang Adaptive Heuristic Fallback ({e})...[/dim yellow]")

        # 3. Fallback Heuristic cơ bản
        if not patched_code:
            patched_code = self._apply_fallback_healing(defect, original_content)

        if patched_code and patched_code != original_content:
            target_file.write_text(patched_code, encoding="utf-8")
            defect.resolved = True
            defect.patch_summary = "Applied patch via Auto-Healing Coordinator"
            console.print(f"  [bold green]✔ Đã áp bản vá Auto-Healing thành công cho:[/bold green] {defect.file_path}")
            return True

        return False

    def _apply_fallback_healing(self, defect: DefectTicket, content: str) -> Optional[str]:
        """Quy tắc vá mã nguồn dự phòng khi chạy offline hoặc sandbox cô lập."""
        desc = (defect.issue_description + " " + (defect.stack_trace or "")).lower()
        new_content = content

        # Trường hợp 1: Trùng lặp khóa chính Unique constraint
        if "unique constraint failed" in desc or "integrityerror" in desc:
            if "import uuid" not in new_content:
                new_content = "import uuid\n" + new_content
            new_content = re.sub(
                r'order_id\s*=\s*f"ORD_\{[^}]+\}"',
                'order_id = f"ORD_{uuid.uuid4().hex[:8].upper()}"',
                new_content
            )

        # Trường hợp 2: Rò rỉ secret key
        if "secret" in desc or "credential" in desc:
            if 'SECRET_KEY = "' in new_content and "os.getenv" not in new_content:
                if "import os" not in new_content:
                    new_content = "import os\n" + new_content
                new_content = re.sub(
                    r'SECRET_KEY\s*=\s*"([^"]+)"',
                    r'SECRET_KEY: str = os.getenv("SECRET_KEY", "\1")',
                    new_content
                )

        # Trường hợp 3: CORS missing localhost:3000
        if "cors" in desc and "allow_origins" in new_content:
            if "http://localhost:3000" not in new_content:
                new_content = new_content.replace(
                    "allow_origins=[",
                    'allow_origins=["http://localhost:3000", "http://localhost:3001", '
                )

        return new_content if new_content != content else None

    async def run_auto_healing_cycle(
        self,
        defects: List[DefectTicket],
        agent_factory: Any,
        workspace_dir: Path,
        test_runner_fn: Any
    ) -> bool:
        """Thực thi vòng lặp: Vá mã nguồn -> Chạy lại test suite (Tối đa max_iterations)."""
        SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        for iteration in range(1, self.max_iterations + 1):
            unresolved = sorted(
                [d for d in defects if not d.resolved],
                key=lambda d: SEVERITY_ORDER.get(getattr(d, "severity", "HIGH").upper(), 99)
            )
            if not unresolved:
                return True

            console.print(Panel(
                f"[bold]Vòng lặp sửa lỗi tự động (Auto-Healing Iteration):[/bold] {iteration}/{self.max_iterations}\n"
                f"[bold]Số lỗi cần xử lý:[/bold] {len(unresolved)}",
                title="[bold cyan]Auto-Healing Coordinator Active[/bold cyan]",
                border_style="yellow"
            ))

            any_patched = False
            for defect in unresolved:
                patched = await self.execute_healing(defect, agent_factory, workspace_dir)
                if patched:
                    any_patched = True

            if not any_patched:
                console.print("  [dim yellow]Không còn bản vá nào được áp dụng thêm. Dừng vòng lặp.[/dim yellow]")
                break

            # Chạy lại test suite
            console.print("  [bold cyan]► Đang chạy lại kiểm thử để xác thực bản vá...[/bold cyan]")
            passed, stdout, stderr = await test_runner_fn()
            if passed:
                console.print("[bold green]✔ TẤT CẢ TEST CASES ĐÃ PASSED SAU KHI AUTO-HEALING![/bold green]")
                defects.clear()
                return True
            else:
                console.print(f"  [bold red]✗ Test vẫn chưa pass ở iteration {iteration}. Cập nhật traceback...[/bold red]")
                for defect in defects:
                    defect.stack_trace = f"{stdout}\n{stderr}"
                    defect.resolved = False

        return False

    def log_iteration_status(self, iteration: int, qa_result: QAEvaluationResult):
        color = "green" if qa_result.passed else "yellow"
        console.print(Panel(
            f"[bold]Vòng lặp sửa lỗi (Iteration):[/bold] {iteration} / {self.max_iterations}\n"
            f"[bold]Kết quả QA:[/bold] {'[green]PASSED[/green]' if qa_result.passed else '[red]FAILED[/red]'}\n"
            f"[bold]Độ phủ kiểm thử (Coverage):[/bold] {qa_result.coverage_score}%\n"
            f"[bold]Số lỗi còn tồn đọng:[/bold] {qa_result.total_defects}\n"
            f"[italic]{qa_result.summary}[/italic]",
            title="[bold cyan]Cơ Chế Auto-Healing Loop[/bold cyan]",
            border_style=color
        ))


def main(argv=None):
    console.print("[bold cyan]Auto-Healing Coordinator Module[/bold cyan]")
    console.print("Sử dụng thông qua orchestrator.runner hoặc scripts/auto_heal_heuristics.py.")


if __name__ == "__main__":
    main()
