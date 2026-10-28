@echo off
REM AI-Vibe-Coding: Trình khởi chạy Windows Command Prompt (CMD)
REM Tự động ủy quyền sang run.ps1 với ExecutionPolicy Bypass

set SCRIPT_DIR=%~dp0
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%run.ps1" %*
