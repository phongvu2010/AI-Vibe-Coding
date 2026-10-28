"""Automated tests for Tactical Agile Fast-Track runner and model routing."""

import json
import sys
from pathlib import Path

import pytest
import yaml

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from fast_track import FastTrackOrchestrator, analyze_task_impact, apply_llm_code_blocks  # noqa: E402
from agent_factory import AgentFactory, ModelRouter  # noqa: E402
from release_bundler import ReleaseBundler  # noqa: E402
from state import SDLCState  # noqa: E402


def test_fast_track_impact_analysis_database():
    """Verify task mentioning database layers is correctly flagged."""
    impact = analyze_task_impact("Thêm cột is_verified vào database bảng users và migration")
    assert impact["database"] is True
    assert any("src/db/" in layer for layer in impact["affected_layers"])
    assert impact["recommended_agent"] == "fast-track-squad"


def test_fast_track_impact_analysis_backend_api():
    """Verify backend API task flags backend layer."""
    impact = analyze_task_impact("Thêm endpoint GET /orders/filter theo status trong FastAPI service")
    assert impact["backend"] is True
    assert any("src/backend/" in layer for layer in impact["affected_layers"])


def test_fast_track_impact_analysis_frontend_web():
    """Verify UI task flags frontend layer."""
    impact = analyze_task_impact("Sửa nút submit button và giao diện form login trên web")
    assert impact["frontend"] is True
    assert any("src/frontend/" in layer for layer in impact["affected_layers"])


def test_fast_track_impact_analysis_mobile():
    """Verify mobile app task flags mobile layer."""
    impact = analyze_task_impact("Fix lỗi render danh sách trên expo mobile app màn hình home")
    assert impact["mobile"] is True
    assert any("src/mobile/" in layer for layer in impact["affected_layers"])


def test_fast_track_impact_analysis_fullstack_multi_layer():
    """Verify fullstack task flags multiple layers appropriately."""
    impact = analyze_task_impact("Thêm trường avatar_url vào db model, backend API và frontend profile screen")
    assert impact["database"] is True
    assert impact["backend"] is True
    assert impact["frontend"] is True
    assert len(impact["affected_layers"]) >= 3


