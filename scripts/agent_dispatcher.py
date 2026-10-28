#!/usr/bin/env python3
"""
agent_dispatcher.py — Động Cơ Điều Phối & Kích Hoạt Subagents / Sub-Teams (Antigravity 2.0 & Gemini API)
Thuộc hệ thống AI-Vibe-Coding.

Chức năng:
1. Định tuyến mô hình nhận thức (Model Routing & Cost Optimization): PRO, FLASH, FLASH-LITE theo `config/model_router.yaml`.
2. Nạp ngữ cảnh, System Prompts và Guardrails từ `.agents/agents/`, `.agents/subteams/` và `.agents/rules/`.
3. Dispatch và tương tác với AI Models qua `google.antigravity` SDK hoặc `google.genai` SDK (Gemini API) với hỗ trợ Structured Output Pydantic Schemas.
4. Chế độ Mock / Offline Fallback thông minh khi chạy kiểm thử cục bộ hoặc không có API key.

Cách sử dụng:
    python scripts/agent_dispatcher.py --models
    python scripts/agent_dispatcher.py --list-agents
    python scripts/agent_dispatcher.py --agent lead-ba --prompt "Làm rõ yêu cầu đặt lịch bảo dưỡng xe máy"
    python scripts/agent_dispatcher.py --subteam discovery --input examples/sample_client_brief.md
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Type
import yaml

# Đảm bảo console UTF-8 trên Windows
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    from pydantic import BaseModel
except ImportError:
    BaseModel = object

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    console = Console()
    HAS_RICH = True
except ImportError:
    console = None
    HAS_RICH = False

# Kiểm tra Google GenAI / Antigravity SDK
try:
    from google import genai
    from google.genai import types as genai_types
    HAS_GOOGLE_GENAI = True
except ImportError:
    HAS_GOOGLE_GENAI = False

try:
    from google import antigravity
    HAS_ANTIGRAVITY_SDK = True
except ImportError:
    HAS_ANTIGRAVITY_SDK = False

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
AGENTS_DIR = BASE_DIR / ".agents"


class ModelRouter:
    """Bộ định tuyến và phân bổ mô hình AI (Model Router & Cost Allocator)."""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or (CONFIG_DIR / "model_router.yaml")
        self.config: Dict[str, Any] = {}
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.config = yaml.safe_load(f) or {}
            except Exception as e:
                print(f"⚠️ Không thể nạp model_router.yaml: {e}")

    def get_tier_model(self, tier: str) -> str:
        """Lấy tên model theo tier ('pro', 'flash', 'flash_lite'), hỗ trợ override qua biến môi trường."""
        tier_clean = tier.lower().strip()
        if "pro" in tier_clean:
            tier_key = "pro"
        elif "lite" in tier_clean:
            tier_key = "flash_lite"
        elif "flash" in tier_clean:
            tier_key = "flash"
        else:
            tier_key = "flash"

        tier_config = self.config.get("tiers", {}).get(tier_key, {})
        env_key = tier_config.get("env_override_key") or f"GEMINI_{tier_key.upper()}_MODEL"
        default_model = tier_config.get("nextgen_model") or tier_config.get("model_name") or {
            "pro": "gemini-2.5-pro",
            "flash": "gemini-2.5-flash",
            "flash_lite": "gemini-2.5-flash-lite"
        }.get(tier_key, "gemini-2.5-flash")

        return os.getenv(env_key, default_model)

    def get_tier_for_agent(self, agent_id: str) -> str:
        """Lấy tier danh định cho một Subagent."""
        clean_id = agent_id.lower().replace("@", "").strip()
        agents_alloc = self.config.get("agents_allocation", {})
        if clean_id in agents_alloc:
            return agents_alloc[clean_id].get("tier", "flash")

        # Suy đoán theo hậu tố hoặc phân đội
        if any(k in clean_id for k in ["architect", "planner", "reviewer"]):
            return "pro"
        elif any(k in clean_id for k in ["writer", "manifest", "scanner", "handover"]):
            return "flash_lite"
        return "flash"

    def get_model_for_agent(self, agent_id: str) -> str:
        """Trả về tên model thực tế cho agent."""
        tier = self.get_tier_for_agent(agent_id)
        return self.get_tier_model(tier)

    def print_matrix(self) -> None:
        """Hiển thị bảng ma trận phân bổ mô hình và chi phí tương đối."""
        if HAS_RICH and console:
            table = Table(title="🤖 Ma Trận Phân Bổ Mô Hình & Tối Ưu Chi Phí (AI-Vibe-Coding)", border_style="cyan")
            table.add_column("Tier", style="bold magenta")
            table.add_column("Mô hình mặc định", style="green")
            table.add_column("Next-Gen Model", style="yellow")
            table.add_column("Chi phí tương đối", style="cyan")
            table.add_column("Tác vụ tiêu biểu", style="white")

            for tier, info in self.config.get("tiers", {}).items():
                tasks = "\n".join(f"• {t}" for t in info.get("target_tasks", [])[:3])
                table.add_row(
                    tier.upper(),
                    info.get("model_name", "N/A"),
                    info.get("nextgen_model", "N/A"),
                    f"{info.get('relative_cost_factor', 1.0)}x",
                    tasks
                )
            console.print(table)
        else:
            print("Ma Trận Phân Bổ Mô Hình (Model Router):")
            for tier, info in self.config.get("tiers", {}).items():
                print(f"  [{tier.upper()}] Model: {info.get('nextgen_model', info.get('model_name'))} ({info.get('relative_cost_factor')}x)")


class AgentDispatcher:
    """Bộ nạp ngữ cảnh và điều phối lệnh tới các Subagents / Sub-Teams."""

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or BASE_DIR
        self.router = ModelRouter(self.base_dir / "config" / "model_router.yaml")
        self.agents_dir = self.base_dir / ".agents" / "agents"
        self.subteams_dir = self.base_dir / ".agents" / "subteams"
        self.rules_dir = self.base_dir / ".agents" / "rules"

    def load_agent_prompt(self, agent_id: str) -> str:
        """Nạp nội dung System Prompt của Agent từ thư mục .agents/agents/."""
        clean_id = agent_id.lower().replace("@", "").strip()
        candidates = [
            self.agents_dir / f"{clean_id}.md",
            self.agents_dir / f"{clean_id.replace('-', '_')}.md",
        ]
        for p in candidates:
            if p.exists():
                return p.read_text(encoding="utf-8")
        return f"# Agent: {clean_id}\nBạn là chuyên gia phụ trách phân hệ {clean_id} trong AI-Vibe-Coding."

    def load_subteam_prompt(self, subteam_id: str) -> str:
        """Nạp nội dung System Prompt của Sub-Team từ thư mục .agents/subteams/."""
        clean_id = subteam_id.lower().replace("@", "").strip()
        for p in self.subteams_dir.glob("*.md"):
            if clean_id in p.stem.lower():
                return p.read_text(encoding="utf-8")
        return f"# Sub-Team: {clean_id}\nĐội ngũ phát triển phần mềm thuộc AI-Vibe-Coding."

    def load_all_rules(self) -> str:
        """Nạp toàn bộ bộ quy chuẩn an toàn và tiêu chuẩn lập trình."""
        rules = []
        if self.rules_dir.exists():
            for p in sorted(self.rules_dir.glob("*.md")):
                rules.append(f"### [RULE: {p.stem.upper()}]\n{p.read_text(encoding='utf-8')}")
        return "\n\n".join(rules)

    def get_available_mcp_servers(self) -> List[Dict[str, Any]]:
        """Phát hiện các MCP Servers khả dụng trong Antigravity 2.0 (~/.gemini/antigravity/mcp)."""
        mcp_dirs = [
            Path(os.path.expanduser("~/.gemini/antigravity/mcp")),
            self.base_dir / ".gemini" / "antigravity" / "mcp"
        ]
        available_mcps = []
        for mcp_root in mcp_dirs:
            if mcp_root.exists() and mcp_root.is_dir():
                for d in mcp_root.iterdir():
                    if d.is_dir() and not d.name.startswith("."):
                        tools = [t.stem for t in d.glob("*.json")]
                        available_mcps.append({
                            "name": d.name,
                            "path": str(d),
                            "tools": tools
                        })
        return available_mcps

    def get_mcp_context_instructions(self) -> str:
        """Sinh chỉ dẫn khai thác MCP Servers cho Agents trên Antigravity 2.0."""
        mcps = self.get_available_mcp_servers()
        if not mcps:
            return ""
        lines = [
            "\n### TẬN DỤNG CÁC MCP SERVERS KHẢ DỤNG TRÊN ANTIGRAVITY 2.0:",
            "Các Agents được trang bị quyền truy vấn các MCP tools sau để hỗ trợ thẩm định và phát triển:"
        ]
        for m in mcps:
            tools_str = ", ".join(m["tools"][:6]) if m["tools"] else "native tools"
            lines.append(f"- MCP Server `{m['name']}`: Công cụ khả dụng: [{tools_str}]")
        lines.append("- Sub-Team 1 (Discovery): Ưu tiên dùng `gemini-notebook-mcp` (`notebook_query`, `notebook_list`, `research_start`) để tra cứu tài liệu nghiệp vụ tham khảo.")
        lines.append("- Sub-Team 2 & 3 (Architecture & Dev): Ưu tiên dùng `gemini-api_gemini-api-docs` (`gemini_search_docs`, `gemini_get_doc`) để tra cứu chuẩn SDK Google GenAI & OpenAPI specs mới nhất.")
        lines.append("- Sub-Team 4 (QA & Audit): Ưu tiên dùng `chrome-devtools` để audit giao diện (a11y, console logs, network errors).")
        return "\n".join(lines) + "\n"

    def dispatch(
        self,
        target_name: str,
        user_prompt: str,
        schema_class: Optional[Type[BaseModel]] = None,
        is_subteam: bool = False
    ) -> Any:
        """Thực thi chỉ thị bằng Gemini API hoặc Mock Engine."""
        tier = self.router.get_tier_for_agent(target_name)
        model_name = self.router.get_tier_model(tier)
        system_prompt = self.load_subteam_prompt(target_name) if is_subteam else self.load_agent_prompt(target_name)
        rules = self.load_all_rules()
        mcp_context = self.get_mcp_context_instructions()

        full_system_instruction = f"{system_prompt}\n\n## QUY TẮC BẢO MẬT & CHẤT LƯỢNG (RULES):\n{rules}\n{mcp_context}"

        api_key = os.getenv("GEMINI_API_KEY")

        if api_key and HAS_GOOGLE_GENAI:
            try:
                client = genai.Client(api_key=api_key)
                config_args = {
                    "system_instruction": full_system_instruction,
                    "temperature": 0.2 if tier == "pro" else 0.4,
                }
                if schema_class and issubclass(schema_class, BaseModel):
                    config_args["response_mime_type"] = "application/json"
                    config_args["response_schema"] = schema_class

                response = client.models.generate_content(
                    model=model_name,
                    contents=user_prompt,
                    config=genai_types.GenerateContentConfig(**config_args)
                )

                if schema_class and hasattr(response, "parsed") and response.parsed:
                    return response.parsed
                return response.text
            except Exception as e:
                print(f"⚠️ Lỗi khi gọi Gemini API ({model_name}): {e}. Chuyển sang chế độ mô phỏng (Offline Fallback)...")

        # Mock / Offline Fallback Mode
        return self._generate_mock_response(target_name, user_prompt, model_name, tier, schema_class)

    def _generate_mock_response(
        self,
        target: str,
        prompt: str,
        model: str,
        tier: str,
        schema_class: Optional[Type[BaseModel]]
    ) -> Any:
        """Sinh phản hồi giả lập có cấu trúc phục vụ test cục bộ mà không tốn token."""
        if schema_class:
            try:
                # Trả về đối tượng schema rỗng mặc định nếu có
                return schema_class()
            except Exception:
                pass

        return (
            f"[OFFLINE/MOCK DISPATCH RUNNER]\n"
            f"• Target Agent/Squad : {target}\n"
            f"• Routed Tier        : {tier.upper()} (Model: {model})\n"
            f"• Status             : Ready for execution in Antigravity Chat Canvas\n"
            f"• Prompt Received    : {prompt[:120]}..."
        )


def main():
    parser = argparse.ArgumentParser(description="Động cơ điều phối Subagents & Model Router cho AI-Vibe-Coding")
    parser.add_argument("--models", action="store_true", help="Hiển thị ma trận phân bổ mô hình Model Router")
    parser.add_argument("--list-agents", action="store_true", help="Liệt kê danh sách 15 Subagents chuyên trách")
    parser.add_argument("--mcp", action="store_true", help="Quét và hiển thị các MCP Servers & Tools khả dụng")
    parser.add_argument("--agent", help="Tên Subagent cần gọi (vd: lead-ba, system-architect)")
    parser.add_argument("--subteam", help="Tên Sub-Team cần gọi (vd: discovery, architecture, engineering, qa, release)")
    parser.add_argument("--prompt", help="Nội dung câu lệnh hoặc chỉ thị gửi tới Agent")
    parser.add_argument("--input", help="Đường dẫn file văn bản đầu vào (vd: brief.md)")

    args = parser.parse_args()
    dispatcher = AgentDispatcher()

    if args.mcp:
        mcps = dispatcher.get_available_mcp_servers()
        print(f"\n🔌 PHÁT HIỆN {len(mcps)} MCP SERVERS KHẢ DỤNG TRÊN ANTIGRAVITY 2.0:")
        if not mcps:
            print("  (Không tìm thấy MCP Server trong ~/.gemini/antigravity/mcp)")
        for m in mcps:
            print(f"  • MCP Server: \033[1;36m{m['name']}\033[0m")
            print(f"    - Đường dẫn: {m['path']}")
            print(f"    - Công cụ: {', '.join(m['tools'][:10])}{' ...' if len(m['tools']) > 10 else ''}")
        print("\n" + dispatcher.get_mcp_context_instructions())
        return

    if args.models:
        dispatcher.router.print_matrix()
        return

    if args.list_agents:
        print("\n🏛️ DANH SÁCH 5 SUB-TEAMS & 15 SUBAGENTS (AI-VIBE-CODING):")
        agents = [
            ("1. Discovery & Solutions", "account-lead", "flash", "Tiếp nhận brief, phân loại T-Shirt size S/M/L"),
            ("1. Discovery & Solutions", "lead-ba", "pro", "Phỏng vấn làm rõ qua ask_question, viết PRD"),
            ("1. Discovery & Solutions", "uiux-designer", "flash", "Thiết kế luồng màn hình, ma trận 5 UI states"),
            ("2. Architecture & Planning", "system-architect", "pro", "Clean Architecture 5 tầng, ERD quan hệ"),
            ("2. Architecture & Planning", "security-architect", "pro", "STRIDE Threat Model, OWASP Guardrails"),
            ("2. Architecture & Planning", "tech-planner", "pro", "Kế hoạch plan.md, Data Contract Matrix"),
            ("3. Core Engineering", "db-dev", "inherit", "SQLAlchemy 2.0 Async Models & Alembic"),
            ("3. Core Engineering", "frontend-dev", "inherit", "Next.js 15 / React Native Expo, 5 UI states"),
            ("3. Core Engineering", "backend-dev", "inherit", "FastAPI Clean Architecture, Services & Repos"),
            ("3. Core Engineering", "devops-engineer", "inherit", "Docker, docker-compose, scripts vận hành"),
            ("4. QA & Security Audit", "qa-tester", "flash", "Kiểm thử tự động 5 tầng, Pytest, Linter"),
            ("4. QA & Security Audit", "code-reviewer", "pro", "Thẩm định chất lượng code & bảo mật qua diff"),
            ("5. Release & Handover", "release-engineer", "flash_lite", "Đóng gói release .zip, SHA-256 Checksum"),
            ("5. Release & Handover", "tech-writer", "flash_lite", "Soạn USER_MANUAL.md, API_GUIDE.md"),
            ("5. Release & Handover", "handover-lead", "flash", "Soạn UAT_CHECKLIST.md, bàn giao khách hàng"),
        ]
        for team, agent, tier, desc in agents:
            print(f"  • [{agent:<18}] (Tier: {tier:<10}) [{team}] -> {desc}")
        return

    target = args.agent or args.subteam
    if not target:
        parser.print_help()
        return

    prompt_content = args.prompt or ""
    if args.input:
        input_file = Path(args.input)
        if input_file.exists():
            prompt_content = input_file.read_text(encoding="utf-8")
        else:
            print(f"❌ File không tồn tại: {args.input}")
            sys.exit(1)

    if not prompt_content:
        print("❌ Vui lòng cung cấp nội dung chỉ thị qua --prompt hoặc --input.")
        sys.exit(1)

    res = dispatcher.dispatch(
        target_name=target,
        user_prompt=prompt_content,
        is_subteam=bool(args.subteam)
    )
    print("\n" + "=" * 70)
    print(f"🤖 KẾT QUẢ ĐIỀU PHỐI TÁC TỬ: {target.upper()}")
    print("=" * 70)
    print(res)
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
