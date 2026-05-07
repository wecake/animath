# app/prompt_template.py

def build_prompt(question, template_type="阿氏圆", custom_rule="", script_rule="", story_rule=""):
    base_prompt = f"""
你是一个专业的 Manim 动画工程师。请根据以下初中几何题目，生成一套完整的教学动画方案。

题目：{question}
题型：{template_type}

请严格按照以下 JSON 格式输出，不要添加任何其他解释性文字，也不要使用 Markdown：

{{
    "answer": "最终答案（如：6）",
    "steps": [
        "步骤1：...",
        "步骤2：..."
    ],
    "scripts": [
        "解说词1",
        "解说词2"
    ],
    "storyboard": [
        "分镜1：...",
        "分镜2：..."
    ],
    "manim_code": "```python
from manim import *
import numpy as np

class MathAnimation(Scene):
    def construct(self):
        # 这里必须生成完整的动画代码，包括：
        # 1. 坐标系/背景设置
        # 2. 题目图形绘制（点、线、圆等）
        # 3. 关键步骤的动画（移动、高亮、缩放）
        # 4. 文字标注和解题过程演示
        pass
```"
}}

要求：
1.  `manim_code` 字段里必须包含一个完整的 `class MathAnimation(Scene)` 类，代码必须是可直接运行的。
2.  代码中不能出现非 ASCII 字符（如中文、特殊符号），变量名用英文。
3.  动画步骤要和 `steps` 里的解题过程一一对应。
4.  必须使用 480p15 的标准配置，不要设置特殊参数。
"""

    if custom_rule:
        base_prompt += f"\n额外规则：{custom_rule}"
    if script_rule:
        base_prompt += f"\n解说词规则：{script_rule}"
    if story_rule:
        base_prompt += f"\n分镜规则：{story_rule}"

    return base_prompt