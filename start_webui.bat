@echo off
chcp 65001 >nul
cd /d "%~dp0"

PowerShell -NoProfile -Command ^
"Set-ExecutionPolicy -Scope Process RemoteSigned -Force; ^
.\.venv\Scripts\Activate.ps1; ^
python run_webui.py"

pause