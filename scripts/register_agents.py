#!/usr/bin/env python3
"""
register_agents.py — Quản lý & Xác thực Định nghĩa Subagents Antigravity 2.0
Thuộc hệ thống AI-Vibe-Coding (Antigravity 2.0).

Chức năng:
1. Quét toàn bộ các file đặc tả tác tử trong .agents/agents/*.md.
2. Kiểm tra tính hợp lệ của YAML frontmatter (name, description, model, tools).
3. Xuất danh sách payload chuẩn hóa cho Tech Lead sử dụng với define_subagent hoặc invoke_subagent.
4. Tương thích hoàn toàn với kiến trúc 5 Sub-Teams (15 Subagents chuyên trách + 5 Squad Orchestrators).

Cách sử dụng:
    python3 scripts/register_agents.py --list
    python3 scripts/register_agents.py --validate
    python3 scripts/register_agents.py --export-json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Đảm bảo console UTF-8
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
AGENTS_DIR = ROOT_DIR / ".agents" / "agents"


def parse_agent_markdown(file_path: Path) -> Optional[Dict[str, Any]]:
    """Phân tích cú pháp Markdown có chứa YAML Frontmatter."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"❌ Lỗi đọc file {file_path.name}: {e}")
        return None

    pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return None

    raw_frontmatter, body = match.group(1), match.group(2).strip()
    data: Dict[str, Any] = {}

    # Phân tích thủ công các trường cơ bản để không phụ thuộc cứng vào pyyaml
    tools = []
    skills = []
    current_list = None

    for line in raw_frontmatter.splitlines():
        line_str = line.strip()
        if not line_str or line_str.startswith("#"):
            continue

        if line_str.startswith("tools:"):
            current_list = tools
            continue
        elif line_str.startswith("skills:"):
            current_list = skills
            continue
        elif line_str.startswith("- ") and current_list is not None:
            current_list.append(line_str[2:].strip().strip("'\""))
            continue
        else:
            current_list = None

        if ":" in line_str:
            key, val = line_str.split(":", 1)
            key = key.strip()
            val = val.strip().strip("'\"")
            data[key] = val

    data["tools"] = tools
    data["skills"] = skills
    data["system_prompt"] = body
    data["file_path"] = str(file_path.relative_to(ROOT_DIR))
    return data


def load_all_agents() -> List[Dict[str, Any]]:
    """Tải và sắp xếp toàn bộ danh sách tác tử."""
    if not AGENTS_DIR.exists():
        return []

    agents = []
    for file in sorted(AGENTS_DIR.glob("*.md")):
        parsed = parse_agent_markdown(file)
        if parsed and "name" in parsed:
            agents.append(parsed)
    return agents


def validate_agents(agents: List[Dict[str, Any]]) -> bool:
    """Xác thực tính toàn vẹn của danh sách tác tử."""
    print("=" * 72)
    print("🔍 [AGENT VALIDATOR] Đang kiểm tra 20 Subagent Specs trong .agents/agents/...")
    print("=" * 72)

    valid_models = {"pro", "flash", "flash_lite", "inherit"}
    all_ok = True

    for ag in agents:
        name = ag.get("name", "Unknown")
        model = ag.get("model", "inherit")
        desc = ag.get("description", "")
        prompt = ag.get("system_prompt", "")

        errors = []
        if not desc:
            errors.append("Thiếu trường 'description'")
        if model not in valid_models:
            errors.append(f"Model tier '{model}' không hợp lệ (hợp lệ: {valid_models})")
        if len(prompt) < 50:
            errors.append("System prompt quá ngắn (< 50 ký tự)")

        if errors:
            print(f"❌ [{name}]: {', '.join(errors)}")
            all_ok = False
        else:
            tier_badge = f"[{model.upper():<10}]"
            is_squad = "squad" in name
            tag = "📦 SQUAD" if is_squad else "👤 AGENT"
            print(f"✅ {tier_badge} {tag:<8} : {name:<20} ({ag['file_path']})")

    print("=" * 72)
    if all_ok:
        print(f"🎉 [VALIDATION PASSED] Toàn bộ {len(agents)} subagent specs đạt chuẩn Antigravity 2.0!")
    else:
        print(f"⚠️ Phát hiện lỗi trong cấu hình tác tử. Vui lòng khắc phục.")
    print("=" * 72)
    return all_ok


def list_agents(agents: List[Dict[str, Any]]) -> None:
    print("\n🏛️ DANH SÁCH 5 SUB-TEAMS & 15 SUBAGENTS (AI-VIBE-CODING):")
    print("-" * 72)
    print(f"{'Tên Tác Tử':<22} | {'Tier Model':<10} | {'Mô Tả & Trách Nhiệm'}")
    print("-" * 72)
    for ag in agents:
        name = ag.get("name", "")
        model = ag.get("model", "inherit")
        desc = ag.get("description", "")
        if len(desc) > 60:
            desc = desc[:57] + "..."
        print(f"{name:<22} | {model:<10} | {desc}")
    print("-" * 72)


def main():
    parser = argparse.ArgumentParser(description="Quản lý & xác thực Subagents trên Antigravity 2.0")
    parser.add_argument("--list", action="store_true", help="Liệt kê danh sách toàn bộ subagents")
    parser.add_argument("--validate", action="store_true", help="Kiểm tra tính hợp lệ của specs")
    parser.add_argument("--export-json", action="store_true", help="Xuất danh sách JSON cho define_subagent")

    args = parser.parse_args()
    agents = load_all_agents()

    if not agents:
        print("❌ Không tìm thấy file tác tử nào trong .agents/agents/")
        sys.exit(1)

    if args.list:
        list_agents(agents)
    elif args.export_json:
        payload = [
            {
                "name": ag["name"],
                "description": ag.get("description", ""),
                "system_prompt": ag.get("system_prompt", ""),
                "enable_write_tools": "write_to_file" in ag.get("tools", []),
                "enable_mcp_tools": True,
                "enable_subagent_tools": "invoke_subagent" in ag.get("tools", []) or "squad" in ag["name"],
            }
            for ag in agents
        ]
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        # Mặc định là validate
        ok = validate_agents(agents)
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
