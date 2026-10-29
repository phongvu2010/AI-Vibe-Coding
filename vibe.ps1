# AI-Vibe-Coding PowerShell Launcher
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPython = Join-Path $ScriptDir ".venv\Scripts\python.exe"

if (Test-Path $VenvPython) {
    & $VenvPython (Join-Path $ScriptDir "vibe.py") $args
} else {
    python (Join-Path $ScriptDir "vibe.py") $args
}
