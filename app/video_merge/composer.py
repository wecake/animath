import subprocess
import os

class VideoComposer:
    def __init__(self, ffmpeg_path: str = "ffmpeg"):
        self.ffmpeg = ffmpeg_path

    def merge_all(self,
                  raw_video: str,
                  srt_path: str,
                  audio_dir: str,
                  out_video: str):
        """
        合并流程：
        1. 拼接多段配音为完整音频
        2. 原视频 + 完整音频 合并
        3. 嵌入SRT硬字幕（白字黑边固定样式）
        """
        # 1. 拼接所有配音
        list_txt = "output/audio/list.txt"
        audio_files = sorted([
            os.path.join(audio_dir, f)
            for f in os.listdir(audio_dir)
            if f.endswith(".mp3")
        ])

        with open(list_txt, "w", encoding="utf-8") as f:
            for af in audio_files:
                f.write(f"file '{af}'\n")

        full_audio = "output/audio/full_voice.mp3"
        cmd_concat = [
            self.ffmpeg, "-y", "-f", "concat", "-safe", "0",
            "-i", list_txt, "-c", "mp3", full_audio
        ]
        subprocess.run(cmd_concat, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 2. 视频 + 音频 + 硬字幕 合成最终成片
        # 字幕样式：白字、黑边、底部固定、字号适中
        filter_sub = (
            f"subtitles={srt_path}:force_style="
            "'FontName=SimHei,FontSize=24,PrimaryColour=FFFFFF,"
            "OutlineColour=000000,Outline=2,Alignment=2'"
        )

        cmd_final = [
            self.ffmpeg, "-y",
            "-i", raw_video,
            "-i", full_audio,
            "-filter_complex", f"[0:v]{filter_sub}[v];[1:a]apad[a]",
            "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-c:a", "aac",
            "-shortest",
            out_video
        ]
        subprocess.run(cmd_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return out_video