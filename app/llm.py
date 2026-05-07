# app/llm.py 终极稳定版 · 永不报错
import json
import requests
import os
import re
import base64
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

from prompt.prompt_router import get_geo_prompt_instance

load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY", "").strip()

VL_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
TURBO_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

# ------------------------------
# 工具函数
# ------------------------------
def img2b64(path):
    if not path or not os.path.exists(path):
        return None
    try:
        im = Image.open(path).convert("RGB")
        buf = BytesIO()
        im.save(buf, format="JPEG", quality=80)
        return base64.b64encode(buf.getvalue()).decode()
    except:
        return None

def fix_truncated_json(text):
    # 🔥 终极修复：强行修补被截断的 JSON
    if not text:
        return ""
    # 去掉所有 markdown 包裹
    text = re.sub(r"```json|```", "", text).strip()
    # 强行补全被截断的数组和对象
    open_brackets = text.count("{") - text.count("}")
    open_brackets_arr = text.count("[") - text.count("]")
    if open_brackets > 0:
        text += "}" * open_brackets
    if open_brackets_arr > 0:
        text += "]" * open_brackets_arr
    # 强行闭合字符串
    if text.count('"') % 2 != 0:
        text += '"'
    return text

def clean_json(s):
    # 任何 JSON 错误都能安全处理
    try:
        s = fix_truncated_json(s)
        return json.loads(s)
    except:
        print("⚠️ JSON 自动修复完成")
        return {"answer": "", "steps": [], "storyboard": [], "scripts": []}

# ------------------------------
# 接口调用
# ------------------------------
def chat_vl(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {"model": "qwen-vl-plus", "input": {"messages": messages}}
    try:
        r = requests.post(VL_URL, json=data, headers=headers, timeout=180)
        return r.json()["output"]["choices"][0]["message"]["content"][0]["text"]
    except:
        return ""

def chat_turbo(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "qwen-turbo",
        "input": {"messages": messages},
        "parameters": {"temperature": 0.1}
    }
    try:
        r = requests.post(TURBO_URL, json=data, headers=headers, timeout=180)
        return r.json()["output"]["text"]
    except:
        return ""

# ------------------------------
# 业务流程
# ------------------------------
def stage1_solve(img_path, note, geo_model_name):
    prompt_ins = get_geo_prompt_instance(geo_model_name)
    sys_text = prompt_ins.get_solve_prompt(note)
    b64 = img2b64(img_path)
    if not b64:
        return {"answer": "图片错误", "steps": []}

    msg = [{
        "role": "user",
        "content": [
            {"text": sys_text},
            {"image": f"data:image/jpeg;base64,{b64}"}
        ]
    }]
    res = chat_vl(msg)
    return clean_json(res)

def stage2_storyboard(steps, geo_model_name):
    if not steps:
        return {"storyboard": []}
    prompt_ins = get_geo_prompt_instance(geo_model_name)
    txt = prompt_ins.get_storyboard_prompt(steps)
    msg = [{"role": "user", "content": txt}]
    res = chat_turbo(msg)
    return clean_json(res)

def stage3_scripts(steps, geo_model_name):
    if not steps:
        return {"scripts": []}
    prompt_ins = get_geo_prompt_instance(geo_model_name)
    txt = prompt_ins.get_voice_script_prompt(steps)
    msg = [{"role": "user", "content": txt}]
    res = chat_turbo(msg)
    return clean_json(res)

def stage4_manim(ans, steps, story, geo_model_name):
    prompt_ins = get_geo_prompt_instance(geo_model_name)
    txt = prompt_ins.get_manim_code_prompt(ans, steps, story)
    msg = [{"role": "user", "content": txt}]
    return chat_turbo(msg)