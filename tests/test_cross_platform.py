import ast
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def test_gitattributes_configuration():
    """Kiểm tra cấu hình .gitattributes bảo đảm chuẩn hóa Line Endings (LF)."""
    gitattributes_file = BASE_DIR / ".gitattributes"
    assert gitattributes_file.exists(), "Tập tin .gitattributes không tồn tại ở thư mục gốc!"
    content = gitattributes_file.read_text(encoding="utf-8")
    assert "*.sh text eol=lf" in content
    assert "Dockerfile* text eol=lf" in content
    assert "* text=auto" in content


def test_scripts_file_io_uses_utf8_encoding():
    """Kiểm tra tĩnh AST toàn bộ mã nguồn scripts bảo đảm luôn khai báo encoding='utf-8'."""
    py_files = list((BASE_DIR / "scripts").rglob("*.py"))
    assert len(py_files) > 0

    for py_file in py_files:
        code = py_file.read_text(encoding="utf-8")
        tree = ast.parse(code, filename=str(py_file))
        for node in ast.walk(tree):
            # Kiểm tra write_text
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "write_text":
                has_enc = any(kw.arg == "encoding" for kw in node.keywords)
                assert has_enc, f"Phát hiện write_text thiếu encoding tại {py_file.name}:{node.lineno}"

            # Kiểm tra read_text
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "read_text":
                has_enc = any(kw.arg == "encoding" for kw in node.keywords)
                assert has_enc, f"Phát hiện read_text thiếu encoding tại {py_file.name}:{node.lineno}"

            # Kiểm tra open() cho text mode
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "open":
                has_enc = any(kw.arg == "encoding" for kw in node.keywords)
                is_binary = any(isinstance(a, ast.Constant) and "b" in str(a.value) for a in node.args[1:])
                is_binary = is_binary or any(kw.arg == "mode" and isinstance(kw.value, ast.Constant) and "b" in str(kw.value.value) for kw in node.keywords)
                if not is_binary:
                    assert has_enc, f"Phát hiện open() text mode thiếu encoding='utf-8' tại {py_file.name}:{node.lineno}"


def test_all_file_io_uses_utf8_encoding():
    """Kiểm tra tĩnh AST toàn bộ mã nguồn orchestrator & src bảo đảm luôn khai báo encoding='utf-8'."""
    py_files = [
        f for f in list((BASE_DIR / "orchestrator").rglob("*.py")) + list((BASE_DIR / "src").rglob("*.py"))
        if "__pycache__" not in str(f)
    ]
    assert len(py_files) > 0

    for py_file in py_files:
        code = py_file.read_text(encoding="utf-8")
        tree = ast.parse(code, filename=str(py_file))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "write_text":
                has_enc = any(kw.arg == "encoding" for kw in node.keywords)
                assert has_enc, f"Phát hiện write_text thiếu encoding tại {py_file.name}:{node.lineno}"

            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "read_text":
                has_enc = any(kw.arg == "encoding" for kw in node.keywords)
                assert has_enc, f"Phát hiện read_text thiếu encoding tại {py_file.name}:{node.lineno}"

            # Kiểm tra open() cho text mode
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "open":
                has_enc = any(kw.arg == "encoding" for kw in node.keywords)
                is_binary = any(isinstance(a, ast.Constant) and "b" in str(a.value) for a in node.args[1:])
                is_binary = is_binary or any(kw.arg == "mode" and isinstance(kw.value, ast.Constant) and "b" in str(kw.value.value) for kw in node.keywords)
                if not is_binary:
                    assert has_enc, f"Phát hiện open() text mode thiếu encoding='utf-8' tại {py_file.name}:{node.lineno}"


def test_windows_powershell_toolkit_exists():
    """Kiểm tra sự hiện diện của PowerShell Toolkit (run.ps1 & scripts/dev.ps1) và thiết lập UTF-8."""
    run_ps1 = BASE_DIR / "run.ps1"
    assert run_ps1.exists(), "run.ps1 không tồn tại ở thư mục gốc!"
    content_run = run_ps1.read_text(encoding="utf-8")
    assert "PYTHONUTF8" in content_run, "run.ps1 cần kích hoạt PYTHONUTF8 cho Windows!"

    dev_ps1 = BASE_DIR / "scripts" / "dev.ps1"
    assert dev_ps1.exists(), "scripts/dev.ps1 không tồn tại!"
    content_dev = dev_ps1.read_text(encoding="utf-8")
    assert "PYTHONUTF8" in content_dev, "scripts/dev.ps1 cần kích hoạt PYTHONUTF8 cho Windows!"
    assert "smoke" in content_dev
    assert "task" in content_dev
    assert "checkpoint" in content_dev
    assert "run-backend" in content_dev
    assert "clean-project" in content_dev
    assert "clean-skeleton" in content_dev


def test_qa_phase_cross_platform_jest_resolution():
    """Kiểm tra logic giải quyết Jest Runner trong qa_phase.py hỗ trợ jest.cmd trên Windows."""
    qa_phase_file = BASE_DIR / "scripts" / "workflows" / "qa_phase.py"
    assert qa_phase_file.exists(), "qa_phase.py không tồn tại!"
    content = qa_phase_file.read_text(encoding="utf-8")
    assert "jest.cmd" in content
    assert "utf-8" in content.lower()


def test_alembic_and_init_db_synchronization():
    """Kiểm tra template database và migration_manager có hàm stamp_head và tự phục hồi khi bảng đã tồn tại."""
    synth_file = BASE_DIR / "scripts" / "synthesis_engine.py"
    assert synth_file.exists(), "synthesis_engine.py không tồn tại!"
    content = synth_file.read_text(encoding="utf-8")
    assert "def stamp_head()" in content
    assert "already exists" in content
    assert "stamp_head()" in content
