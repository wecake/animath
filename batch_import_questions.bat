@echo off
chcp 65001 >nul
echo ==============================================
echo     题库批量导入 / 批量生成 任务启动
echo ==============================================
cd /d "%~dp0"

:: 激活uv虚拟环境，执行题库脚本
PowerShell -NoProfile -Command ^
"Set-ExecutionPolicy -Scope Process RemoteSigned -Force; ^
.\.venv\Scripts\Activate.ps1; ^
python storyboard_generator.py"

echo.
echo ✅ 题库批量任务执行完毕
pause