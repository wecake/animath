from app.template_lib.asycircle.asycircle_template import AsyCircleTemplate
from app.template_lib.base_template import MathTemplate
import json

class StoryboardGenerator:
    def __init__(self, template: MathTemplate):
        self.template = template

    def generate(self, llm_json: dict) -> dict:
        # 读取固定解说词
        scripts = self.template.get_fixed_script()

        # 读取固定分镜
        storyboard = self.template.get_storyboard()

        # 绑定解说词到分镜
        for i, scene in enumerate(storyboard):
            if i < len(scripts):
                scene.script = scripts[i]

        # 输出最终结构化分镜
        return {
            "type": self.template.name,
            "style": "style.yaml",
            "scripts": scripts,
            "storyboard": [s.dict() for s in storyboard]
        }

# -------------------
# 测试运行
# -------------------
if __name__ == "__main__":
    template = AsyCircleTemplate()
    gen = StoryboardGenerator(template)
    result = gen.generate({})
    print(json.dumps(result, ensure_ascii=False, indent=2))