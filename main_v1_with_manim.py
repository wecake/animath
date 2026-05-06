import json
from app.template_lib.template_factory import TemplateFactory
from app.storyboard.storyboard_generator import StoryboardGenerator
from app.manim_code.code_gen import ManimCodeGenerator

# 加载全局样式
STYLE_CONFIG = {
    "background": "#000000",
    "colors": {
        "bg": "#000000",
        "primary": "#FFFFFF",
        "secondary": "#87CEEB",
        "highlight": "#FFFF00",
        "accent": "#FF0000"
    }
}

# ======================
# 1. 输入题目
# ======================
question = "正方形ABCD边长为4，以B为圆心，2为半径作圆，P为圆上动点，求PD + 1/2 PC最小值。"

# ======================
# 2. 自动匹配模板
# ======================
template = TemplateFactory.get_template(question)

# ======================
# 3. 生成固定分镜
# ======================
gen = StoryboardGenerator(template)
final_data = gen.generate({})

# ======================
# 4. 自动生成 MANIM 代码
# ======================
code_gen = ManimCodeGenerator(STYLE_CONFIG)
full_manim_code = code_gen.generate_full_code(final_data)

# ======================
# 输出结果
# ======================
print("=" * 60)
print("✅ 自动生成 Manim 代码（可直接保存运行）")
print("=" * 60)
print(full_manim_code)

# 保存到文件
with open("output/manim_code.py", "w", encoding="utf-8") as f:
    f.write(full_manim_code)

print("\n✅ 代码已保存至 output/manim_code.py")