@echo off
REM AI-Vibe-Coding: Developer Automation Launcher (CMD Wrapper)
REM Delegates to root run.bat / run.ps1 for 100% compatibility with Multi-Agents-Dev
set SCRIPT_DIR=%~dp0
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%..\run.ps1" %*
