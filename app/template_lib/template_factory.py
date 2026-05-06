from app.template_lib.asycircle.asycircle_template import AsyCircleTemplate

class TemplateFactory:
    @staticmethod
    def get_template(q: str):
        if "阿氏圆" in q or "1/2" in q or "k·PA" in q:
            return AsyCircleTemplate()
        raise Exception("不支持")