#!/usr/bin/env python3
"""
checkpoint.py — Quản lý Trạng thái SDLC, Checkpoints & Khôi phục (Session Resume & Rollback)
Thuộc hệ thống AI-Vibe-Coding (Antigravity 2.0).

Tích hợp tinh hoa State Machine từ Multi-Agents-Dev & Instant Rollback từ AI-Team-Dev:
1. Lưu trữ tiến độ từng Giai đoạn (Phase) và các chốt chặn Quality Gates (G1, G2, G3).
2. Tự động đóng gói Snapshot mã nguồn sạch tương ứng với mỗi checkpoint.
3. Cho phép khôi phục (Rollback) hoặc tiếp tục phiên làm việc (Resume) bất kỳ lúc nào.

Cách sử dụng:
    python scripts/checkpoint.py save --phase gate_1_prd --status APPROVED --note "User duyệt PRD"
    python scripts/checkpoint.py list
    python scripts/checkpoint.py status
    python scripts/checkpoint.py resume
    python scripts/checkpoint.py restore <checkpoint_id>
"""

import argparse
import datetime
import json
import sys
import tarfile
from pathlib import Path
from typing import Dict, List, Optional

# Đảm bảo console UTF-8 trên Windows
if hasattr(sys.stdout, "reconfigure") and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure") and sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
CHECKPOINTS_DIR = ROOT_DIR / "dist" / "checkpoints"
SNAPSHOTS_DIR = ROOT_DIR / "dist" / "snapshots"
LATEST_FILE = CHECKPOINTS_DIR / "LATEST_CHECKPOINT.json"

PHASE_LABELS = {
    "discovery": "1. Discovery & Solutions (Sub-Team 1)",
    "gate_1_prd": "GATE 1: Client Scope & PRD Sign-off",
    "architecture": "2. Architecture & Planning (Sub-Team 2)",
    "gate_2_architecture": "GATE 2: Technical & Contract Sign-off",
    "engineering": "3. Core Engineering 2-Wave (Sub-Team 3)",
    "qa_verification": "4. QA & Security Audit (Sub-Team 4)",
    "gate_3_deploy": "GATE 3: Production Readiness Sign-off",
    "release_handover": "5. Release & Client Handover (Sub-Team 5)",
    "completed": "✅ Hoàn tất toàn bộ chu trình SDLC",
}

EXCLUDE_DIRS = {
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "node_modules",
    ".next",
    ".expo",
    ".git",
    "dist",
    "build",
}

EXCLUDE_EXTS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".sqlite",
    ".sqlite3",
    ".db",
    ".log",
    ".tmp",
    ".DS_Store",
}


def should_include_file(file_path: Path) -> bool:
    for part in file_path.parts:
        if part in EXCLUDE_DIRS:
            return False
    if file_path.suffix in EXCLUDE_EXTS:
        return False
    return True


def create_code_snapshot(tag: str) -> Path:
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"snapshot_{tag}_{timestamp}.tar.gz"
    archive_path = SNAPSHOTS_DIR / archive_name

    include_dirs = ["src", "config", "docs", "scripts"]

    def filter_tar(tarinfo):
        path_obj = Path(tarinfo.name)
        if not should_include_file(path_obj):
            return None
        return tarinfo

    with tarfile.open(archive_path, "w:gz") as tar:
        for item in include_dirs:
            item_path = ROOT_DIR / item
            if item_path.exists():
                tar.add(item_path, arcname=item, filter=filter_tar)

    return archive_path


def get_project_name() -> str:
    profile_path = ROOT_DIR / "config" / "company_profile.yaml"
    if profile_path.exists():
        try:
            import yaml
            data = yaml.safe_load(profile_path.read_text(encoding="utf-8")) or {}
            return data.get("company", {}).get("name", "AI-Vibe-Coding Project")
        except Exception:
            pass
    return "AI-Vibe-Coding Project"


