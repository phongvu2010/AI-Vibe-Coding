#!/usr/bin/env python3
"""
bundle_release.py
Bộ tự động hóa đóng gói phát hành phần mềm (Automated Release Bundler).
Tạo gói zip hoàn chỉnh, tính toán mã băm SHA256, và xuất bản RELEASE_MANIFEST.json bàn giao cho khách hàng.
"""

import datetime
import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path


def get_git_commit(root: Path) -> str:
    try:
        res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True)
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception:
        pass
    return "uncommitted_local_build"

def calculate_sha256(file_path: Path) -> str:
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest()

def bundle(feature_slug: str, version: str = "1.0.0"):
    root = Path(__file__).resolve().parent.parent
    dist_dir = root / "dist" / "releases"
    dist_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"{feature_slug}_v{version}_{timestamp}.zip"
    zip_path = dist_dir / zip_name

    print(f"📦 [RELEASE BUNDLER] Đang đóng gói bản phát hành cho '{feature_slug}' (v{version})...")

    # Các thư mục và file đưa vào bản phát hành
    include_paths = ["src", "scripts", "docs", "config", "docker-compose.yml", "Makefile", "pyproject.toml", ".env.example"]

    file_manifest = []
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for item in include_paths:
            path = root / item
            if path.is_file():
                arcname = item
                zip_file.write(path, arcname=arcname)
                file_manifest.append({
                    "path": arcname,
                    "sha256": calculate_sha256(path),
                    "size_bytes": path.stat().st_size
                })
            elif path.is_dir():
                for subfile in path.rglob("*"):
                    if subfile.is_file() and not any(p in subfile.parts for p in ["__pycache__", ".pytest_cache", "node_modules", ".git"]):
                        arcname = str(subfile.relative_to(root))
                        zip_file.write(subfile, arcname=arcname)
                        file_manifest.append({
                            "path": arcname,
                            "sha256": calculate_sha256(subfile),
                            "size_bytes": subfile.stat().st_size
                        })

    package_sha256 = calculate_sha256(zip_path)
    git_sha = get_git_commit(root)

    manifest_data = {
        "project": "AI-Vibe-Coding",
        "feature_slug": feature_slug,
        "version": version,
        "release_timestamp": datetime.datetime.now().isoformat(),
        "package_filename": zip_name,
        "package_sha256": package_sha256,
        "git_commit": git_sha,
        "total_files": len(file_manifest),
        "files": file_manifest
    }

    manifest_path = dist_dir / "RELEASE_MANIFEST.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)

    print("✅ [RELEASE BUNDLER] Đóng gói thành công!")
    print(f"   • File zip: {zip_path}")
    print(f"   • SHA256  : {package_sha256}")
    print(f"   • Manifest: {manifest_path}")

def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else "core-release"
    version = sys.argv[2] if len(sys.argv) > 2 else "1.0.0"
    bundle(slug, version)

if __name__ == "__main__":
    main()
