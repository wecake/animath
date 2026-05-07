from prompt.prompt_template import BaseGeoPrompt

class RevEqualLineGeoPrompt(BaseGeoPrompt):
    def __init__(self):
        super().__init__("逆等线模型")

    def get_manim_code_prompt(self, answer: str, steps_text: str, storyboard_text: str) -> str:
        base_prompt = super().get_manim_code_prompt(answer, steps_text, storyboard_text)
        extra = """
额外专属要求：
1. 构造两条逆向等长线段、平移平行结构；
2. 辅助线平移构造全等三角形；
3. 标注相等线段、平行关系、动点轨迹。
"""
        return base_prompt + extra