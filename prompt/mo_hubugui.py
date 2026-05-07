from prompt.prompt_template import BaseGeoPrompt

class HuBuGuiGeoPrompt(BaseGeoPrompt):
    def __init__(self):
        super().__init__("胡不归模型")

    def get_manim_code_prompt(self, answer: str, steps_text: str, storyboard_text: str) -> str:
        base_prompt = super().get_manim_code_prompt(answer, steps_text, storyboard_text)
        extra = """
额外专属要求：
1. 绘制定点、定直线、含系数k·PA+PB结构；
2. 构造定角做平行线转化加权线段；
3. 标出最短距离垂线段与关键角度。
"""
        return base_prompt + extra