def save_checkpoint(
    phase: str,
    status: str = "APPROVED",
    reviewer: str = "Tech Lead",
    note: str = "",
    project: Optional[str] = None,
) -> Path:
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    project_name = project or get_project_name()

    safe_phase = phase.lower().replace(" ", "_")
    cp_id = f"CP_{timestamp}_{safe_phase}"
    json_path = CHECKPOINTS_DIR / f"{cp_id}.json"

    print(f"💾 Đang tạo Checkpoint '{cp_id}' cho Phase [{PHASE_LABELS.get(safe_phase, safe_phase)}]...")

    # Tạo snapshot code
    snapshot_archive = create_code_snapshot(safe_phase)

    # Thu thập danh sách artifacts hiện hữu
    artifacts = []
    specs_dir = ROOT_DIR / "docs" / "specs"
    if specs_dir.exists():
        for f in specs_dir.rglob("*.md"):
            artifacts.append(str(f.relative_to(ROOT_DIR)))

    checkpoint_data = {
        "checkpoint_id": cp_id,
        "project_name": project_name,
        "phase": safe_phase,
        "phase_label": PHASE_LABELS.get(safe_phase, safe_phase),
        "status": status.upper(),
        "reviewer": reviewer,
        "note": note or f"Checkpoint tại {PHASE_LABELS.get(safe_phase, safe_phase)}",
        "timestamp": datetime.datetime.now().isoformat(),
        "snapshot_file": str(snapshot_archive.relative_to(ROOT_DIR)),
        "artifacts_count": len(artifacts),
        "artifacts": artifacts[:10],
    }

    json_path.write_text(json.dumps(checkpoint_data, indent=2, ensure_ascii=False), encoding="utf-8")
    LATEST_FILE.write_text(json.dumps(checkpoint_data, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✅ [CHECKPOINT SAVED] Đã lưu thành công checkpoint tại: {json_path.name}")
    print(f"📦 [CODE SNAPSHOT] Mã nguồn được lưu trữ tại: {snapshot_archive.name}")
    return json_path


def list_checkpoints() -> List[Dict]:
    if not CHECKPOINTS_DIR.exists():
        print("ℹ️ Chưa có checkpoint nào được lưu.")
        return []

    checkpoints = []
    for file in sorted(CHECKPOINTS_DIR.glob("CP_*.json"), reverse=True):
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            checkpoints.append(data)
        except Exception:
            continue

    if not checkpoints:
        print("ℹ️ Chưa có checkpoint nào được lưu.")
        return []

    print("=" * 85)
    print(f"📋 DANH SÁCH CHECKPOINTS ĐÃ LƯU ({len(checkpoints)} checkpoints)")
    print("=" * 85)
    print(f"{'Mã Checkpoint':<28} | {'Giai đoạn (Phase)':<25} | {'Trạng thái':<10} | {'Thời gian'}")
    print("-" * 85)

    for cp in checkpoints:
        cp_id = cp.get("checkpoint_id", "")
        phase = cp.get("phase", "")
        status = cp.get("status", "APPROVED")
        ts = cp.get("timestamp", "")[:19].replace("T", " ")
        print(f"{cp_id:<28} | {phase:<25} | {status:<10} | {ts}")

    print("=" * 85)
    return checkpoints


def print_status() -> None:
    if not LATEST_FILE.exists():
        print("ℹ️ Chưa có trạng thái checkpoint nào được ghi nhận.")
        print("👉 Gợi ý: Hãy lưu checkpoint đầu tiên bằng: make checkpoint PHASE=discovery")
        return

    try:
        latest = json.loads(LATEST_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Không thể đọc trạng thái mới nhất: {e}")
        return

    print("=" * 72)
    print("📍 TRẠNG THÁI TIẾN TRÌNH SDLC HIỆN TẠI (AI-Vibe-Coding)")
    print("=" * 72)
    print(f"• Dự án:          {latest.get('project_name')}")
    print(f"• Checkpoint ID:  {latest.get('checkpoint_id')}")
    print(f"• Giai đoạn:      {latest.get('phase_label')}")
    print(f"• Trạng thái:     {latest.get('status')} (Bởi: {latest.get('reviewer')})")
    print(f"• Thời gian:      {latest.get('timestamp')[:19].replace('T', ' ')}")
    print(f"• Ghi chú:        {latest.get('note')}")
    print(f"• File Snapshot:  {latest.get('snapshot_file')}")
    print("=" * 72)


def print_resume_guide() -> None:
    if not LATEST_FILE.exists():
        print("ℹ️ Chưa có phiên làm việc nào để tiếp tục.")
        print("👉 Bắt đầu dự án mới với Sub-Team 1: Triệu hồi @discovery-squad hoặc @lead-ba!")
        return

    latest = json.loads(LATEST_FILE.read_text(encoding="utf-8"))
    phase = latest.get("phase", "")
    print_status()

    print("\n🧭 HƯỚNG DẪN TIẾP TỤC PHIÊN LÀM VIỆC (RESUME PLAYBOOK):")
    if phase in ["discovery", "gate_1_prd"]:
        print("👉 Giai đoạn tiếp theo: SUB-TEAM 2 (Architecture & Planning Squad)")
        print("   Hãy gọi: '@architecture-squad hãy thiết kế kiến trúc và hợp đồng dữ liệu cho PRD vừa duyệt!'")
    elif phase in ["architecture", "gate_2_architecture"]:
        print("👉 Giai đoạn tiếp theo: SUB-TEAM 3 (Core Engineering Squad - Wave 1)")
        print("   Hãy gọi: '@dev-squad bắt đầu lập trình Wave 1 (db-dev + frontend-dev) theo plan.md!'")
    elif phase == "engineering":
        print("👉 Giai đoạn tiếp theo: SUB-TEAM 4 (QA & Security Squad)")
        print("   Hãy gọi: '@qa-squad thực thi kiểm thử 5 tầng và thẩm định chất lượng mã nguồn qua make smoke!'")
    elif phase in ["qa_verification", "gate_3_deploy"]:
        print("👉 Giai đoạn tiếp theo: SUB-TEAM 5 (Release & Client Handover Squad)")
        print("   Hãy gọi: '@release-squad đóng gói bản phát hành và soạn tài liệu bàn giao qua make release!'")
    elif phase == "release_handover":
        print("🎉 Dự án đã sẵn sàng bàn giao! Chạy 'make docker-up' để nghiệm thu ứng dụng.")
    else:
        print("👉 Bạn có thể tiếp tục tương tác cùng Tech Lead trên Chat Canvas.")


def restore_checkpoint(checkpoint_id: str) -> bool:
    cp_file = CHECKPOINTS_DIR / f"{checkpoint_id}.json"
    if not cp_file.exists():
        # Thử tìm kiếm mờ
        matches = list(CHECKPOINTS_DIR.glob(f"*{checkpoint_id}*.json"))
        if matches:
            cp_file = matches[0]
        else:
            print(f"❌ Lỗi: Không tìm thấy checkpoint '{checkpoint_id}'.")
            return False

    try:
        data = json.loads(cp_file.read_text(encoding="utf-8"))
        snapshot_rel = data.get("snapshot_file")
        snapshot_path = ROOT_DIR / snapshot_rel

        if not snapshot_path.exists():
            print(f"❌ Lỗi: Tệp snapshot '{snapshot_path}' không tồn tại.")
            return False

        print(f"🔄 Đang khôi phục mã nguồn và trạng thái về Checkpoint '{data['checkpoint_id']}'...")
        print(f"📦 Giai đoạn: {data.get('phase_label')}")

        with tarfile.open(snapshot_path, "r:gz") as tar:
            tar.extractall(path=ROOT_DIR)

        LATEST_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"✅ [RESTORE COMPLETED] Khôi phục thành công toàn bộ mã nguồn về Checkpoint '{data['checkpoint_id']}'!")
        return True
    except Exception as e:
        print(f"❌ Lỗi khi khôi phục checkpoint: {e}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Quản lý SDLC Checkpoints & Session Resume cho AI-Vibe-Coding")
    subparsers = parser.add_subparsers(dest="command", help="Lệnh thực thi")

    # save
    save_parser = subparsers.add_parser("save", help="Lưu checkpoint mới kèm snapshot mã nguồn")
    save_parser.add_argument("--phase", required=True, choices=list(PHASE_LABELS.keys()), help="Giai đoạn SDLC hiện tại")
    save_parser.add_argument("--status", default="APPROVED", choices=["APPROVED", "PENDING", "REVISION_REQUESTED"], help="Trạng thái chốt chặn")
    save_parser.add_argument("--reviewer", default="Tech Lead", help="Người/Tác tử thực hiện thẩm định")
    save_parser.add_argument("--note", default="", help="Ghi chú chi tiết cho checkpoint")
    save_parser.add_argument("--project", default=None, help="Tên dự án tùy chọn")

    # list
    subparsers.add_parser("list", help="Liệt kê toàn bộ các checkpoint đã lưu")

    # status
    subparsers.add_parser("status", help="Xem trạng thái checkpoint mới nhất")

    # resume
    subparsers.add_parser("resume", help="Xem hướng dẫn tiếp tục phiên làm việc đang dang dở")

    # restore
    restore_parser = subparsers.add_parser("restore", help="Khôi phục mã nguồn và trạng thái về checkpoint cụ thể")
    restore_parser.add_argument("checkpoint_id", help="Mã ID của checkpoint cần khôi phục")

    args = parser.parse_args()

    if args.command == "save":
        save_checkpoint(
            phase=args.phase,
            status=args.status,
            reviewer=args.reviewer,
            note=args.note,
            project=args.project,
        )
        return 0
    elif args.command == "list":
        list_checkpoints()
        return 0
    elif args.command == "status":
        print_status()
        return 0
    elif args.command == "resume":
        print_resume_guide()
        return 0
    elif args.command == "restore":
        success = restore_checkpoint(args.checkpoint_id)
        return 0 if success else 1
    else:
        print_status()
        return 0


if __name__ == "__main__":
    sys.exit(main())
