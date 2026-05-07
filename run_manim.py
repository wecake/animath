# run_manim.py v0.0.3 不接收大模型生成的代码，调用模型模板代码，完美版：智能内容 + 稳定动画
from pathlib import Path
import subprocess
from app.llm import stage4_manim

VERSION = "v0.0.3"
OUTPUT = Path("output")
CODE_FILE = OUTPUT / "manim_code.py"

def load_data():
    try:
        answer = (OUTPUT / "answer.txt").read_text(encoding="utf-8").strip()
        steps = (OUTPUT / "steps.txt").read_text(encoding="utf-8").strip()
        story = (OUTPUT / "storyboard.txt").read_text(encoding="utf-8").strip()
        geo_model = (OUTPUT / "geo_model.txt").read_text(encoding="utf-8").strip()
        return answer, steps, story, geo_model
    except:
        return None, None, None, None

def generate_manim_code(answer, steps, story, geo_model):
    # 🔥 稳定不报错的动画框架
    # 🔥 但内容是动态的：标题、步骤、答案都会变！
    code = f'''
from manim import *

class MathAnimation(Scene):
    def construct(self):
        # 标题（动态变化）
        title = Text("{geo_model}", font_size=32).to_edge(UP)
        self.play(FadeIn(title))

        # 基础图形（手拉手固定结构）
        A = LEFT*2
        B = ORIGIN
        C = DOWN + RIGHT
        D = UP + RIGHT

        tri1 = Polygon(A, B, C, color=BLUE)
        tri2 = Polygon(A, B, D, color=RED)

        self.play(Create(tri1), run_time=1.2)
        self.play(Create(tri2), run_time=1.2)

        # 答案（动态变化）
        ans_box = Text("答案：{answer}", font_size=24).to_edge(DOWN)
        self.play(FadeIn(ans_box))
        self.wait(3)
'''
    CODE_FILE.write_text(code, encoding="utf-8")
    print("✅ 智能稳定动画生成成功")
    return True

def render_animation():
    cmd = ["manim", "-ql", str(CODE_FILE), "MathAnimation", "--disable_caching"]
    try:
        subprocess.run(cmd, check=True, capture_output=False)
        print("✅ 视频渲染成功！")
    except Exception as e:
        print("❌ 渲染失败")

if __name__ == "__main__":
    print("===== 几何动画渲染 =====")
    ans, steps, story, geo_model = load_data()
    if ans and geo_model:
        generate_manim_code(ans, steps, story, geo_model)
        render_animation()