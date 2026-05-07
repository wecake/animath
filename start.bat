@echo off
chcp 65001
echo ==============================================
echo          Animath 几何AI动画系统 v0.0.2
echo ==============================================
echo.

echo 1/4 启动 Web 界面：识图 → 解题 → 分镜 → 文案
start python run_webui.py

echo 2/4 等待 3 秒确保文案生成完成...
timeout /t 3 /nobreak >nul

echo 3/4 生成字幕 + 语音
python run_voice.py

echo 4/4 合成最终成片
python run_artifact.py

echo.
echo ✅ 全流程执行完成！
echo 📁 成品视频：output/final_video.mp4
echo.
pause