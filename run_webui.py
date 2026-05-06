import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gradio as gr
from app.template_lib.template_factory import TemplateFactory
from app.storyboard.storyboard_generator import StoryboardGenerator
from app.manim_code.code_gen import ManimCodeGenerator
from app.tts_subtitle.tts_engine import EdgeTTSEngine
from app.tts_subtitle.srt_generator import SrtGenerator

STYLE_CONFIG = {
    "colors": {
        "bg": "#000000",
        "primary": "#FFFFFF",
        "secondary": "#87CEEB",
        "highlight": "#FFFF00",
        "accent": "#FF0000"
    }
}

def generate_all(question: str, progress=gr.Progress()):
    progress(0.1, desc="🎯 正在识别题型...")
    try:
        template = TemplateFactory.get_template(question)
    except:
        return "❌ 无法识别题型", "", "", ""

    progress(0.2, desc="📝 生成分镜与解说词...")
    sg = StoryboardGenerator(template)
    story_data = sg.generate({})

    progress(0.3, desc="⚙️ 生成 Manim 代码...")
    code_gen = ManimCodeGenerator(STYLE_CONFIG)
    manim_code = code_gen.generate_full_code(story_data)
    code_path = os.path.join("output", "manim_code.py")
    os.makedirs("output", exist_ok=True)
    with open(code_path, "w", encoding="utf-8") as f:
        f.write(manim_code)

    progress(0.5, desc="🔊 生成 AI 配音...")
    try:
        tts = EdgeTTSEngine()
        tts.run_batch(story_data["scripts"])
    except Exception as e:
        pass

    progress(0.7, desc="📄 生成字幕...")
    srt_dir = "output/subtitle"
    os.makedirs(srt_dir, exist_ok=True)
    srt_path = os.path.join(srt_dir, "auto.srt")
    SrtGenerator.generate_srt(story_data["storyboard"], story_data["scripts"], srt_path)

    progress(0.9, desc="✅ 任务完成！")

    script_text = "\n\n".join(story_data["scripts"])
    storyboard_text = "\n".join([f"[{i+1}] {x['scene']} ({x['duration']}s)" for i, x in enumerate(story_data["storyboard"])])
    
    return (
        "✅ 生成完成！\n\n渲染命令：manim -pql output/manim_code.py",
        manim_code,
        script_text,
        storyboard_text
    )

with gr.Blocks(title="MathAnimeOS", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎬 MathAnimeOS V1.0")
    question_input = gr.Textbox(label="输入题目", lines=3, placeholder="正方形ABCD边长为4...")
    run_btn = gr.Button("▶️ 一键生成", variant="primary")
    with gr.Row():
        with gr.Column():
            status_output = gr.Textbox(label="状态")
            manim_code_output = gr.Code(label="Manim 代码", language="python", lines=10)
        with gr.Column():
            script_output = gr.Textbox(label="解说词", lines=8)
            storyboard_output = gr.Textbox(label="分镜", lines=8)
    run_btn.click(generate_all, inputs=question_input, outputs=[status_output, manim_code_output, script_output, storyboard_output])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)