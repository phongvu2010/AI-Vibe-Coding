#!/usr/bin/env python3
"""
dag_engine.py — Động cơ điều phối và phân tích đồ thị phụ thuộc DAG (Directed Acyclic Graph).
Thuộc hệ thống AI-Vibe-Coding (Antigravity 2.0).

Chức năng:
1. Phát hiện chu trình phụ thuộc (Cycle / Deadlock detection) giữa các tác vụ.
2. Tính toán các Wave thực thi song song (Parallel Wave Scheduling).
3. Thẩm định file task_backlog_dag.json trong docs/specs/<feature-slug>/.

Cách sử dụng:
    python scripts/dag_engine.py --file docs/specs/example/task_backlog_dag.json
    python scripts/dag_engine.py --demo
"""

import argparse
import json
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from rich.console import Console
    from rich.table import Table
    console = Console()
    HAS_RICH = True
except ImportError:
    console = None
    Table = None
    HAS_RICH = False

try:
    from pydantic import BaseModel, Field
except ImportError:
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    def Field(default_factory=None, **kwargs):
        return default_factory() if default_factory else None


class TaskNode:
    def __init__(
        self,
        id: str,
        team: str = "engineering",
        title: str = "",
        depends_on: List[str] = None,
        status: str = "pending",
        result: Dict[str, Any] = None,
        **kwargs
    ):
        self.id = id
        self.team = team
        self.title = title
        self.depends_on = depends_on or []
        self.status = status
        self.result = result or {}


class DAGExecutionEngine:
    """Động cơ điều phối và thực thi công việc theo Đồ thị Có hướng Không chu trình (DAG)."""

    def __init__(self, raw_tasks: List[Dict[str, Any]]):
        self.tasks: Dict[str, TaskNode] = {t["id"]: TaskNode(**t) for t in raw_tasks}
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)
        self._build_graph()

    def _build_graph(self):
        for task_id in self.tasks:
            self.in_degree[task_id] = 0

        for task_id, node in self.tasks.items():
            for dep in node.depends_on:
                if dep in self.tasks:
                    self.graph[dep].append(task_id)
                    self.in_degree[task_id] += 1
                else:
                    print(f"⚠️ Cảnh báo: Task '{task_id}' phụ thuộc vào '{dep}' không tồn tại.")

    def detect_cycle(self) -> bool:
        """Kiểm tra xem đồ thị có chu trình lặp vô tận (deadlock) hay không."""
        in_degrees = dict(self.in_degree)
        queue = deque([node for node, deg in in_degrees.items() if deg == 0])
        visited_count = 0

        while queue:
            current = queue.popleft()
            visited_count += 1
            for neighbor in self.graph[current]:
                in_degrees[neighbor] -= 1
                if in_degrees[neighbor] == 0:
                    queue.append(neighbor)

        return visited_count != len(self.tasks)

    def get_execution_waves(self) -> List[List[TaskNode]]:
        """Phân rã các task thành các Wave (Đợt thực thi song song)."""
        if self.detect_cycle():
            raise ValueError("Phát hiện chu trình phụ thuộc (Cycle/Deadlock) trong danh sách Task!")

        in_degrees = dict(self.in_degree)
        queue = deque([node for node, deg in in_degrees.items() if deg == 0])
        waves: List[List[TaskNode]] = []

        while queue:
            current_wave_ids = list(queue)
            current_wave_tasks = [self.tasks[tid] for tid in current_wave_ids]
            waves.append(current_wave_tasks)

            next_queue = deque()
            for tid in current_wave_ids:
                for neighbor in self.graph[tid]:
                    in_degrees[neighbor] -= 1
                    if in_degrees[neighbor] == 0:
                        next_queue.append(neighbor)
            queue = next_queue

        return waves

    def print_execution_plan(self):
        """Hiển thị kế hoạch phân rã Task trực quan trên Terminal (sử dụng Rich Table nếu có)."""
        waves = self.get_execution_waves()

        if HAS_RICH and console and Table:
            table = Table(title="KẾ HOẠCH ĐIỀU PHỐI TASK THEO ĐỒ THỊ DAG (PARALLEL WAVES)", border_style="cyan")
            table.add_column("Wave (Đợt)", justify="center", style="cyan")
            table.add_column("Task ID", style="bold yellow")
            table.add_column("Sub-Team Phụ Trách", style="magenta")
            table.add_column("Tiêu Đề Công Việc", style="white")
            table.add_column("Phụ Thuộc Vào (Depends On)", style="green")

            for wave_idx, wave in enumerate(waves, 1):
                for task in wave:
                    deps = ", ".join(task.depends_on) if task.depends_on else "[italic dim]None (Độc lập)[/italic dim]"
                    table.add_row(f"Wave {wave_idx}", task.id, task.team.upper(), task.title, deps)

            console.print(table)
        else:
            print("\n" + "=" * 70)
            print("  📊 KẾ HOẠCH PHÂN RÃ VÀ ĐIỀU PHỐI TASK THEO ĐỒ THỊ DAG (PARALLEL WAVES)")
            print("=" * 70)
            for wave_idx, wave in enumerate(waves, 1):
                print(f"\n▶ WAVE {wave_idx} ({len(wave)} tasks có thể chạy song song):")
                for task in wave:
                    deps = ", ".join(task.depends_on) if task.depends_on else "None (Độc lập)"
                    print(f"  • [{task.id}] ({task.team.upper()}): {task.title} (Phụ thuộc: {deps})")
            print("\n" + "=" * 70)

    def export_wave_plan(self, output_path: Path) -> Path:
        """Xuất kế hoạch thực thi song song theo đợt ra file JSON chuẩn hóa cho Orchestrator / Dispatcher."""
        waves = self.get_execution_waves()
        plan_data = {
            "total_waves": len(waves),
            "total_tasks": len(self.tasks),
            "deadlock_detected": False,
            "waves": [
                {
                    "wave_index": wave_idx,
                    "task_count": len(wave),
                    "execution_mode": "parallel" if len(wave) > 1 else "sequential",
                    "tasks": [
                        {
                            "id": t.id,
                            "team": t.team,
                            "title": t.title,
                            "depends_on": t.depends_on,
                            "status": t.status
                        }
                        for t in wave
                    ]
                }
                for wave_idx, wave in enumerate(waves, 1)
            ]
        }
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(plan_data, f, ensure_ascii=False, indent=2)
        return output_path

    def display_execution_plan(self):
        """Bí danh của print_execution_plan cho tính tương thích ngược."""
        self.print_execution_plan()


