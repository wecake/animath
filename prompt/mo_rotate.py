from prompt.prompt_template import BaseGeoPrompt

class HandInHandGeoPrompt(BaseGeoPrompt):
    def __init__(self):
        super().__init__("手拉手模型")

    def get_manim_code_prompt(self, answer: str, steps_text: str, storyboard_text: str) -> str:
        base_prompt = super().get_manim_code_prompt(answer, steps_text, storyboard_text)
        extra = """
额外专属要求：
1. 绘制共顶点双等腰/等边三角形结构；
2. 突出旋转重合、手拉手全等三角形；
3. 标注公共顶点、旋转角、相等边与相等角。
"""
        return base_prompt + extra