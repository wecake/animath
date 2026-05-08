# run_voice.py edge-tts版
from pathlib import Path
import edge_tts

OUTPUT = Path("output")
AUDIO_FILE = OUTPUT / "voice.mp3"

def load_scripts():
    try:
        return (OUTPUT / "scripts.txt").read_text(encoding="utf-8").strip()
    except:
        print("❌ 未找到配音文案")
        return None

def generate_voice(text):
    try:
        # 只生成语音，不搞字幕（避开 SubMaker 报错）
        communicate = edge_tts.Communicate(text, "zh-CN-YunxiNeural")
        communicate.save_sync(AUDIO_FILE)
        print(f"✅ 配音已生成：{AUDIO_FILE}")
    except Exception as e:
        print("❌ 配音生成失败：", e)

if __name__ == "__main__":
    print("===== 配音生成模块 =====")
    text = load_scripts()
    if text:
        generate_voice(text)