@echo off
chcp 65001
setlocal enabledelayedexpansion

:: ========== 配置项（根据需要修改） ==========
set "PYTHON_SCRIPT=run_webui.py"
set "QUESTION=正方形ABCD边长为4，以B为圆心2为半径作圆，P为圆上动点，求PD + 1/2 PC最小值。"
set "VIDEO_PATH=media\videos\0_20p1080p60\MathAnimation.mp4"
set "AUDIO_DIR=output\audio"
set "SRT_FILE=output\subtitle\auto.srt"
set "FINAL_OUTPUT=output\final_video.mp4"

:: ========== 1. 启动 WebUI 生成代码、配音、字幕 ==========
echo [1/4] 启动 WebUI 生成内容...
start /B python "%PYTHON_SCRIPT%"
timeout /t 5 >nul

:: 调用API生成内容（这里用简单的命令行方式，也可以用curl等）
echo %QUESTION% > temp_question.txt
python -c "
import sys
sys.path.insert(0, '.')
from app.template_lib.template_factory import TemplateFactory
from app.storyboard.storyboard_generator import StoryboardGenerator
from app.manim_code.code_gen import ManimCodeGenerator
from app.tts_subtitle.tts_engine import EdgeTTSEngine
from app.tts_subtitle.srt_generator import SrtGenerator

with open('temp_question.txt', 'r', encoding='utf-8') as f:
    question = f.read().strip()

STYLE_CONFIG = {
    'colors': {
        'bg': '#000000',
        'primary': '#FFFFFF',
        'secondary': '#87CEEB',
        'highlight': '#FFFF00',
        'accent': '#FF0000'
    }
}

template = TemplateFactory.get_template(question)
sg = StoryboardGenerator(template)
story_data = sg.generate({})
code_gen = ManimCodeGenerator(STYLE_CONFIG)
manim_code = code_gen.generate_full_code(story_data)

import os
os.makedirs('output', exist_ok=True)
with open('output/manim_code.py', 'w', encoding='utf-8') as f:
    f.write(manim_code)

tts = EdgeTTSEngine()
tts.run_batch(story_data['scripts'])

os.makedirs('output/subtitle', exist_ok=True)
SrtGenerator.generate_srt(story_data['storyboard'], story_data['scripts'], 'output/subtitle/auto.srt')

print('✅ 内容生成完成')
"
del temp_question.txt
echo.

:: ========== 2. 用 Manim 渲染视频 ==========
echo [2/4] 渲染 Manim 视频...
manim -pql output/manim_code.py MathAnimation
if not exist "%VIDEO_PATH%" (
    echo ❌ 渲染失败，视频文件未找到！
    pause
    exit /b 1
)
echo.

:: ========== 3. 合并所有配音 ==========
echo [3/4] 合并配音文件...
if exist "%AUDIO_DIR%\voice_*.mp3" (
    dir /b "%AUDIO_DIR%\voice_*.mp3" | sort > audio_list.txt
    set "FFMPEG_CONCAT="
    for /f "delims=" %%i in (audio_list.txt) do (
        set "FFMPEG_CONCAT=!FFMPEG_CONCAT! -i "%AUDIO_DIR%\%%i""
    )
    ffmpeg !FFMPEG_CONCAT! -filter_complex "concat=n=5:v=0:a=1" -y "%AUDIO_DIR%\combined_voice.mp3"
    del audio_list.txt
) else (
    echo 未找到配音文件，跳过音频合并
    set "AUDIO_FILE="
)
echo.

:: ========== 4. 合成视频 + 音频 + 字幕 ==========
echo [4/4] 合成最终视频...
if exist "%AUDIO_DIR%\combined_voice.mp3" (
    ffmpeg -i "%VIDEO_PATH%" -i "%AUDIO_DIR%\combined_voice.mp3" -vf "subtitles=%SRT_FILE%" -c:v libx264 -c:a aac -shortest -y "%FINAL_OUTPUT%"
) else (
    ffmpeg -i "%VIDEO_PATH%" -vf "subtitles=%SRT_FILE%" -c:v libx264 -y "%FINAL_OUTPUT%"
)

echo.
echo ✅ 全部流程完成！
echo 最终视频文件：%FINAL_OUTPUT%
pause