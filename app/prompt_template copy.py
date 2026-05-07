def build_prompt(question, template_type="阿氏圆", **kwargs):
    custom = kwargs.get("custom_rule", "")
    return f"""
【题目】
{question}

【题型】
{template_type}

【用户要求】
{custom}

输出JSON：answer, steps, scripts, storyboard, manim_code
"""