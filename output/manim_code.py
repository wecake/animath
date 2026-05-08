
from manim import *

class MathAnimation(Scene):
    def construct(self):
        # 标题（动态变化）
        title = Text("手拉手模型", font_size=32).to_edge(UP)
        self.play(FadeIn(title))

        # 基础图形（手拉手固定结构）
        A = LEFT*2
        B = ORIGIN
        C = DOWN + RIGHT
        D = UP + RIGHT

        tri1 = Polygon(A, B, C, color=BLUE)
        tri2 = Polygon(A, B, D, color=RED)

        self.play(Create(tri1), run_time=1.2)
        self.play(Create(tri2), run_time=1.2)

        # 答案（动态变化）
        ans_box = Text("答案：5", font_size=24).to_edge(DOWN)
        self.play(FadeIn(ans_box))
        self.wait(3)
