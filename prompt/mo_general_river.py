from prompt.prompt_template import BaseGeoPrompt

class GeneralRiverGeoPrompt(BaseGeoPrompt):
    def __init__(self):
        super().__init__("将军饮马模型")

    def get_manim_code_prompt(self, answer: str, steps_text: str, storyboard_text: str) -> str:
        base_prompt = super().get_manim_code_prompt(answer, steps_text, storyboard_text)
        extra = """
额外专属要求：
1. 绘制直线河岸、两侧/同侧定点A、B；
2. 作出对称点、连线找最短路径动点；
3. 动画演示路径折线变直线的最短原理。
"""
        return base_prompt + extra