# run_artifact.py 修复版 只合并视频+音频
from pathlib import Path
import subprocess
import glob

OUTPUT = Path("output")
VIDEO_PATTERN = "media/videos/manim_code/480p15/*.mp4"
FINAL_VIDEO = OUTPUT / "final_video.mp4"

def find_video():
    files = glob.glob(VIDEO_PATTERN)
    return files[0] if files else None

def merge_video_audio():
    video = find_video()
    audio = OUTPUT / "voice.mp3"

    if not video or not audio.exists():
        print("❌ 缺少视频或配音")
        return

    # 只混流视频+音频，不加入字幕，避免MP4不支持字幕容器报错
    cmd = [
        "ffmpeg",
        "-i", video,
        "-i", str(audio),
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        "-y", str(FINAL_VIDEO)
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=False)
        print(f"✅ 成片已生成：{FINAL_VIDEO}")
    except Exception as e:
        print("❌ 合成失败：", e)

if __name__ == "__main__":
    print("===== 最终成片合成 =====")
    merge_video_audio()