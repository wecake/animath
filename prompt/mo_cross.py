from prompt.prompt_template import BaseGeoPrompt

class CrossGeoPrompt(BaseGeoPrompt):
    def __init__(self):
        super().__init__("十字架模型")

    def get_manim_code_prompt(self, answer: str, steps_text: str, storyboard_text: str) -> str:
        base_prompt = super().get_manim_code_prompt(answer, steps_text, storyboard_text)
        extra = """
额外专属要求：
1. 绘制正方形/矩形内部十字垂直线段；
2. 突出线段互相垂直、长度相等特征；
3. 画出垂直直角符号、对应相等线段标记。
"""
        return base_prompt + extra