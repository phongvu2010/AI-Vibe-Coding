import sys
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def test_company_profile_exists_and_valid():
    """Kiểm tra tính hợp lệ của cấu hình company_profile.yaml."""
    cfg_file = BASE_DIR / "config" / "company_profile.yaml"
    assert cfg_file.exists(), "config/company_profile.yaml không tồn tại!"
    data = yaml.safe_load(cfg_file.read_text(encoding="utf-8"))
    assert "company" in data
    assert "engineering_standards" in data
    assert "guardrails" in data


def test_model_router_tiers():
    """Kiểm tra ma trận model_router.yaml phân bổ đúng tiers."""
    cfg_file = BASE_DIR / "config" / "model_router.yaml"
    assert cfg_file.exists(), "config/model_router.yaml không tồn tại!"
    data = yaml.safe_load(cfg_file.read_text(encoding="utf-8"))
    assert "agents_allocation" in data
    routing = data["agents_allocation"]
    # Kiểm tra các role then chốt
    assert "lead-ba" in routing
    assert "system-architect" in routing
    assert "qa-tester" in routing
    assert "code-reviewer" in routing


def test_spec_templates_exist():
    """Kiểm tra sự hiện diện của 4 spec templates chuẩn."""
    templates_dir = BASE_DIR / "templates" / "specs"
    assert templates_dir.exists(), "templates/specs không tồn tại!"
    expected_templates = [
        "prd-template.md",
        "plan-template.md",
        "test-report-template.md",
        "review-report-template.md",
    ]
    for tmpl in expected_templates:
        assert (templates_dir / tmpl).exists(), f"Thiếu template: {tmpl}"


def test_all_registered_subagents_have_spec_files():
    """Kiểm tra toàn bộ 15 subagents và squads đều có file định nghĩa markdown."""
    agents_dir = BASE_DIR / ".agents" / "agents"
    assert agents_dir.exists()

    required_agents = [
        "account-lead.md", "lead-ba.md", "uiux-designer.md",
        "system-architect.md", "security-architect.md", "tech-planner.md",
        "db-dev.md", "frontend-dev.md", "backend-dev.md", "devops-engineer.md",
        "qa-tester.md", "code-reviewer.md",
        "release-engineer.md", "tech-writer.md", "handover-lead.md",
        "fast-track-squad.md"
    ]
    for agent_file in required_agents:
        assert (agents_dir / agent_file).exists(), f"Thiếu file agent: {agent_file}"


def test_skills_catalog():
    """Kiểm tra các skills cốt lõi đều hiện diện đầy đủ."""
    skills_dir = BASE_DIR / ".agents" / "skills"
    assert skills_dir.exists()

    required_skills = [
        "requirement_elicitation",
        "gherkin_generator",
        "threat_modeling_stride",
        "contract_synchronizer",
        "db_sqlalchemy_alembic",
        "backend_fastapi_clean",
        "frontend_nextjs_tailwind",
        "frontend-vite",
        "mobile_react_native_expo",
        "test_runner_suite",
        "code_review_evaluator",
        "secret_scanner",
        "release_packager",
        "uat_checklist_builder"
    ]
    for skill in required_skills:
        assert (skills_dir / skill / "SKILL.md").exists(), f"Thiếu SKILL.md tại: {skill}"


def test_tech_lead_profile_exists():
    """Kiểm tra sự hiện diện của tech_lead_profile.yaml."""
    profile = BASE_DIR / "config" / "tech_lead_profile.yaml"
    assert profile.exists(), "config/tech_lead_profile.yaml không tồn tại!"
    data = yaml.safe_load(profile.read_text(encoding="utf-8"))
    assert "tech_lead" in data
    assert "familiar_stacks" in data["tech_lead"]


def test_scoped_agents_md_rules():
    """Kiểm tra các quy tắc AGENTS.md phân tầng theo thư mục src/*/."""
    layers = ["backend", "frontend", "mobile", "db"]
    for layer in layers:
        rule_file = BASE_DIR / "src" / layer / "AGENTS.md"
        assert rule_file.exists(), f"Thiếu scoped rule file: src/{layer}/AGENTS.md"


