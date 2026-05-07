from prompt.prompt_template import BaseGeoPrompt

class HalfAngleGeoPrompt(BaseGeoPrompt):
    def __init__(self):
        super().__init__("半角模型")

    def get_manim_code_prompt(self, answer: str, steps_text: str, storyboard_text: str) -> str:
        base_prompt = super().get_manim_code_prompt(answer, steps_text, storyboard_text)
        extra = """
额外专属要求：
1. 绘制90°含45°、120°含60°标准半角结构；
2. 演示三角形旋转拼接、构造全等；
3. 清晰标注大角、半角、等量替换线段。
"""
        return base_prompt + extra