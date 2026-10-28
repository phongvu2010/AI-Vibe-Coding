#!/usr/bin/env python3
"""
generate_gate_review.py — Sinh Biên Bản Đánh Giá Quality Gate & Duyệt Tương Tác (HITL)
Thuộc hệ thống AI-Vibe-Coding (Antigravity 2.0).

Chức năng:
1. Đọc cấu hình tiêu chí từ `config/quality_gates.yaml`.
2. Tự động quét kiểm tra sự tồn tại và kích thước của các Artifacts theo từng Gate.
3. Sinh tài liệu Markdown tương tác `review_gate_<N>.md` với bảng artifacts,
   checklist nghiệm thu và quyết định ký duyệt (Approval Log).
4. Hỗ trợ chế độ `--interactive` (Human-in-the-Loop TUI) cho phép Tech Lead phê duyệt,
   yêu cầu sửa đổi hoặc từ chối trực tiếp từ dòng lệnh kèm lưu checkpoint tự động.

Cách sử dụng:
    python scripts/generate_gate_review.py --gate 1 --feature motocare-booking
    python scripts/generate_gate_review.py --gate 1 --interactive
    python scripts/generate_gate_review.py --gate 2 --status APPROVED --reviewer "Tech Lead"
"""

import argparse
import datetime
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Đảm bảo console UTF-8 trên Windows
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    import yaml
except ImportError:
    yaml = None

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.table import Table
    console = Console()
    HAS_RICH = True
except ImportError:
    console = None
    HAS_RICH = False

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "quality_gates.yaml"


GATE_MAP = {
    "1": "gate_1_client_signoff",
    "gate_1": "gate_1_client_signoff",
    "gate_1_prd": "gate_1_client_signoff",
    "gate_1_client_signoff": "gate_1_client_signoff",
    "2": "gate_2_architecture_signoff",
    "gate_2": "gate_2_architecture_signoff",
    "gate_2_architecture": "gate_2_architecture_signoff",
    "gate_2_architecture_signoff": "gate_2_architecture_signoff",
    "3": "gate_3_production_readiness",
    "gate_3": "gate_3_production_readiness",
    "gate_3_deploy": "gate_3_production_readiness",
    "gate_3_production_readiness": "gate_3_production_readiness",
}


def load_quality_gates() -> Dict[str, Any]:
    if not CONFIG_PATH.exists() or yaml is None:
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data.get("quality_gates", {})
    except Exception as e:
        print(f"⚠️ Không thể đọc {CONFIG_PATH}: {e}")
        return {}


def get_default_artifacts(gate_id: str, feature_slug: str) -> List[Path]:
    specs_dir = BASE_DIR / "docs" / "specs" / feature_slug
    if gate_id == "gate_1_client_signoff":
        return [
            specs_dir / "prd.md",
            specs_dir / "ui_ux_spec.md",
            specs_dir / "clarification_qna.md",
        ]
    elif gate_id == "gate_2_architecture_signoff":
        return [
            specs_dir / "plan.md",
            specs_dir / "openapi.yaml",
            specs_dir / "erd.mermaid",
        ]
    elif gate_id == "gate_3_production_readiness":
        return [
            specs_dir / "test-report.md",
            specs_dir / "review-report.md",
            specs_dir / "uat_checklist.md",
        ]
    return []


