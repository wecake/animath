@echo off
chcp 65001
title animath - AI数学动画WebUI
call .venv\Scripts\activate.bat
python run_webui.py
pause