def test_fast_track_model_routing_config():
    """Verify model_router.yaml properly routes fast-track-squad to flash tier."""
    router_path = ROOT_DIR / "config" / "model_router.yaml"
    assert router_path.exists(), "config/model_router.yaml must exist"

    with open(router_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Check routing in agents_allocation
    agents_allocation = data.get("agents_allocation", {})
    assert "fast-track-squad" in agents_allocation, "fast-track-squad must be defined in agents_allocation"
    assert agents_allocation["fast-track-squad"]["tier"] == "flash", "fast-track-squad must route to flash tier"


def test_fast_track_llm_code_block_extraction(tmp_path: Path):
    """Kiểm tra apply_llm_code_blocks bóc tách khối mã và ghi file an toàn."""
    sample_llm_output = """
Dưới đây là bản cập nhật mã nguồn theo yêu cầu:
### FILE: src/backend/app/core/constants.py
```python
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT_SEC = 30
```
"""
    applied = apply_llm_code_blocks(sample_llm_output, base_dir=tmp_path)
    assert "src/backend/app/core/constants.py" in applied
    written = (tmp_path / "src" / "backend" / "app" / "core" / "constants.py").read_text(encoding="utf-8")
    assert "MAX_RETRY_COUNT = 3" in written
    assert "DEFAULT_TIMEOUT_SEC = 30" in written


def test_fast_track_model_routing():
    """Kiểm tra ModelRouter phân bổ đúng tier FLASH cho fast_track_team và ai_team_dev."""
    router = ModelRouter(ROOT_DIR / "config" / "model_router.yaml")
    model, tier = router.get_model_for_team("fast_track_team")
    assert tier == "flash"
    assert "gemini" in model

    alias_model, alias_tier = router.get_model_for_team("ai_team_dev")
    assert alias_tier == "flash"
    assert alias_model == model


def test_subagent_role_routing():
    """Kiểm tra định tuyến chi tiết theo từng subagent_role trong config/model_router.yaml."""
    factory = AgentFactory(ROOT_DIR)

    # Engineering roles: backend_engineer (pro), frontend_engineer (flash), devops_engineer (flash_lite)
    _, be_tier = factory.model_router.get_model_for_team("engineering_team", subagent_role="backend_engineer")
    _, fe_tier = factory.model_router.get_model_for_team("engineering_team", subagent_role="frontend_engineer")
    _, do_tier = factory.model_router.get_model_for_team("engineering_team", subagent_role="devops_engineer")
    assert be_tier == "pro"
    assert fe_tier == "flash"
    assert do_tier == "flash_lite"

    # QA roles: qa_automation (flash), code_reviewer (pro)
    _, qa_runner_tier = factory.model_router.get_model_for_team("qa_team", subagent_role="qa_automation")
    _, qa_review_tier = factory.model_router.get_model_for_team("qa_team", subagent_role="code_reviewer")
    assert qa_runner_tier == "flash"
    assert qa_review_tier == "pro"

    # Fast-Track roles: dev_sage (pro), dev_nova (flash)
    sage_agent = factory.get_subteam("fast_track_team", subagent_role="dev_sage")
    nova_agent = factory.get_subteam("fast_track_team", subagent_role="dev_nova")
    assert getattr(sage_agent, "model_tier", None) == "pro"
    assert getattr(nova_agent, "model_tier", None) == "flash"


def test_producer_scoping():
    """Kiểm tra Producer Remy bóc tách đúng phạm vi ảnh hưởng cho các loại task khác nhau."""
    orchestrator = FastTrackOrchestrator(ROOT_DIR)

    # 1. Order task
    scope_order = orchestrator.scope_task("Bổ sung endpoint lọc order theo status")
    assert any("order" in t for t in scope_order["backend_targets"])
    assert "Remy" in scope_order["producer"]
    assert scope_order["db_migration_needed"] is False
    assert scope_order["primary_role"] == "dev_sage"

    # 2. Database model task
    scope_db = orchestrator.scope_task("Thêm cột discount_code vào bảng orders và tạo DB model")
    assert scope_db["db_migration_needed"] is True
    assert any("alembic" in t or "models" in t for t in scope_db["backend_targets"])

    # 3. Auth task
    scope_auth = orchestrator.scope_task("Sửa lỗi xác thực mật khẩu người dùng trong AuthService")
    assert any("auth" in t or "user" in t for t in scope_auth["backend_targets"])


def test_native_antigravity_agents_frontmatter():
    """Kiểm tra cấu hình chuẩn Native Antigravity 2.0 trong .agents/agents/, .agents/subteams/ và .agents/hooks.json."""
    agents_dir = ROOT_DIR / ".agents" / "agents"
    subteams_dir = ROOT_DIR / ".agents" / "subteams"
    hooks_file = ROOT_DIR / ".agents" / "hooks.json"

    assert agents_dir.exists() and agents_dir.is_dir()
    assert subteams_dir.exists() and subteams_dir.is_dir()
    assert hooks_file.exists()

    expected_agents = {
        "discovery_team.md",
        "architecture_team.md",
        "engineering_team.md",
        "qa_team.md",
        "release_team.md",
        "fast_track_team.md",
        "ai_team_dev.md",
    }
    actual_agents = {p.name for p in agents_dir.glob("*.md")}
    assert expected_agents.issubset(actual_agents)

    for md_file in list(agents_dir.glob("*.md")) + list(subteams_dir.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        assert content.startswith("---"), f"{md_file} phải có YAML frontmatter"
        parts = content.split("---", 2)
        meta = yaml.safe_load(parts[1])
        assert meta.get("name"), f"{md_file} thiếu name"
        assert meta.get("mainAgent") is True, f"{md_file.name} thiếu mainAgent: true"
        assert meta.get("subagent") is True, f"{md_file.name} thiếu subagent: true"
        assert meta.get("commandExecutionPolicy") == "auto", f"{md_file.name} thiếu commandExecutionPolicy: auto"
        tools = meta.get("tools", [])
        if tools is not None:
            assert "view_file" in tools, f"{md_file.name} phải dùng view_file chuẩn Antigravity 2.0"
            assert "read_file" not in tools, f"{md_file.name} còn chứa tool cũ read_file"

    hooks_data = json.loads(hooks_file.read_text(encoding="utf-8"))
    assert any("guardrails" in k or "post" in k or "sdlc" in k for k in hooks_data.keys())


def test_release_bundler_sha256_and_metrics(tmp_path: Path):
    """Kiểm tra ReleaseBundler tính toán SHA-256 thật và đọc số liệu từ test_summary.json."""
    artifacts_dir = tmp_path / "artifacts"
    output_project_dir = tmp_path / "output_project"
    (output_project_dir / "backend").mkdir(parents=True)
    (output_project_dir / "backend" / "main.py").write_text("print('ok')\n", encoding="utf-8")

    qa_dir = artifacts_dir / "04_quality"
    qa_dir.mkdir(parents=True)
    test_summary = qa_dir / "test_summary.json"
    test_summary.write_text(json.dumps({
        "backend_tests": {
            "coverage_percentage": 94.2,
            "failed": 0
        }
    }), encoding="utf-8")

    state = SDLCState(
        project_name="TestReleaseApp",
        raw_requirements="Sample brief",
        artifacts={"test_summary": str(test_summary)}
    )
    bundler = ReleaseBundler(artifacts_dir=artifacts_dir, output_project_dir=output_project_dir)
    zip_path = bundler.bundle_release_package(state)

    assert zip_path.exists()
    manifest_path = artifacts_dir / "05_handover" / "RELEASE_MANIFEST.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["quality_metrics"]["coverage_score"] == "94.2%"
    sha256_hex = manifest["package_archive"]["sha256_checksum"]
    assert len(sha256_hex) == 64
    assert state.artifacts["release_sha256"] == sha256_hex


def test_agent_factory_fast_track_subteam():
    """Kiểm tra AgentFactory khởi tạo thành công Fast-Track subteam và alias ai_team_dev."""
    factory = AgentFactory(ROOT_DIR)
    agent = factory.get_subteam("fast_track_team")
    assert agent is not None
    assert "fast_track" in str(agent).lower() or "Fast-Track" in getattr(agent, "name", "") or "fast-track" in str(agent).lower()

    alias_agent = factory.get_subteam("ai_team_dev")
    assert alias_agent is not None


@pytest.mark.asyncio
async def test_fast_track_filter_orders_scoping_and_patching(tmp_path: Path):
    """Kiểm tra Fast-Track tự động nhận diện phạm vi và áp dụng bản vá filter đơn hàng."""
    fake_root = tmp_path / "project"
    backend_dir = fake_root / "src" / "backend" / "app" / "routers"
    backend_dir.mkdir(parents=True, exist_ok=True)
    tests_dir = fake_root / "src" / "backend" / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)

    orders_router = backend_dir / "orders.py"
    orders_router.write_text("@router.get('/')\ndef list_orders(): pass\n", encoding="utf-8")
    orders_test = tests_dir / "test_orders.py"
    orders_test.write_text("def test_list_orders(): pass\n", encoding="utf-8")

    orchestrator = FastTrackOrchestrator(fake_root)
    scope = orchestrator.scope_task("Bổ sung endpoint filter đơn hàng theo status")
    assert scope["primary_role"] == "dev_sage"
    assert any("order" in target for target in scope["backend_targets"])

    res = await orchestrator.implement_task(scope, "TestProject")
    assert res["task"] == "Bổ sung endpoint filter đơn hàng theo status"
    assert "filter_orders_by_status" in orders_router.read_text(encoding="utf-8")
    assert "test_filter_orders_by_status_endpoint" in orders_test.read_text(encoding="utf-8")