def generate_gate_review(
    gate_key_input: str,
    feature_slug: str = "default",
    status: str = "PENDING",
    reviewer: str = "Product Owner / Tech Lead",
    feedback: str = ""
) -> Path:
    normalized_key = GATE_MAP.get(str(gate_key_input).lower(), "gate_1_client_signoff")
    gates_config = load_quality_gates()
    gate_data = gates_config.get(normalized_key, {})

    gate_name = gate_data.get("name", normalized_key.upper())
    responsible = gate_data.get("responsible", "Tech Lead")
    approver = gate_data.get("approver", reviewer)
    checklist = gate_data.get("checklist", [])

    specs_dir = BASE_DIR / "docs" / "specs" / feature_slug
    specs_dir.mkdir(parents=True, exist_ok=True)

    artifacts = get_default_artifacts(normalized_key, feature_slug)

    artifact_rows = []
    for idx, p in enumerate(artifacts, 1):
        exists = p.exists()
        status_icon = "✅ Sẵn sàng" if exists else "⚠️ Chưa tạo"
        size_str = f"{p.stat().st_size:,} bytes" if exists else "N/A"
        rel_path = p.relative_to(BASE_DIR) if p.is_relative_to(BASE_DIR) else p
        artifact_rows.append(f"| {idx} | [{p.name}]({rel_path}) | `{rel_path}` | {size_str} | {status_icon} |")

    table_md = "\n".join(artifact_rows) if artifact_rows else "| - | Không có artifact cụ thể | - | - | - |"

    checklist_rows = []
    for item in checklist:
        checked = "x" if status == "APPROVED" else " "
        mandatory_tag = " *(Bắt buộc)*" if item.get("mandatory") else ""
        checklist_rows.append(f"- [{checked}] **[{item.get('id', 'ITEM')}]** {item.get('item', '')}{mandatory_tag}")

    checklist_md = "\n".join(checklist_rows) if checklist_rows else "- [ ] Tiêu chuẩn kiểm tra đạt yêu cầu"

    now_iso = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    decision_md = f"""## 📋 BIÊN BẢN PHÊ DUYỆT (DECISION LOG)
- **Trạng thái:** **{status.upper()}**
- **Người ký duyệt:** `{approver}`
- **Tác tử phụ trách:** `{responsible}`
- **Thời gian đánh giá:** `{now_iso}`
- **Ý kiến chỉ đạo / Phản hồi:**
> {feedback if feedback else "Các tiêu chí kỹ thuật và nghiệp vụ đã được thẩm định theo quy chuẩn Antigravity 2.0."}
"""

    gate_num = "1" if "1" in normalized_key else "2" if "2" in normalized_key else "3"
    target_file = specs_dir / f"review_gate_{gate_num}.md"

    content = f"""# 🚦 BIÊN BẢN ĐÁNH GIÁ CHẤT LƯỢNG: {gate_name.upper()}
> [!IMPORTANT]
> **Dự án / Phân hệ:** `{feature_slug}`  
> **Người có thẩm quyền phê duyệt:** `{approver}`  
> **Tác tử chịu trách nhiệm chuẩn bị:** `{responsible}`  
> **Cập nhật lần cuối:** `{now_iso}`

---

## 📂 1. DANH SÁCH ARTIFACTS CẦN THẨM ĐỊNH

| STT | Tài Liệu / Tệp Tin | Đường Dẫn Tương Đối | Dung Lượng | Trạng Thái |
|---|---|---|---|---|
{table_md}

---

## 🎯 2. BẢNG TIÊU CHÍ NGHIỆM THU (GATE EXIT CHECKLIST)
{checklist_md}

---

{decision_md}
"""

    target_file.write_text(content, encoding="utf-8")
    print(f"✅ Đã sinh biên bản Gate Review tại: {target_file.relative_to(BASE_DIR)}")
    return target_file


