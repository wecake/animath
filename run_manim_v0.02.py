# run_manim.py v0.0.2 接收大模型生成的代码并渲染动画（代码有错就崩溃）
from pathlib import Path
import subprocess
from app.llm import stage4_manim

VERSION = "v0.0.2"
OUTPUT = Path("output")
CODE_FILE = OUTPUT / "manim_code.py"

def load_data():
    try:
        answer = (OUTPUT / "answer.txt").read_text(encoding="utf-8").strip()
        steps = (OUTPUT / "steps.txt").read_text(encoding="utf-8").strip()
        story = (OUTPUT / "storyboard.txt").read_text(encoding="utf-8").strip()
        geo_model = (OUTPUT / "geo_model.txt").read_text(encoding="utf-8").strip()
        return answer, steps, story, geo_model
    except Exception as e:
        print("❌ 读取输出文件失败，请先运行 run_webui.py")
        return None, None, None, None

def clean_manim_code(code):
    # 🔥 关键修复：去掉 ```python ``` 这些标记
    code = code.strip()
    if code.startswith("```python"):
        code = code[9:]
    if code.endswith("```"):
        code = code[:-3]
    return code.strip()

def generate_manim_code(answer, steps, story, geo_model):
    code = stage4_manim(answer, steps, story, geo_model)
    if not code:
        print("❌ 未生成有效代码")
        return False

    # 🔥 自动清理
    code = clean_manim_code(code)
    CODE_FILE.write_text(code, encoding="utf-8")
    print("✅ Manim 代码已生成：", CODE_FILE)
    return True

def render_animation():
    print("🎬 开始渲染视频...")
    cmd = [
        "manim",
        "-ql",
        str(CODE_FILE),
        "MathAnimation",
        "--disable_caching"
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=False, text=True)
        print("✅ 视频渲染完成！")
    except Exception as e:
        print("❌ 渲染失败：", e)

if __name__ == "__main__":
    print(f"===== 几何动画渲染 {VERSION} =====")
    ans, steps, story, geo_model = load_data()
    if ans and steps and story and geo_model:
        if generate_manim_code(ans, steps, story, geo_model):
            render_animation()
    else:
        print("⚠️  缺少输出文件，无法渲染")