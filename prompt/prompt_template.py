# prompt_template.py
class BaseGeoPrompt:
    """
    几何模型 Prompt 母版基类 v0.0.2
    所有8大模型全部继承此类，统一规范、可扩展
    """
    def __init__(self, geo_model_name: str):
        self.geo_model_name = geo_model_name
        self.version = "v0.0.2"

    # 1. 识图解题Prompt
    def get_solve_prompt(self, user_note: str = "") -> str:
        return f"""
你是资深初中几何名师，严格限定使用【{self.geo_model_name}】标准模型思路解题。
用户补充说明：{user_note}

要求：
1. 严格匹配本几何模型特征，不跑偏、不套用其他模型；
2. 解题步骤条理清晰，适合初中生理解；
3. 必须严格返回纯标准JSON，无多余解释、无markdown、无```包裹；
格式固定：
{{
    "answer": "最终答案",
    "steps": ["步骤1","步骤2","步骤3"]
}}
""".strip()

    # 2. 动画分镜Prompt
    def get_storyboard_prompt(self, steps_text: str) -> str:
        return f"""
你是几何动画分镜导演，基于【{self.geo_model_name}】模型，
根据下面解题步骤设计Manim动画分镜镜头：
{steps_text}

要求：
1. 分镜按绘图→辅助线→关键点→推导→结论顺序设计；
2. 语言简洁，适合逐帧做动画；
3. 严格返回JSON：{{"storyboard":["镜头1","镜头2","镜头3"]}}
""".strip()

    # 3. 配音解说文案Prompt
    def get_voice_script_prompt(self, steps_text: str) -> str:
        return f"""
你是初中几何教学解说员，基于【{self.geo_model_name}】模型，
把下面解题步骤改成口语化、分段式配音文案：
{steps_text}

要求：
1. 每句简短适合字幕逐行显示；
2. 专业但通俗，适合课堂讲解；
3. 严格返回JSON：{{"scripts":["文案1","文案2","文案3"]}}
""".strip()

    # 4. Manim 生成代码基础Prompt（子类可重写追加专属约束）
    def get_manim_code_prompt(self, answer: str, steps_text: str, storyboard_text: str) -> str:
        return f"""
你是Manim专业动画工程师 v0.0.2
当前几何模型：{self.geo_model_name}
解题答案：{answer}
解题步骤：{steps_text}
动画分镜：{storyboard_text}

强制编码规范：
1. 主类必须 class MathAnimation(Scene):
2. 禁止 small=True、禁止废弃参数
3. 图形比例标准、线条清晰、关键点标注字母
4. 只输出可直接运行的完整Python代码，无任何多余解释、无markdown
""".strip()