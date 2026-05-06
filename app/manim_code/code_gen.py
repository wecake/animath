from typing import List, Dict

class ManimCodeGenerator:
    def __init__(self, style):
        self.style = style
        self.c = style["colors"]

    def generate_header(self):
        return f'''from manim import *
config.background_color = "{self.c['bg']}"
config.frame_height = 9
config.frame_width = 16
config.pixel_height = 1080
config.pixel_width = 1920
config.frame_rate = 60

COLOR_NORMAL = "{self.c['primary']}"
COLOR_HELPER = "{self.c['secondary']}"
COLOR_POINT = "{self.c['highlight']}"
COLOR_RESULT = "{self.c['accent']}"
'''

    def generate_scene(self, board):
        lines = ["class MathAnimation(Scene):", "    def construct(self):"]
        for i, item in enumerate(board):
            anim = item["animation"]
            if anim == "DrawFigure":
                lines.append("        square = Square(4, color=COLOR_NORMAL)")
                lines.append("        self.play(Create(square))")
                lines.append("        self.wait()")
            elif anim == "MarkPointP":
                lines.append("        circle = Circle(radius=2, color=COLOR_HELPER)")
                lines.append("        point_p = Dot(color=COLOR_POINT)")
                lines.append("        self.play(Create(circle), FadeIn(point_p))")
                lines.append("        self.wait()")
            elif anim == "ConstructSimilar":
                lines.append("        helper_line = Line(ORIGIN, RIGHT*2, color=COLOR_HELPER)")
                lines.append("        self.play(Create(helper_line))")
                lines.append("        self.wait()")
            elif anim == "AnimatePointPMove":
                # 最终修复：用 ApplyMethod 实现旋转
                lines.append("        self.play(ApplyMethod(point_p.rotate, TAU, {'about_point': circle.get_center()}), run_time=4)")
                lines.append("        self.wait()")
            elif anim == "ShowResult":
                lines.append("        result = Text('最小值: √17', color=COLOR_RESULT)")
                lines.append("        result.to_edge(DOWN)")
                lines.append("        self.play(FadeIn(result))")
                lines.append("        self.wait(2)")
        return "\n".join(lines)

    def generate_full_code(self, data):
        return self.generate_header() + self.generate_scene(data["storyboard"])