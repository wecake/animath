from prompt.prompt_template import BaseGeoPrompt

class ApoCircleGeoPrompt(BaseGeoPrompt):
    def __init__(self):
        super().__init__("阿氏圆模型")

    def get_manim_code_prompt(self, answer: str, steps_text: str, storyboard_text: str) -> str:
        base_prompt = super().get_manim_code_prompt(answer, steps_text, storyboard_text)
        extra = """
额外专属要求：
1. 绘制基础圆、圆外定点、圆上动点P；
2. 构造内外分点、相似三角形比例关系；
3. 清晰标注半径、比例线段、最值位置。
"""
        return base_prompt + extra