def test_subteams_definition_files():
    """Kiểm tra 6 subteams trong .agents/subteams/."""
    subteams_dir = BASE_DIR / ".agents" / "subteams"
    assert subteams_dir.exists(), ".agents/subteams không tồn tại!"
    expected = [
        "subteam_1_discovery.md",
        "subteam_2_architecture.md",
        "subteam_3_engineering.md",
        "subteam_4_qa.md",
        "subteam_5_release.md",
        "subteam_6_fast_track.md"
    ]
    for subteam in expected:
        assert (subteams_dir / subteam).exists(), f"Thiếu file: {subteam}"


def test_playbook_and_e2e_suite_exist():
    """Kiểm tra TEAM_PLAYBOOK.md và Frontend headless E2E suite."""
    assert (BASE_DIR / "TEAM_PLAYBOOK.md").exists(), "Thiếu TEAM_PLAYBOOK.md!"
    assert (BASE_DIR / "src" / "frontend" / "scripts" / "run_e2e_tests.cjs").exists(), "Thiếu run_e2e_tests.cjs!"


def test_subteam_aliases_exist():
    """Kiểm tra sự hiện diện của các file bí danh subteams (@..._team) tương thích ngược."""
    agents_dir = BASE_DIR / ".agents" / "agents"
    expected_aliases = [
        "discovery_team.md",
        "architecture_team.md",
        "engineering_team.md",
        "qa_team.md",
        "release_team.md",
        "fast_track_team.md",
        "ai_team_dev.md",
    ]
    for alias in expected_aliases:
        assert (agents_dir / alias).exists(), f"Thiếu alias agent file: {alias}"


def test_universal_api_client_capabilities():
    """Kiểm tra tính năng của Universal Typed API Client trong frontend."""
    client_file = BASE_DIR / "src" / "frontend" / "src" / "lib" / "api" / "client.ts"
    assert client_file.exists(), "src/frontend/src/lib/api/client.ts không tồn tại!"
    content = client_file.read_text(encoding="utf-8")
    assert "getApiBaseUrl" in content
    assert "apiRequest" in content
    assert "apiClient" in content
    assert "clearClientApiCache" in content
    assert "checkApiHealth" in content


def test_auto_healing_prompt_generation():
    """Kiểm tra hàm sinh prompt Auto-Healing cho Dev trong parse_traceback.py."""
    from scripts.parse_traceback import format_fix_prompt_for_dev
    mock_defect = {
        "file_path": "src/backend/app/api/v1/users.py",
        "line": 15,
        "test_name": "test_get_user_not_found",
        "error_message": "AssertionError: 404 != 200",
    }
    prompt = format_fix_prompt_for_dev(mock_defect)
    assert "MICRO-PATCH GUARDRAILS" in prompt
    assert "src/backend/app/api/v1/users.py" in prompt


def test_sdlc_pydantic_schemas():
    """Kiểm tra tính hợp lệ của các Pydantic Schemas trong scripts/schemas.py."""
    from scripts.schemas import (
        DiscoveryResult, UserStoryModel, ArchitectureResult,
        DefectTicket, GateDecision, GateDecisionStatus
    )
    story = UserStoryModel(
        id="US-01",
        title="Đăng ký tài khoản",
        as_a="Khách hàng",
        i_want_to="Đăng ký tài khoản",
        so_that="Tôi có thể đặt lịch",
        acceptance_criteria_gherkin="Scenario: Thành công\nGiven...\nWhen...\nThen..."
    )
    assert story.id == "US-01"

    decision = GateDecision(
        gate_id="gate_1_client_signoff",
        reviewer="Product Owner",
        status=GateDecisionStatus.APPROVED
    )
    assert decision.status == GateDecisionStatus.APPROVED


def test_heuristic_auto_patcher():
    """Kiểm tra động cơ Heuristic Auto-Healing (Zero-Token Rule Patcher)."""
    from scripts.auto_heal_heuristics import HeuristicAutoPatcher
    patcher = HeuristicAutoPatcher()

    # Test patch hardcoded secret
    dummy_code = 'SECRET_KEY = "my_super_secret_key_12345"'
    new_code, patched = patcher.patch_hardcoded_secrets(dummy_code)
    assert patched is True
    assert 'os.getenv("SECRET_KEY"' in new_code

    # Test patch UUID collision
    dummy_code2 = 'order_id = f"ORD_{count + 1}"'
    new_code2, patched2 = patcher.patch_uuid_collision(dummy_code2)
    assert patched2 is True
    assert "uuid.uuid4()" in new_code2


