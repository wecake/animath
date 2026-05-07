# run_webui.py v0.0.3 最终稳定版
import gradio as gr
from pathlib import Path
from app.llm import stage1_solve, stage2_storyboard, stage3_scripts
from prompt.prompt_router import GEO_MODEL_CHOICES

VERSION = "v0.0.3"
TITLE = f"几何AI解题系统 {VERSION}"
OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)

def safe_join(arr):
    if not arr:
        return ""
    out = []
    for item in arr:
        if isinstance(item, (dict, list)):
            out.append(str(item))
        else:
            out.append(str(item))
    return "\n".join(out)

def save_outputs(answer, steps, scripts, storyboard, geo_model):
    (OUTPUT / "answer.txt").write_text(str(answer), encoding="utf-8")
    (OUTPUT / "steps.txt").write_text(steps, encoding="utf-8")
    (OUTPUT / "scripts.txt").write_text(scripts, encoding="utf-8")
    (OUTPUT / "storyboard.txt").write_text(storyboard, encoding="utf-8")
    (OUTPUT / "geo_model.txt").write_text(geo_model, encoding="utf-8")
    (OUTPUT / "version.txt").write_text(VERSION, encoding="utf-8")

def pipeline(img, note, geo_model, progress=gr.Progress()):
    yield "", "", "", "", "启动中..."

    progress(0.3, "正在识图解题")
    d1 = stage1_solve(img, note, geo_model)
    ans = d1.get("answer", "")
    steps = safe_join(d1.get("steps", []))
    yield steps, "", "", ans, "✅ 解题完成"

    progress(0.6, "正在生成分镜")
    d2 = stage2_storyboard(steps, geo_model)
    story = safe_join(d2.get("storyboard", []))
    yield steps, "", story, ans, "✅ 分镜完成"

    progress(0.9, "正在生成配音文案")
    d3 = stage3_scripts(steps, geo_model)
    scripts = safe_join(d3.get("scripts", []))
    yield steps, scripts, story, ans, "✅ 文案生成完成"

    save_outputs(ans, steps, scripts, story, geo_model)
    yield steps, scripts, story, ans, "✅ 全部输出已保存到 output/"

with gr.Blocks(title=TITLE) as demo:
    gr.Markdown(f"# {TITLE}")
    with gr.Row():
        img = gr.Image(type="filepath", label="题目图片")
        with gr.Column():
            note = gr.Textbox(label="辅助说明", lines=2)
            geo_model = gr.Dropdown(
                choices=GEO_MODEL_CHOICES,
                value=GEO_MODEL_CHOICES[0],
                label="选择几何模型"
            )
            btn = gr.Button("🚀 开始解析", variant="primary")

    steps = gr.Textbox(label="解题步骤", lines=3)
    scripts = gr.Textbox(label="配音文案", lines=3)
    story = gr.Textbox(label="动画分镜", lines=3)
    ans = gr.Textbox(label="最终答案")
    status = gr.Textbox(label="运行状态")

    btn.click(
        pipeline,
        inputs=[img, note, geo_model],
        outputs=[steps, scripts, story, ans, status]
    )

if __name__ == "__main__":
    demo.queue().launch(server_name="0.0.0.0", server_port=7860, show_error=True)