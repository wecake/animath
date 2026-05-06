from pydantic import BaseModel
from typing import List

class StoryboardItem(BaseModel):
    scene: str
    script: str
    animation: str
    duration: float

class MathTemplate:
    name = "base"
    def get_style(self): return {}
    def get_fixed_script(self): return []
    def get_storyboard(self): return []