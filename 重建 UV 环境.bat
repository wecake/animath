@echo off
chcp 65001
title 重建UV环境
rmdir /s /q .venv
uv venv
call .venv\Scripts\activate.bat
uv pip install -r requirements.txt
echo.
echo ✅ 重建完成
pause