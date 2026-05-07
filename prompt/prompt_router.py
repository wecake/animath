# prompt_router.py
from prompt.mo_rotate import HandInHandGeoPrompt
from prompt.mo_cross import CrossGeoPrompt
from prompt.mo_half_angle import HalfAngleGeoPrompt
from prompt.mo_general_river import GeneralRiverGeoPrompt
from prompt.mo_hubugui import HuBuGuiGeoPrompt
from prompt.mo_apo_circle import ApoCircleGeoPrompt
from prompt.mo_rev_equal import RevEqualLineGeoPrompt
from prompt.mo_fold import FoldGeoPrompt

# 模型名称映射 → 对应类
GEO_MODEL_MAP = {
    "手拉手模型": HandInHandGeoPrompt,
    "十字架模型": CrossGeoPrompt,
    "半角模型": HalfAngleGeoPrompt,
    "将军饮马模型": GeneralRiverGeoPrompt,
    "胡不归模型": HuBuGuiGeoPrompt,
    "阿氏圆模型": ApoCircleGeoPrompt,
    "逆等线模型": RevEqualLineGeoPrompt,
    "折叠模型": FoldGeoPrompt
}

def get_geo_prompt_instance(model_name: str):
    """根据模型名称获取对应Prompt实例"""
    cls = GEO_MODEL_MAP.get(model_name, GeneralRiverGeoPrompt)
    return cls()

# 下拉选项列表，直接给WebUI使用
GEO_MODEL_CHOICES = list(GEO_MODEL_MAP.keys())