def run_interactive_review(gate_key_input: str, feature_slug: str, reviewer: str = "Tech Lead") -> Tuple[str, str]:
    """Chạy quy trình phê duyệt tương tác Human-in-the-Loop trực tiếp từ Terminal."""
    normalized_key = GATE_MAP.get(str(gate_key_input).lower(), "gate_1_client_signoff")
    gates_config = load_quality_gates()
    gate_data = gates_config.get(normalized_key, {})
    gate_name = gate_data.get("name", normalized_key.upper())
    gate_num = "1" if "1" in normalized_key else "2" if "2" in normalized_key else "3"

    artifacts = get_default_artifacts(normalized_key, feature_slug)

    print("\n" + "=" * 75)
    print(f"  🚦 HUMAN-IN-THE-LOOP QUALITY GATE: {gate_name.upper()}")
    print("=" * 75)
    print(f"Phân hệ / Feature: {feature_slug}")
    print(f"Người kiểm duyệt : {reviewer}")
    print("-" * 75)
    print("Danh sách Artifacts:")
    for idx, p in enumerate(artifacts, 1):
        exists_str = "✔ SẴN SÀNG" if p.exists() else "✗ CHƯA CÓ"
        size_str = f"({p.stat().st_size:,} bytes)" if p.exists() else ""
        print(f"  [{idx}] {p.name:<25} {exists_str:<12} {size_str}")

    print("\nLỰA CHỌN KÝ DUYỆT (Tech Lead / Reviewer):")
    print("  [1] PHÊ DUYỆT (Approve)           -> Chuyển tiếp sang Phase tiếp theo")
    print("  [2] YÊU CẦU SỬA ĐỔI (Need Review) -> Nhập feedback yêu cầu AI sửa lại")
    print("  [3] TỪ CHỐI (Reject)              -> Dừng quy trình")

    if HAS_RICH and console:
        choice = Prompt.ask("\nVui lòng chọn", choices=["1", "2", "3"], default="1")
    else:
        choice = input("\nVui lòng chọn [1/2/3] (mặc định 1): ").strip() or "1"

    if choice == "1":
        if HAS_RICH and console:
            feedback = Prompt.ask("Ghi chú phê duyệt", default="Đã phê duyệt, đạt chuẩn kỹ thuật.")
        else:
            feedback = input("Ghi chú phê duyệt [Đã phê duyệt, đạt chuẩn kỹ thuật]: ").strip() or "Đã phê duyệt, đạt chuẩn kỹ thuật."
        status = "APPROVED"
    elif choice == "2":
        if HAS_RICH and console:
            feedback = Prompt.ask("Nội dung yêu cầu sửa đổi chi tiết")
        else:
            feedback = input("Nội dung yêu cầu sửa đổi chi tiết: ").strip() or "Cần điều chỉnh theo phản hồi của Tech Lead."
        status = "REVISION_REQUESTED"
    else:
        if HAS_RICH and console:
            feedback = Prompt.ask("Lý do từ chối", default="Không đạt tiêu chí nghiệm thu.")
        else:
            feedback = input("Lý do từ chối [Không đạt tiêu chí nghiệm thu]: ").strip() or "Không đạt tiêu chí nghiệm thu."
        status = "REJECTED"

    # Sinh review markdown
    generate_gate_review(
        gate_key_input=gate_key_input,
        feature_slug=feature_slug,
        status=status,
        reviewer=reviewer,
        feedback=feedback
    )

    # Tự động lưu checkpoint
    checkpoint_script = BASE_DIR / "scripts" / "checkpoint.py"
    if checkpoint_script.exists():
        try:
            subprocess.run([
                sys.executable, str(checkpoint_script), "save",
                "--phase", f"gate_{gate_num}",
                "--status", status,
                "--note", f"Gate {gate_num} {status}: {feedback[:50]}"
            ], capture_output=True, text=True)
            print(f"💾 Đã tự động lưu Checkpoint cho Gate {gate_num} (Trạng thái: {status})")
        except Exception as e:
            print(f"⚠️ Không thể lưu checkpoint tự động: {e}")

    return status, feedback


def main():
    parser = argparse.ArgumentParser(description="Sinh biên bản Gate Review & Duyệt tương tác cho AI-Vibe-Coding")
    parser.add_argument("--gate", required=True, help="Số thứ tự hoặc mã Gate (1, 2, 3 hoặc gate_1_client_signoff)")
    parser.add_argument("--feature", default="motocare-booking", help="Slug của feature/specs")
    parser.add_argument("--status", choices=["PENDING", "APPROVED", "REVISION_REQUESTED", "REJECTED"], default="PENDING", help="Trạng thái phê duyệt")
    parser.add_argument("--reviewer", default="Product Owner / Tech Lead", help="Tên hoặc vai trò người ký duyệt")
    parser.add_argument("--feedback", default="", help="Nội dung nhận xét / phản hồi")
    parser.add_argument("--interactive", action="store_true", help="Chạy chế độ duyệt tương tác trực tiếp trên Terminal")

    args = parser.parse_args()

    if args.interactive:
        run_interactive_review(
            gate_key_input=args.gate,
            feature_slug=args.feature,
            reviewer=args.reviewer
        )
    else:
        generate_gate_review(
            gate_key_input=args.gate,
            feature_slug=args.feature,
            status=args.status,
            reviewer=args.reviewer,
            feedback=args.feedback
        )


if __name__ == "__main__":
    main()
