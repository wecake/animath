@echo off
chcp 65001 >nul
title MathAnimeOS 全流程一键制作
setlocal enabledelayedexpansion

:: ===================== 配置区 自行可改 =====================
set "QUESTION=正方形ABCD边长为4，以B为圆心2为半径作圆，P为圆上动点，求PD + 1/2 PC最小值。"
set "VIDEO_REL_PATH=media\videos\0_20\p1080p60\MathAnimation.mp4"
set "AUDIO_DIR=output\audio"
set "SRT_FILE=output\subtitle\auto.srt"
set "FINAL_VIDEO=output\final_video.mp4"
:: ===========================================================

echo ==============================================
echo   MathAnimeOS UV全流程一键制作
echo   自动：生成代码→渲染→配音合并→字幕合成
echo ==============================================
echo.

:: 1. 激活UV虚拟环境
echo [1] 激活 uv 虚拟环境...
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo 未检测到.venv，请先执行uv创建环境
    pause
    exit /b
)

:: 2. 清空旧输出
echo [2] 清理旧输出文件...
rmdir /s /q output 2>nul
mkdir output\audio 2>nul
mkdir output\subtitle 2>nul
echo.

:: 3. 命令行静默生成：代码+解说+配音+字幕
echo [3] 自动生成Manim代码、解说、AI配音、字幕...
python -c "
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

STYLE_CONFIG = {
    'colors': {
        'bg': '#000000',
        'primary': '#FFFFFF',
        'secondary': '#87CEEB',
        'highlight': '#FFFF00',
        'accent': '#FF0000'
    }
}

from app.template_lib.template_factory import TemplateFactory
from app.storyboard.storyboard_generator import StoryboardGenerator
from app.manim_code.code_gen import ManimCodeGenerator
from app.tts_subtitle.tts_engine import EdgeTTSEngine
from app.tts_subtitle.srt_generator import SrtGenerator

question = '''%QUESTION%'''

template = TemplateFactory.get_template(question)
sd = StoryboardGenerator(template).generate()
code = ManimCodeGenerator(STYLE_CONFIG).generate_full_code(sd)

os.makedirs('output', exist_ok=True)
with open('output/manim_code.py','w',encoding='utf-8') as f:
    f.write(code)

# 生成配音
EdgeTTSEngine().run_batch(sd['scripts'])
# 生成字幕
SrtGenerator.generate_srt(sd['storyboard'], sd['scripts'], 'output/subtitle/auto.srt')
print('✅ 生成完成')
"
echo.

:: 4. Manim 渲染视频
echo [4] Manim 开始渲染视频...
manim -ql output/manim_code.py MathAnimation
echo.

if not exist "%VIDEO_REL_PATH%" (
    echo ❌ 渲染失败，未找到视频文件
    pause
    exit /b
)

:: 5. 合并多段配音为一个音频
echo [5] 合并所有AI配音片段...
set "AUDIO_COMB=%AUDIO_DIR%\combined.mp3"
if exist "%AUDIO_DIR%\voice_*.mp3" (
    echo file list > concat.txt
    for %%f in (%AUDIO_DIR%\voice_*.mp3) do echo file '%%~f' >> concat.txt
    ffmpeg -y -f concat -safe 0 -i concat.txt -c copy "%AUDIO_COMB%" >nul 2>&1
    del concat.txt
)
echo.

:: 6. 视频 + 配音 + 字幕 压制成品
echo [6] 合成最终带字幕带配音成品视频...
if exist "%AUDIO_COMB%" (
    ffmpeg -y -i "%VIDEO_REL_PATH%" -i "%AUDIO_COMB%" ^
    -vf "subtitles=%SRT_FILE%" -c:v libx264 -c:a aac -shortest "%FINAL_VIDEO%"
) else (
    ffmpeg -y -i "%VIDEO_REL_PATH%" -vf "subtitles=%SRT_FILE%" "%FINAL_VIDEO%"
)

echo.
echo ==============================================
echo ✅ 全部完成！
echo 成品视频：%FINAL_VIDEO%
echo ==============================================
pause