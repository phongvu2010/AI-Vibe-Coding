"""
persistence.py — SDLC State Persistence & Checkpoint Recovery
Part of AI-Vibe-Coding (Antigravity 2.0).
"""

import json
from pathlib import Path
import sys
from typing import Optional
from rich.console import Console

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

try:
    from state import SDLCState
except ImportError:
    from scripts.state import SDLCState

console = Console()


class StatePersistence:
    """Quản lý lưu trữ và khôi phục trạng thái (Checkpoints) cho chu trình SDLC."""

    def __init__(self, checkpoints_dir: Path):
        self.checkpoints_dir = checkpoints_dir
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)

    def _get_checkpoint_path(self, project_name: str) -> Path:
        safe_name = project_name.lower().replace(" ", "_")
        return self.checkpoints_dir / f"{safe_name}_checkpoint.json"

    def save_checkpoint(self, state: SDLCState) -> Path:
        """Lưu snapshot hiện tại của dự án vào đĩa."""
        path = self._get_checkpoint_path(state.project_name)
        data = state.model_dump(mode="json")
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        console.print(f"  [dim]💾 Đã lưu checkpoint tại Phase ({state.current_phase.value}): {path.name}[/dim]")
        return path

    def load_checkpoint(self, project_name: str) -> Optional[SDLCState]:
        """Khôi phục trạng thái dự án từ checkpoint đã lưu."""
        path = self._get_checkpoint_path(project_name)
        if not path.exists():
            return None
        try:
            content = path.read_text(encoding="utf-8")
            data = json.loads(content)
            state = SDLCState.model_validate(data)
            console.print(f"[bold green]✓ Khôi phục thành công checkpoint dự án '{project_name}' tại Phase [{state.current_phase.value}][/bold green]")
            return state
        except Exception as e:
            console.print(f"[bold red]✗ Không thể đọc checkpoint: {e}[/bold red]")
            return None


def main(argv=None):
    console.print("[bold cyan]State Persistence Module[/bold cyan]")
    console.print("Quản lý lưu trữ và khôi phục trạng thái Checkpoint.")


if __name__ == "__main__":
    main()
