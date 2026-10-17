#!/usr/bin/env python3
"""
generate_openapi.py
Xuất bản đặc tả OpenAPI tự động từ ứng dụng FastAPI (OpenAPI Spec Exporter).
Giúp đảm bảo tài liệu API luôn đồng bộ 100% với mã nguồn thật.
"""

import json
import sys
from pathlib import Path

# Thêm root vào sys.path để import được src
root = Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from src.backend.app.main import app  # noqa: E402


def export_openapi():
    root = Path(__file__).resolve().parent.parent
    output_dir = root / "docs" / "specs"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "openapi.json"

    print("📄 [OPENAPI EXPORTER] Đang trích xuất đặc tả OpenAPI từ FastAPI app...")
    schema = app.openapi()

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)

    print(f"✅ [OPENAPI EXPORTER] Đã xuất bản file đặc tả tại: {output_path}")

if __name__ == "__main__":
    export_openapi()
