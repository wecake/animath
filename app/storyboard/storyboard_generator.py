from app.template_lib.base_template import MathTemplate

class StoryboardGenerator:
    def __init__(self, template: MathTemplate):
        self.t = template

    def generate(self, data=None):
        scripts = self.t.get_fixed_script()
        storyboard = self.t.get_storyboard()
        for i, s in enumerate(storyboard):
            if i < len(scripts):
                s.script = scripts[i]
        return {
            "type": self.t.name,
            "scripts": scripts,
            "storyboard": [x.dict() for x in storyboard]
        }