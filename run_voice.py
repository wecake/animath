# run_voice.py 最终稳定版 · 零报错
import asyncio
from pathlib import Path
import edge_tts

OUTPUT = Path("output")
AUDIO_FILE = OUTPUT / "voice.mp3"

def load_scripts():
    try:
        return (OUTPUT / "scripts.txt").read_text(encoding="utf-8").strip()
    except:
        return None

async def text_to_speech(text, voice="zh-CN-XiaoxiaoNeural", rate="+0%"):
    try:
        communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
        await communicate.save(str(AUDIO_FILE))
        print("✅ 配音生成成功：", AUDIO_FILE)
        return True
    except Exception as e:
        print("❌ 配音失败：", e)
        return False

def generate_voice(text, voice_name="female_calm", speed=1.0, pitch=0.0, volume=1.0):
    # 映射音色
    vmap = {
        "female_calm": "zh-CN-XiaoxiaoNeural",
        "male_steady": "zh-CN-YunyangNeural",
        "female_lively": "zh-CN-YunxiNeural"
    }
    voice = vmap.get(voice_name, "zh-CN-XiaoxiaoNeural")
    sp = int((speed - 1.0) * 100)
    rate = f"{sp:+d}%"

    asyncio.run(text_to_speech(text, voice=voice, rate=rate))

if __name__ == "__main__":
    text = load_scripts()
    if text:
        generate_voice(text)