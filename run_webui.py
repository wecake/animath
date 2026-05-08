import gradio as gr
from pathlib import Path
import subprocess
import threading
import sys
import logging

# ====================== 统一日志系统（文件 + 控制台）======================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-5s | %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging.getLogger(__name__)
# ========================================================================

# 强制使用当前虚拟环境 Python，杜绝环境错误
PYTHON = sys.executable

# 正确导入（仅保留项目中真实存在的模块）
from app.llm import stage1_solve, stage2_storyboard, stage3_scripts

# 目录初始化
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

def safe_join(arr):
    """安全拼接数组为字符串"""
    if not arr:
        return ""
    return "\n".join(str(item).strip() for item in arr if str(item).strip())

def save_all_outputs(answer, steps, scripts, story, geo_model):
    """保存所有解析结果到文件"""
    try:
        (OUTPUT_DIR / "answer.txt").write_text(str(answer), encoding="utf-8")
        (OUTPUT_DIR / "steps.txt").write_text(steps, encoding="utf-8")
        (OUTPUT_DIR / "scripts.txt").write_text(scripts, encoding="utf-8")
        (OUTPUT_DIR / "storyboard.txt").write_text(story, encoding="utf-8")
        (OUTPUT_DIR / "geo_model.txt").write_text(geo_model, encoding="utf-8")
        log.info("✅ 所有文件已保存到 output/")
    except Exception as e:
        log.error(f"❌ 保存文件失败: {str(e)}")

# ====================== 核心流程 ======================
def pipeline(img, note, geo_model, progress=gr.Progress()):
    log.info("===== 开始解析流程 =====")
    yield "", "", "", "", "初始化中..."

    try:
        # 步骤1：解题
        progress(0.3, "🔍 正在解题")
        log.info("步骤1：AI 解题中")
        d1 = stage1_solve(img, note, geo_model)
        ans = d1.get("answer", "")
        steps = safe_join(d1.get("steps", []))
        log.info("✅ 解题完成")
        yield steps, "", "", ans, "✅ 解题完成"

        # 步骤2：生成分镜
        progress(0.6, "🎬 生成动画分镜")
        log.info("步骤2：生成分镜")
        d2 = stage2_storyboard(steps, geo_model)
        story = safe_join(d2.get("storyboard", []))
        log.info("✅ 分镜生成完成")
        yield steps, story, "", ans, "✅ 分镜完成"

        # 步骤3：生成配音文案
        progress(0.9, "🎙️ 生成配音文案")
        log.info("步骤3：生成配音文案")
        d3 = stage3_scripts(steps, geo_model)
        scripts = safe_join(d3.get("scripts", []))
        log.info("✅ 配音文案生成完成")
        yield steps, story, scripts, ans, "✅ 文案完成"

        # 保存文件
        save_all_outputs(ans, steps, scripts, story, geo_model)
        yield steps, story, scripts, ans, "✅ 全部解析完成！"

    except Exception as e:
        log.error(f"❌ 流程异常: {str(e)}")
        yield "", "", "", "", f"错误：{str(e)}"

# ====================== 后台任务 ======================
def generate_voice_task(voice_name, speed, pitch, volume):
    """后台生成配音（不阻塞界面）"""
    try:
        from run_voice import load_scripts, generate_voice
        text = load_scripts()
        if text:
            log.info(f"🎙️ 开始生成配音 | 音色: {voice_name}")
            generate_voice(text, voice_name, speed, pitch, volume)
            log.info("✅ 配音生成成功")
    except Exception as e:
        log.error(f"❌ 配音失败: {str(e)}")

# ====================== 按钮功能 ======================
def gen_anim():
    log.info("🎬 启动动画渲染")
    threading.Thread(
        target=lambda: subprocess.run([PYTHON, "run_manim.py"], capture_output=True),
        daemon=True
    ).start()
    return "🎬 动画正在后台渲染..."

def gen_voice(voice_name, speed, pitch, volume):
    threading.Thread(
        target=generate_voice_task,
        args=(voice_name, speed, pitch, volume),
        daemon=True
    ).start()
    return "🎙️ 配音正在生成..."

def gen_final():
    log.info("📽️ 启动视频合成")
    threading.Thread(
        target=lambda: subprocess.run([PYTHON, "run_artifact.py"], capture_output=True),
        daemon=True
    ).start()
    return "📽️ 视频正在合成..."

# ====================== WebUI 界面 ======================
with gr.Blocks(title="几何AI动画教学系统") as demo:
    gr.Markdown("# 📐 几何AI动画教学系统")

    with gr.Row():
        img = gr.Image(type="filepath", label="题目图片")
        with gr.Column():
            note = gr.Textbox(label="补充说明", lines=2)
            geo_model = gr.Dropdown(
                choices=["angle", "triangle", "circle", "quadrilateral", "similar", "congruent"],
                value="angle",
                label="几何模型"
            )
            btn_parse = gr.Button("🚀 开始解析", variant="primary")

    gr.Markdown("## 📝 解析结果")
    steps = gr.Textbox(label="解题步骤", lines=5)
    story = gr.Textbox(label="动画分镜", lines=4)
    scripts = gr.Textbox(label="配音文案", lines=4)
    ans = gr.Textbox(label="最终答案")

    gr.Markdown("## ⚙️ 配音设置")
    with gr.Row():
        voice_sel = gr.Dropdown(
            ["female_calm", "male_steady", "female_lively"],
            value="female_calm",
            label="音色"
        )
        speed_sel = gr.Slider(0.8, 1.2, 1.05, step=0.05, label="语速")
    with gr.Row():
        pitch_sel = gr.Slider(-0.3, 0.3, 0, step=0.05, label="音调")
        vol_sel = gr.Slider(0.5, 1.5, 1.0, step=0.05, label="音量")

    gr.Markdown("## 🎯 一键生成")
    with gr.Row():
        b1 = gr.Button("1️⃣ 生成动画")
        b2 = gr.Button("2️⃣ 生成配音")
        b3 = gr.Button("3️⃣ 合成成片")

    status = gr.Textbox(label="运行状态", interactive=False)

    # 事件绑定
    btn_parse.click(
        pipeline,
        inputs=[img, note, geo_model],
        outputs=[steps, story, scripts, ans, status]
    )
    b1.click(gen_anim, outputs=[status])
    b2.click(gen_voice, inputs=[voice_sel, speed_sel, pitch_sel, vol_sel], outputs=[status])
    b3.click(gen_final, outputs=[status])

# ====================== 启动 ======================
if __name__ == "__main__":
    log.info("===== 启动 WebUI 服务 =====")
    log.info(f"Python 环境: {sys.executable}")
    demo.queue().launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)