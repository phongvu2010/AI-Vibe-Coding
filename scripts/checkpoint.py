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
    "pre_clean": "🧹 Chuẩn bị dọn sạch đón đề bài mới",
}

GATE_CONFIGS = {
    "gate_1_prd": {
        "title": "GATE 1: Phê Duyệt PRD & Phạm Vi Dự Án (Client Scope Sign-off)",
        "role": "Product Owner / Client Liaison Lead",
        "description": "Thẩm định phạm vi dự án (In-Scope vs Out-of-Scope), User Stories (Gherkin format) và luồng UI/UX Concept.",
        "search_patterns": ["**/prd.md", "**/ui_ux_spec.md", "**/clarification*.md"],
        "checklist": [
            "Đã phỏng vấn làm rõ các yêu cầu nghiệp vụ cốt lõi (Clarification Q&A).",
            "Phạm vi In-Scope MVP và Out-of-Scope v2.0 được phân ranh giới rõ ràng.",
            "Toàn bộ Acceptance Criteria tuân thủ chuẩn Gherkin (Given-When-Then).",
            "Sơ đồ điều hướng màn hình (Mermaid) và ma trận 5 UI states đã được thiết lập.",
        ],
    },
    "gate_2_architecture": {
        "title": "GATE 2: Phê Duyệt Kiến Trúc & Hợp Đồng Dữ Liệu (Technical Sign-off)",
        "role": "System Architect / Tech Lead",
        "description": "Thẩm định thiết kế phân tầng Clean Architecture, OpenAPI Contract, sơ đồ ERD và mô hình đe dọa STRIDE.",
        "search_patterns": ["**/plan.md", "**/openapi.*", "**/architecture*.md"],
        "checklist": [
            "Kiến trúc phân tầng tuân thủ Clean Architecture (core -> models -> schemas -> repos -> services -> routers).",
            "Đồng bộ chuẩn hóa 100% snake_case trên Database, Backend Schemas và Frontend Types.",
            "Mô hình dữ liệu ERD và Alembic Migrations thiết kế đúng chuẩn quan hệ và indexes.",
            "Hoàn thành mô hình đe dọa bảo mật STRIDE và phân quyền RBAC/ABAC.",
        ],
    },
    "gate_3_deploy": {
        "title": "GATE 3: Cấp Phép Triển Khai & Bàn Giao (Production Readiness Sign-off)",
        "role": "Principal Code Reviewer / QA Lead",
        "description": "Thẩm định kết quả kiểm thử tự động, độ phủ mã nguồn (Coverage >= 80%), tính toàn vẹn Database và audit bảo mật OWASP.",
        "search_patterns": ["**/test-report.md", "**/review-report.md", "**/uat_checklist.md"],
        "checklist": [
            "100% bài kiểm thử PyTest Backend và DB vượt qua (Zero Failures).",
            "Độ phủ kiểm thử Backend đạt tối thiểu >= 80% (pytest-cov pass).",
            "Alembic Database đạt chuẩn Zero Schema Drift (alembic check pass).",
            "Bảng điểm Code Review đạt >= 85/100, 0 phát hiện rò rỉ secret hoặc lỗ hổng OWASP nghiêm trọng.",
        ],
    },
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


def generate_review_gate_artifact(
    gate_key: str,
    status: str,
    reviewer: str,
    note: str,
    project_name: str,
) -> Optional[Path]:
    """Sinh tài liệu Review Gate tương tác để hiển thị trực quan trên Antigravity IDE (Artifacts tab)."""
    if gate_key not in GATE_CONFIGS:
        return None

    cfg = GATE_CONFIGS[gate_key]
    specs_dir = ROOT_DIR / "docs" / "specs"
    specs_dir.mkdir(parents=True, exist_ok=True)
    out_file = specs_dir / f"review_{gate_key}.md"

    # Tìm các file tương ứng trong docs/specs
    matched_files = []
    for pattern in cfg["search_patterns"]:
        matched_files.extend(list(specs_dir.glob(pattern)))

    table_rows = []
    if matched_files:
        for idx, f in enumerate(matched_files, 1):
            try:
                rel = f.relative_to(ROOT_DIR)
            except ValueError:
                rel = f
            size_kb = f.stat().st_size / 1024
            table_rows.append(f"| {idx} | [{f.name}]({rel}) | `{rel}` | {size_kb:.1f} KB | ✅ Sẵn sàng |")
    else:
        table_rows.append("| 1 | Chưa phát hiện file spec liên quan | `docs/specs/` | 0 KB | ⚠️ Cần bổ sung |")

    table_md = "\n".join(table_rows)

    checklist_items = []
    for item in cfg["checklist"]:
        check_mark = "[x]" if status.upper() == "APPROVED" else "[ ]"
        checklist_items.append(f"- {check_mark} {item}")
    checklist_md = "\n".join(checklist_items)

    status_icon = "🟢" if status.upper() == "APPROVED" else "🟡"

    content = f"""# 🚦 CHỐT CHẶN KIỂM SOÁT CHẤT LƯỢNG: {cfg['title']}

> [!IMPORTANT]
> **Dự án:** `{project_name}`  
> **Vai trò người phê duyệt yêu cầu:** `{cfg['role']}`  
> **Mục tiêu chốt chặn:** {cfg['description']}

---

## 📂 1. DANH SÁCH ARTIFACTS ĐỐI CHIẾU
| STT | Tên Tài Liệu | Đường Dẫn Tương Đối | Kích Thước | Trạng Thái |
| :---: | :--- | :--- | :--- | :---: |
{table_md}

---

## 📋 2. KẾT QUẢ PHÊ DUYỆT (DECISION LOG)
- **Trạng thái Gate:** {status_icon} **`{status.upper()}`**
- **Người ký duyệt:** `{reviewer}`
- **Thời gian ghi nhận:** `{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}`
- **Ghi chú & Đánh giá của Tech Lead / PO:**
> {note or "Đạt toàn bộ tiêu chuẩn chốt chặn chất lượng."}

---

## ☑️ 3. BẢNG KIỂM TRA PHÊ DUYỆT (QUALITY CHECKLIST)
{checklist_md}
"""
    out_file.write_text(content, encoding="utf-8")
    print(f"📄 [INTERACTIVE ARTIFACT] Đã tạo tài liệu duyệt trực quan: {out_file.name}")
    return out_file


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

    # Sinh interactive review gate markdown nếu thuộc các chốt chặn Gate
    generate_review_gate_artifact(safe_phase, status, reviewer, note, project_name)

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


def count_loc(directory: Path, extensions: tuple) -> tuple[int, int]:
    """Đếm số file và số dòng code trong thư mục."""
    total_files = 0
    total_lines = 0
    if not directory.exists():
        return 0, 0
    for p in directory.rglob("*"):
        if p.is_file() and p.suffix in extensions and "node_modules" not in str(p) and ".next" not in str(p):
            try:
                lines = len(p.read_text(encoding="utf-8", errors="ignore").splitlines())
                total_files += 1
                total_lines += lines
            except Exception:
                pass
    return total_files, total_lines


def print_status() -> None:
    if not LATEST_FILE.exists():
        print("ℹ️ Chưa có trạng thái checkpoint nào được ghi nhận.")
        print("👉 Gợi ý: Hãy lưu checkpoint đầu tiên bằng: make checkpoint PHASE=discovery")
    else:
        try:
            latest = json.loads(LATEST_FILE.read_text(encoding="utf-8"))
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
        except Exception as e:
            print(f"❌ Không thể đọc trạng thái mới nhất: {e}")

    # Thống kê nhanh sức khỏe mã nguồn (Codebase Health Dashboard)
    be_files, be_lines = count_loc(ROOT_DIR / "src" / "backend", (".py",))
    db_files, db_lines = count_loc(ROOT_DIR / "src" / "db", (".py",))
    fe_files, fe_lines = count_loc(ROOT_DIR / "src" / "frontend" / "src", (".ts", ".tsx", ".js", ".jsx"))
    mb_files, mb_lines = count_loc(ROOT_DIR / "src" / "mobile" / "src", (".ts", ".tsx", ".js", ".jsx"))
    mb_app_f, mb_app_l = count_loc(ROOT_DIR / "src" / "mobile" / "app", (".ts", ".tsx", ".js", ".jsx"))

    specs_files = [p.name for p in (ROOT_DIR / "docs" / "specs").rglob("*.md") if p.is_file()]

    print("\n📊 TỔNG QUAN SỨC KHỎE MÃ NGUỒN (PROJECT HEALTH DASHBOARD):")
    print(f"  • Backend API (FastAPI):       {be_files} files, {be_lines:,} lines of code")
    print(f"  • Database & Models:           {db_files} files, {db_lines:,} lines of code")
    print(f"  • Web Client (Next.js/React):  {fe_files} files, {fe_lines:,} lines of code")
    print(f"  • Mobile App (Expo/React Native): {mb_files + mb_app_f} files, {mb_lines + mb_app_l:,} lines of code")
    print(f"  • Specs & Artifacts:           {len(specs_files)} markdown specs tài liệu")
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

        # [Safety Precaution] Tự động sao lưu dự phòng hiện trạng trước khi khôi phục
        try:
            print("🛡️ [Safety Precaution] Đang tự động lưu snapshot dự phòng 'pre_restore_backup'...")
            pre_backup = create_code_snapshot("pre_restore_backup")
            print(f"   Đã lưu bản phòng ngừa tại: {pre_backup.name}")
        except Exception as e:
            print(f"⚠️ Cảnh báo: Không thể tạo pre-restore backup: {e}")

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
