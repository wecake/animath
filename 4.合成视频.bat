@echo off
chcp 65001
setlocal enabledelayedexpansion

:: ========== 配置路径 ==========
set "VIDEO_FILE=media\videos\0_20p1080p60\MathAnimation.mp4"
set "AUDIO_DIR=output\audio"
set "SRT_FILE=output\subtitle\auto.srt"
set "OUTPUT_FILE=output\final_video.mp4"

:: ========== 合并所有配音 ==========
echo 正在合并配音文件...
if exist "%AUDIO_DIR%\voice_*.mp3" (
    :: 生成文件列表
    dir /b "%AUDIO_DIR%\voice_*.mp3" | sort > audio_list.txt
    set "FFMPEG_CONCAT="
    for /f "delims=" %%i in (audio_list.txt) do (
        set "FFMPEG_CONCAT=!FFMPEG_CONCAT! -i "%AUDIO_DIR%\%%i""
    )
    :: 合并为一个音频文件
    ffmpeg !FFMPEG_CONCAT! -filter_complex "concat=n=5:v=0:a=1" -y "%AUDIO_DIR%\combined_voice.mp3"
    del audio_list.txt
) else (
    echo 未找到配音文件，跳过音频合并
    set "AUDIO_FILE="
)

:: ========== 合成视频 + 音频 + 字幕 ==========
echo 正在合成视频...
if exist "%AUDIO_DIR%\combined_voice.mp3" (
    ffmpeg -i "%VIDEO_FILE%" -i "%AUDIO_DIR%\combined_voice.mp3" -vf "subtitles=%SRT_FILE%" -c:v libx264 -c:a aac -shortest -y "%OUTPUT_FILE%"
) else (
    ffmpeg -i "%VIDEO_FILE%" -vf "subtitles=%SRT_FILE%" -c:v libx264 -y "%OUTPUT_FILE%"
)

echo 合成完成！文件已保存为：%OUTPUT_FILE%
pause