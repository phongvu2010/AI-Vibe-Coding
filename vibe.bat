@echo off
REM AI-Vibe-Coding Windows Launcher
set SCRIPT_DIR=%~dp0
if exist "%SCRIPT_DIR%.venv\Scripts\python.exe" (
    "%SCRIPT_DIR%.venv\Scripts\python.exe" "%SCRIPT_DIR%vibe.py" %*
) else (
    python "%SCRIPT_DIR%vibe.py" %*
)
