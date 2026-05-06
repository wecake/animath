import edge_tts
import asyncio
import os

class EdgeTTSEngine:
    def __init__(self):
        self.voice = "zh-CN-XiaoyiNeural"

    async def gen(self, text, path):
        await edge_tts.Communicate(text, self.voice).save(path)

    def run_batch(self, texts):
        os.makedirs("output/audio", exist_ok=True)
        for i, t in enumerate(texts):
            asyncio.run(self.gen(t, f"output/audio/voice_{i}.mp3"))