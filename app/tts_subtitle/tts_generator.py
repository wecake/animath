import os
import edge_tts
import asyncio

async def save_voice(text, path):
    comm = edge_tts.Communicate(text, "zh-CN-XiaoyiNeural")
    await comm.save(path)

def generate_tts(scripts):
    audio_dir = "output/audio"
    os.makedirs(audio_dir, exist_ok=True)
    for f in os.listdir(audio_dir):
        if f.startswith("voice_"):
            os.remove(os.path.join(audio_dir, f))
    for i, line in enumerate(scripts):
        path = os.path.join(audio_dir, f"voice_{i}.mp3")
        asyncio.run(save_voice(line, path))