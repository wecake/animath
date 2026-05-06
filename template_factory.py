from app.template_lib.asycircle.asycircle_template import AsyCircleTemplate
from app.template_lib.base_template import MathTemplate

class TemplateFactory:
    @staticmethod
    def get_template(question: str) -> MathTemplate:
        if "阿氏圆" in question or "1/2 PC" in question or "k·PA + PB" in question:
            return AsyCircleTemplate()
        # 未来扩展：将军饮马、胡不归...
        raise Exception("不支持的题型")