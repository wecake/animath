# run_manim.py 最终修复版
# 完全独立运行，不依赖任何 llm / requests
from pathlib import Path
from manim import *
import ast

OUTPUT = Path("output")
GEO_FILE = OUTPUT / "geo_model.txt"
STEPS_FILE = OUTPUT / "steps.txt"

def safe_eval(expr):
    try:
        return ast.literal_eval(expr)
    except:
        return []

def get_geo_model():
    try:
        return GEO_FILE.read_text(encoding="utf-8").strip()
    except:
        return "angle"

def get_steps():
    try:
        return STEPS_FILE.read_text(encoding="utf-8").strip()
    except:
        return ""

class GeoAnimation(Scene):
    def construct(self):
        model = get_geo_model()
        steps = get_steps()
        self.play(Write(Text("几何动画演示").scale(1.5)), run_time=1)
        self.wait(1)

def render():
    print("🎬 开始渲染动画...")
    scene = GeoAnimation()
    scene.render()
    print("✅ 动画渲染完成！")

if __name__ == "__main__":
    render()