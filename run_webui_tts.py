# run_webui.py 最终稳定版
import gradio as gr
from pathlib import Path
from app.llm import stage1_solve, stage2_storyboard, stage3_scripts
from prompt.prompt_router import GEO_MODEL_CHOICES

VERSION = "v0.0.6"
TITLE = f"几何AI动画教学系统"
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
    yield "", "", "", "", "启动中"

    d1 = stage1_solve(img, note, geo_model)
    ans = d1.get("answer", "")
    steps = safe_join(d1.get("steps", []))
    yield steps, "", "", ans, "解题完成"

    d2 = stage2_storyboard(steps, geo_model)
    story = safe_join(d2.get("storyboard", []))
    yield steps, "", story, ans, "分镜完成"

    d3 = stage3_scripts(steps, geo_model)
    scripts = safe_join(d3.get("scripts", []))
    yield steps, scripts, story, ans, "配音文案完成"

    save_outputs(ans, steps, scripts, story, geo_model)
    yield steps, scripts, story, ans, "✅ 全部完成"

with gr.Blocks(title=TITLE) as demo:
    gr.Markdown("# 几何AI动画教学系统")
    gr.Markdown("### 智能解题 | 分镜 | 配音 | 渲染 | 合成")

    with gr.Row():
        img = gr.Image(type="filepath", label="题目图片", height=400)
        with gr.Column():
            note = gr.Textbox(label="辅助说明", lines=3)
            geo_model = gr.Dropdown(choices=GEO_MODEL_CHOICES, value=GEO_MODEL_CHOICES[0], label="几何模型")
            btn = gr.Button("🚀 开始解析", variant="primary")

    gr.Markdown("---")

    steps = gr.Textbox(label="解题步骤", lines=5)
    story = gr.Textbox(label="动画分镜", lines=4)
    scripts = gr.Textbox(label="配音文案", lines=4)
    ans = gr.Textbox(label="最终答案")
    status = gr.Textbox(label="状态")

    btn.click(pipeline, inputs=[img, note, geo_model], outputs=[steps, scripts, story, ans, status])

if __name__ == "__main__":
    demo.queue().launch(server_name="0.0.0.0", server_port=7860)