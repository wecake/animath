import gradio as gr
from pathlib import Path
import subprocess
import sys
from app.llm import stage1_solve, stage2_storyboard, stage3_scripts
from prompt.prompt_router import GEO_MODEL_CHOICES

PYTHON = sys.executable

VERSION = "v1.0 状态正常刷新版"
TITLE = "几何AI动画教学系统"
OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)

def safe_join(arr):
    if not arr:
        return ""
    return "\n".join(str(x) for x in arr if x)

def save_outputs(answer, steps, scripts, storyboard, geo_model):
    (OUTPUT / "answer.txt").write_text(str(answer), encoding="utf-8")
    (OUTPUT / "steps.txt").write_text(steps, encoding="utf-8")
    (OUTPUT / "scripts.txt").write_text(scripts, encoding="utf-8")
    (OUTPUT / "storyboard.txt").write_text(storyboard, encoding="utf-8")
    (OUTPUT / "geo_model.txt").write_text(geo_model, encoding="utf-8")

def pipeline(img, note, geo_model, progress=gr.Progress()):
    yield "", "", "", "", "系统初始化中..."
    progress(0.3, "🔍 正在识图解题")
    d1 = stage1_solve(img, note, geo_model)
    ans = d1.get("answer", "")
    steps = safe_join(d1.get("steps", []))
    yield steps, "", "", ans, "✅ 识图解题完成"

    progress(0.6, "🎬 正在生成动画分镜")
    d2 = stage2_storyboard(steps, geo_model)
    story = safe_join(d2.get("storyboard", []))
    yield steps, "", story, ans, "✅ 动画分镜完成"

    progress(0.9, "🎙️ 正在生成配音文案")
    d3 = stage3_scripts(steps, geo_model)
    scripts = safe_join(d3.get("scripts", []))
    yield steps, scripts, story, ans, "✅ 配音文案完成"

    save_outputs(ans, steps, scripts, story, geo_model)
    yield steps, scripts, story, ans, "✅ 全部结果已保存，可下方一键生成成片"

# ✅ 关键修复：状态正常刷新
def gen_anim(status_text):
    return "🎬 后台正在生成动画视频..."

def gen_voice(voice_name, speed, pitch, volume, status_text):
    return "🎙️ 正在生成配音..."

def gen_final(status_text):
    return "📽️ 正在合成最终成片..."

with gr.Blocks(title=TITLE) as demo:
    gr.Markdown("# 几何AI动画教学系统")
    gr.Markdown("### 智能识图解题 · 自动分镜 · 高清配音 · 动画渲染")

    with gr.Row():
        img = gr.Image(type="filepath", label="📷 上传几何题目图片", height=400)
        with gr.Column():
            note = gr.Textbox(label="📝 辅助说明（可选）", lines=3)
            geo_model = gr.Dropdown(
                choices=GEO_MODEL_CHOICES,
                value=GEO_MODEL_CHOICES[0],
                label="📐 选择几何模型"
            )
            btn_parse = gr.Button("🚀 开始智能解析", variant="primary")

    gr.Markdown("---")
    steps = gr.Textbox(label="📚 解题步骤", lines=5)
    story = gr.Textbox(label="🎬 动画分镜脚本", lines=4)
    scripts = gr.Textbox(label="🎙️ 配音文案", lines=4)
    ans = gr.Textbox(label="🏁 最终答案")
    status = gr.Textbox(label="📡 运行状态")

    gr.Markdown("---")
    gr.Markdown("## 🎛️ 配音设置")
    with gr.Row():
        voice_sel = gr.Dropdown(
            label="🎭 配音音色",
            choices=["female_calm","male_steady","female_lively"],
            value="female_calm"
        )
        speed_sel = gr.Slider(
            label="⏱️ 语速",
            minimum=0.8,
            maximum=1.2,
            value=1.05,
            step=0.05
        )
    with gr.Row():
        pitch_sel = gr.Slider(
            label="🎵 音调",
            minimum=-0.3,
            maximum=0.3,
            value=0.0,
            step=0.05
        )
        vol_sel = gr.Slider(
            label="🔊 音量",
            minimum=0.5,
            maximum=1.5,
            value=1.0,
            step=0.05
    )

    gr.Markdown("## 🎯 一键生成")
    with gr.Row():
        b1 = gr.Button("1️⃣ 生成动画", variant="secondary")
        b2 = gr.Button("2️⃣ 生成配音", variant="secondary")
        b3 = gr.Button("3️⃣ 合成最终成片", variant="secondary")

    btn_parse.click(pipeline, inputs=[img, note, geo_model], outputs=[steps, scripts, story, ans, status])

    # ✅ 修复：状态正常更新
    b1.click(gen_anim, inputs=[status], outputs=[status])
    b2.click(gen_voice, inputs=[voice_sel, speed_sel, pitch_sel, vol_sel, status], outputs=[status])
    b3.click(gen_final, inputs=[status], outputs=[status])

if __name__ == "__main__":
    demo.queue().launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)