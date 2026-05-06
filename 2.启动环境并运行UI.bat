@echo off
chcp 65001
echo ==============================
echo 激活虚拟环境 + 启动WebUI
echo ==============================
call venv\Scripts\activate
pip install -r requirements.txt
pip install manim==0.20.1
python run_webui.py
pause