def demo(export_path: Optional[Path] = None):
    sample_tasks = [
        {"id": "TASK-01", "team": "db-dev", "title": "Tạo DB Models & Alembic Migration", "depends_on": []},
        {"id": "TASK-02", "team": "frontend-dev", "title": "Tạo UI Components & Mock Fixtures", "depends_on": []},
        {"id": "TASK-03", "team": "backend-dev", "title": "Viết FastAPI Endpoints & Pydantic Schemas", "depends_on": ["TASK-01"]},
        {"id": "TASK-04", "team": "qa-tester", "title": "Chạy bộ kiểm thử 5 tầng & Smoke Test", "depends_on": ["TASK-02", "TASK-03"]},
        {"id": "TASK-05", "team": "release-engineer", "title": "Đóng gói bản phát hành .zip & UAT", "depends_on": ["TASK-04"]},
    ]
    engine = DAGExecutionEngine(sample_tasks)
    engine.display_execution_plan()
    if export_path:
        out = engine.export_wave_plan(export_path)
        print(f"📦 Đã xuất kế hoạch đợt sóng thực thi ra: {out}")


def main():
    parser = argparse.ArgumentParser(description="DAG Execution Engine cho AI-Vibe-Coding")
    parser.add_argument("--file", help="Đường dẫn file task_backlog_dag.json cần thẩm định")
    parser.add_argument("--export-waves", help="Xuất kế hoạch sóng song song ra file JSON")
    parser.add_argument("--demo", action="store_true", help="Chạy kịch bản mẫu minh họa")
    args = parser.parse_args()

    export_path = Path(args.export_waves) if args.export_waves else None

    if args.demo:
        demo(export_path)
        return

    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"❌ File không tồn tại: {path}")
            sys.exit(1)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        tasks = data if isinstance(data, list) else data.get("tasks", [])
        engine = DAGExecutionEngine(tasks)
        if engine.detect_cycle():
            print("❌ Phát hiện chu trình (Deadlock) trong đồ thị tasks!")
            sys.exit(1)
        engine.display_execution_plan()
        if export_path:
            out = engine.export_wave_plan(export_path)
            print(f"📦 Đã xuất kế hoạch sóng song song ra: {out}")
        print("✔ Đồ thị DAG hợp lệ! Không có chu trình.")
    else:
        demo(export_path)


if __name__ == "__main__":
    main()
