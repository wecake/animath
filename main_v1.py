from app.template_lib.template_factory import TemplateFactory
from app.storyboard.storyboard_generator import StoryboardGenerator
from app.llm_adapter.llm_prompt import get_llm_system_prompt

# 输入题目
question = "正方形ABCD边长为4，以B为圆心，2为半径作圆，P为圆上动点，求PD + 1/2 PC最小值。"

# 自动匹配模板
template = TemplateFactory.get_template(question)

# 生成 LLM 提示词（强制结构化）
prompt = get_llm_system_prompt(template)
print("=== LLM System Prompt ===")
print(prompt)

# 生成分镜（固定结构）
gen = StoryboardGenerator(template)
final_storyboard = gen.generate({})

print("\n=== 最终分镜（可直接给Manim生成）===")
import json
print(json.dumps(final_storyboard, ensure_ascii=False, indent=2))