def test_headless_runner_and_gate_interactive():
    """Kiểm tra sự hiện diện của run_headless_sdlc.py và generate_gate_review.py."""
    assert (BASE_DIR / "scripts" / "run_headless_sdlc.py").exists(), "Thiếu run_headless_sdlc.py!"
    assert (BASE_DIR / "scripts" / "generate_gate_review.py").exists(), "Thiếu generate_gate_review.py!"


def test_makefile_extended_targets():
    """Kiểm tra các targets mở rộng và aliases trong Makefile."""
    makefile_content = (BASE_DIR / "Makefile").read_text(encoding="utf-8")
    expected_targets = [
        "subteams:",
        "test-examples:",
        "docker-build:",
        "auto-heal:",
        "gate-interactive:",
        "check-contracts:",
        "check-migrations:",
        "setup-nextjs:",
        "setup-vite:",
        "setup-mobile:",
    ]
    for target in expected_targets:
        assert target in makefile_content, f"Thiếu target trong Makefile: {target}"


def test_adaptive_code_synthesizer(tmp_path: Path):
    """Kiểm tra AdaptiveCodeSynthesizer sinh đúng bộ khung Clean Architecture 5 tầng."""
    sys.path.insert(0, str(BASE_DIR / "scripts"))
    from synthesis_engine import AdaptiveCodeSynthesizer, analyze_requirements

    domain_info = analyze_requirements(
        "Cần làm ứng dụng đặt lịch cắt tóc tối đa 3 khách mỗi giờ",
        project_name="BarberShop",
        platform="mobile"
    )
    assert domain_info["project_name"] == "BarberShop"
    assert domain_info["max_slot"] == 3

    synthesizer = AdaptiveCodeSynthesizer(tmp_path)
    synthesizer.synthesize_all(domain_info)

    # Kiểm tra cấu trúc backend
    assert (tmp_path / "backend" / "app" / "core" / "config.py").exists()
    assert (tmp_path / "backend" / "app" / "models" / "order.py").exists()
    assert (tmp_path / "backend" / "app" / "routers" / "orders.py").exists()
    assert (tmp_path / "backend" / "alembic" / "env.py").exists()

    # Kiểm tra cấu trúc frontend/mobile & runners độc lập
    assert (tmp_path / "frontend" / "types.ts").exists()
    assert (tmp_path / "frontend" / "__tests__" / "App.test.tsx").exists()
    assert (tmp_path / "frontend" / "run_tests.cjs").exists()
    assert (tmp_path / "frontend" / "run_e2e_tests.cjs").exists()

    # Kiểm tra cấu trúc infra
    assert (tmp_path / "infra" / "Dockerfile.backend").exists()
    assert (tmp_path / "infra" / "docker-compose.yml").exists()


def test_integrated_advanced_capabilities(tmp_path: Path):
    """Kiểm tra các tính năng nâng cao kế thừa từ Multi-Agents-Dev & AI-Team-Dev."""
    # 1. Kiểm tra Secret Scanner 7 regex patterns
    secret_skill_content = (BASE_DIR / ".agents" / "skills" / "secret_scanner" / "SKILL.md").read_text(encoding="utf-8")
    assert "OpenAI / Anthropic Keys" in secret_skill_content
    assert "Google API Keys" in secret_skill_content
    assert "GitHub Personal Tokens" in secret_skill_content
    assert "Private Keys & Certificates" in secret_skill_content
    assert "[CRITICAL]" in secret_skill_content

    # 2. Kiểm tra Web Frontend Synthesis
    from scripts.synthesis_engine import AdaptiveCodeSynthesizer
    synth = AdaptiveCodeSynthesizer(tmp_path)
    synth.synthesize_frontend_web({
        "project_name": "WebShop",
        "primary_entity": "Product",
        "order_entity": "Order",
        "primary_label": "Sản phẩm",
        "unit_name": "cái",
        "default_price": 50000.0,
        "max_slot": 5,
        "rule_desc": "Giới hạn 5 đơn"
    })
    fe_dir = tmp_path / "frontend"
    assert (fe_dir / "src" / "components" / "Navbar.tsx").exists()
    assert (fe_dir / "src" / "components" / "CatalogView.tsx").exists()
    assert (fe_dir / "src" / "components" / "BookingForm.tsx").exists()
    assert (fe_dir / "src" / "components" / "OrderTracker.tsx").exists()
    assert (fe_dir / "src" / "store" / "appStore.ts").exists()
    assert (fe_dir / "run_tests.cjs").exists()
    assert (fe_dir / "run_e2e_tests.cjs").exists()

    # 3. Kiểm tra AutoHealingCoordinator
    from scripts.auto_healing import AutoHealingCoordinator
    from scripts.schemas import DefectTicket
    coordinator = AutoHealingCoordinator(max_iterations=2)
    assert coordinator.max_iterations == 2
    dummy_ticket = DefectTicket(
        id="DEF-01",
        target_team="backend",
        file_path="app/core/config.py",
        issue_description="Hardcoded secret detected",
        suggested_fix="Use os.getenv()"
    )
    prompt = coordinator.format_fix_prompt_for_dev(dummy_ticket, 'SECRET_KEY = "123"')
    assert "DEF-01" in prompt


