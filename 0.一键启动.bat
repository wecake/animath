@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ==================================
echo  MathAnimeOS 一键启动脚本
echo ==================================

:: 1. 创建虚拟环境（如果不存在）
if not exist "venv\" (
    echo [1/3] 正在创建 Python 虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ 创建失败，请检查 Python 是否安装并加入 PATH
        pause
        exit /b 1
    )
) else (
    echo [1/3] 虚拟环境已存在，跳过创建
)

:: 2. 强制激活环境并安装依赖
echo [2/3] 正在安装依赖包...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install gradio==4.44.0
pip install manim==0.20.1
pip install edge-tts pyyaml ffmpeg-python pydantic

:: 3. 启动 WebUI
echo [3/3] 正在启动 WebUI 界面...
echo 浏览器将自动打开: http://127.0.0.1:7860
echo.
python run_webui.py

pause
endlocal