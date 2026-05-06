@echo off
chcp 65001 >nul
title 数学动画 题库批量成片-断点续跑版
setlocal enabledelayedexpansion

:: ========== 配置区 ==========
set "QUEST_FILE=questions.txt"
set "DONE_LOG=done.txt"
set "VIDEO_TPL=media\videos\0_20\p1080p60\MathAnimation.mp4"
set "OUT_ROOT=batch_output"
set "SRT_NAME=auto.srt"
set "AUDIO_COMB_NAME=combined.mp3"
:: ============================

echo ==============================================
echo   题库批量成片｜断点续跑·跳过已完成
echo ==============================================
echo.

:: 激活uv虚拟环境
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo 错误：未找到.venv虚拟环境，请先执行 uv venv
    pause
    exit /b
)

:: 初始化完成记录文件
if not exist "%DONE_LOG%" echo. > "%DONE_LOG%"

:: 创建批量输出根目录
if not exist "%OUT_ROOT%" mkdir "%OUT_ROOT%"

set idx=0
:: 逐行读取题库
for /f "delims=" %%q in (%QUEST_FILE%) do (
    set /a idx+=1
    set "Q=%%q"
    set "CUR_DIR=%OUT_ROOT%\题!idx!"
    set "FINAL_MP4=!CUR_DIR!\成品_第!idx!题.mp4"

    :: 断点判断：已在done.txt里就跳过
    findstr /x /c:"!idx!" "%DONE_LOG%" >nul
    if not errorlevel 1 (
        echo 跳过第 !idx! 题：已完成
        echo.
        continue
    )

    echo ==============================================
    echo 正在处理第 !idx! 题
    echo ==============================================

    :: 清空临时output
    rmdir /s /q output 2>nul
    mkdir output\audio 2>nul
    mkdir output\subtitle 2>nul

    :: 生成代码、配音、字幕
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

question = '''!Q!'''
template = TemplateFactory.get_template(question)
sd = StoryboardGenerator(template).generate()
code = ManimCodeGenerator(STYLE_CONFIG).generate_full_code(sd)

os.makedirs('output', exist_ok=True)
with open('output/manim_code.py','w',encoding='utf-8') as f:
    f.write(code)

EdgeTTSEngine().run_batch(sd['scripts'])
SrtGenerator.generate_srt(sd['storyboard'], sd['scripts'], 'output/subtitle/auto.srt')
"

    :: Manim渲染
    manim -ql output/manim_code.py MathAnimation

    if not exist "%VIDEO_TPL%" (
        echo ❌ 第!idx!题渲染失败，跳过
        echo.
        continue
    )

    :: 创建本题目录
    if not exist "!CUR_DIR!" mkdir "!CUR_DIR!"

    :: 合并配音
    set "AUDIO_COMB=output\audio\%AUDIO_COMB_NAME%"
    if exist "output\audio\voice_*.mp3" (
        echo file list > concat_tmp.txt
        for %%f in (output\audio\voice_*.mp3) do echo file '%%~f' >> concat_tmp.txt
        ffmpeg -y -f concat -safe 0 -i concat_tmp.txt -c copy "!AUDIO_COMB!" >nul 2>&1
        del concat_tmp.txt
    )

    :: 合成成品视频
    if exist "!AUDIO_COMB!" (
        ffmpeg -y -i "%VIDEO_TPL%" -i "!AUDIO_COMB!" ^
        -vf "subtitles=output/subtitle/%SRT_NAME%" -c:v libx264 -c:a aac -shortest "!FINAL_MP4!"
    ) else (
        ffmpeg -y -i "%VIDEO_TPL%" -vf "subtitles=output/subtitle/%SRT_NAME%" "!FINAL_MP4!"
    )

    :: 备份源码、字幕、音频
    copy output\manim_code.py "!CUR_DIR!\manim代码.py" >nul
    copy output\subtitle\%SRT_NAME% "!CUR_DIR!\字幕.srt" >nul
    if exist "!AUDIO_COMB%" copy "!AUDIO_COMB!" "!CUR_DIR!\解说音频.mp3" >nul

    :: 记录已完成题号
    echo !idx! >> "%DONE_LOG%"

    echo ✅ 第!idx!题 完成归档
    echo.
)

echo ==============================================
echo 本轮批量任务结束
echo 已完成记录：%DONE_LOG%
echo 成品目录：%OUT_ROOT%
echo ==============================================
pause