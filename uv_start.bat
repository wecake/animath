@echo off
chcp 65001
echo ==================================
echo  MathAnimeOS —— uv 极速稳定版
echo ==================================

if not exist .venv (
    echo 创建 uv 虚拟环境...
    uv venv
)

echo 激活环境...
call .venv\Scripts\activate

echo 安装依赖（极速不报错）...
uv pip install manim==0.20.1
uv pip install gradio edge-tts pyyaml pillow==11.1.0

echo 启动 WebUI...
python run_webui.py

pause