def test_unified_template_enhancements():
    """Kiểm tra các tính năng nâng cao hợp nhất từ AI-Team-Dev và Multi-Agents-Dev."""
    skills_dir = BASE_DIR / ".agents" / "skills"
    assert skills_dir.exists(), "Thư mục skills không tồn tại!"

    # 1. Kiểm tra hàm bóc tách plan matrix và kiểm tra camelCase trong verify_contracts
    from scripts.verify_contracts import extract_plan_matrix_fields, is_camel_case, is_snake_case
    plan_path = BASE_DIR / "docs" / "specs" / "motocare-booking" / "plan.md"
    assert plan_path.exists()
    fields = extract_plan_matrix_fields(plan_path)
    assert len(fields) >= 5, "extract_plan_matrix_fields phải bóc tách được các trường từ motocare-booking/plan.md"
    assert is_camel_case("userEmail") is True
    assert is_camel_case("user_email") is False
    assert is_snake_case("user_email") is True

    # 3. Kiểm tra User Guide có phần ClinicCare Walkthrough
    user_guide = (BASE_DIR / "USER_GUIDE.md").read_text(encoding="utf-8")
    assert "ClinicCare" in user_guide
    assert "Gate 1" in user_guide and "Gate 2" in user_guide and "Gate 3" in user_guide

    # 4. Kiểm tra Team Playbook có Circuit Breaker Escalation
    playbook = (BASE_DIR / "TEAM_PLAYBOOK.md").read_text(encoding="utf-8")
    assert "CIRCUIT BREAKER ESCALATION" in playbook
    assert "SELF-HEALING ACTION REQUIRED" in playbook

    # 5. Kiểm tra 100% Agent Markdown Files đều có mainAgent: true & subagent: true
    import yaml
    agents_dir = BASE_DIR / ".agents" / "agents"
    for md_file in agents_dir.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        assert content.startswith("---"), f"{md_file.name} thiếu YAML frontmatter"
        parts = content.split("---", 2)
        meta = yaml.safe_load(parts[1])
        assert meta.get("mainAgent") is True, f"{md_file.name} thiếu mainAgent: true"
        assert meta.get("subagent") is True, f"{md_file.name} thiếu subagent: true"

    # 6. Kiểm tra hooks.json có đầy đủ checkpoint reminder và guardrails
    hooks_file = BASE_DIR / ".agents" / "hooks.json"
    import json
    hooks_data = json.loads(hooks_file.read_text(encoding="utf-8"))
    assert "sdlc-checkpoint-reminder" in hooks_data, "hooks.json thiếu sdlc-checkpoint-reminder"
    assert "vibe-coding-guardrails-reminder" in hooks_data, "hooks.json thiếu vibe-coding-guardrails-reminder"

    # 7. Kiểm tra Quy ước phân vùng hồ sơ trong USER_GUIDE.md
    assert "Quy Ước Phân Vùng Lưu Trữ Hồ Sơ & Giao Phẩm" in user_guide
    assert "01_discovery" in user_guide and "05_handover" in user_guide





