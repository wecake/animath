import os
from app.template_lib.template_factory import TemplateFactory
from app.storyboard.storyboard_generator import StoryboardGenerator
from app.manim_code.code_gen import ManimCodeGenerator
from app.tts_subtitle.tts_engine import EdgeTTSEngine
from app.tts_subtitle.srt_generator import SrtGenerator
from app.video_merge.composer import VideoComposer

# 全局样式配置
STYLE_CONFIG = {
    "colors": {
        "bg": "#000000",
        "primary": "#FFFFFF",
        "secondary": "#87CEEB",
        "highlight": "#FFFF00",
        "accent": "#FF0000"
    }
}

def run_pipeline(question: str):
    # 1. 匹配题型模板
    template = TemplateFactory.get_template(question)

    # 2. 生成分镜+解说词结构化数据
    sg = StoryboardGenerator(template)
    story_data = sg.generate({})

    # 3. 生成Manim代码并保存
    code_gen = ManimCodeGenerator(STYLE_CONFIG)
    manim_code = code_gen.generate_full_code(story_data)
    os.makedirs("output", exist_ok=True)
    code_path = "output/manim_code.py"
    with open(code_path, "w", encoding="utf-8") as f:
        f.write(manim_code)
    print("✅ Manim 代码生成完成")

    # 4. TTS 批量生成配音
    tts = EdgeTTSEngine()
    tts.run_batch(story_data["scripts"])
    print("✅ TTS 配音生成完成")

    # 5. 生成SRT字幕
    srt_path = "output/subtitle/auto.srt"
    SrtGenerator.generate_srt(
        story_data["storyboard"],
        story_data["scripts"],
        srt_path
    )
    print("✅ SRT 字幕生成完成")

    # 6. 等待手动渲染manim后，再执行合成
    print("\n👉 请先执行：manim -pql output/manim_code.py")
    print("👉 渲染出视频后，填入下面路径即可合成成片")

if __name__ == "__main__":
    q = "正方形ABCD边长为4，以B为圆心，2为半径作圆，P为圆上动点，求PD + 1/2 PC最小值。"
    run_pipeline(q)