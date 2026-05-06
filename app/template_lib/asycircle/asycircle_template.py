from app.template_lib.base_template import MathTemplate, StoryboardItem

class AsyCircleTemplate(MathTemplate):
    name = "阿氏圆"

    def get_fixed_script(self):
        return [
            "我们来看这道阿氏圆最值问题。",
            "这是带系数的线段和最小值，典型阿氏圆模型。",
            "用母子相似完成比例转化。",
            "动点P沿圆运动观察规律。",
            "三点共线时取最小值。"
        ]

    def get_storyboard(self):
        return [
            StoryboardItem(scene="画图形", script="", animation="DrawFigure", duration=3),
            StoryboardItem(scene="标动点P", script="", animation="MarkPointP", duration=2),
            StoryboardItem(scene="构造相似", script="", animation="ConstructSimilar", duration=4),
            StoryboardItem(scene="P运动", script="", animation="AnimatePointPMove", duration=4),
            StoryboardItem(scene="显示结果", script="", animation="ShowResult", duration=5),
        ]