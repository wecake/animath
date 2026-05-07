from prompt.prompt_template import BaseGeoPrompt

class FoldGeoPrompt(BaseGeoPrompt):
    def __init__(self):
        super().__init__("折叠模型")

    def get_manim_code_prompt(self, answer: str, steps_text: str, storyboard_text: str) -> str:
        base_prompt = super().get_manim_code_prompt(answer, steps_text, storyboard_text)
        extra = """
额外专属要求：
1. 绘制矩形/三角形原始图形 + 折叠后图形；
2. 画出折叠对称轴、对称对应点；
3. 标注折叠前后相等边长、相等角度、重叠区域。
"""
        return base_prompt + extra