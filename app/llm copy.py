import json
import requests
import os
import re
import base64
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("QWEN_API_KEY", "").strip()
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL = "qwen3.5-plus"
TIMEOUT = 600

SYS1 = """
你是初中几何老师。
识别几何题目，严格输出JSON格式：answer, steps。
不要多余内容，不要解释。
"""

SYS2 = """
你是动画导演。
根据解题步骤，生成动画分镜，输出JSON：storyboard。
"""

SYS3 = """
你是视频配音师。
根据解题步骤，生成适合初中生的配音文案，输出JSON：scripts。
"""

SYS4 = """
你是Manim 0.20+工程师。
生成可直接运行的极简Python动画代码：
1. 开头必须 from manim import *
2. 必须包含 class MathAnimation(Scene)
3. 禁止使用 small=True
4. 代码不超过100行
5. 只输出纯代码，无其他内容
"""

def image_to_base64(image_path):
    if not image_path or not os.path.exists(image_path):
        return None
    try:
        with Image.open(image_path) as img:
            img.thumbnail((1080, 1080))
            buf = BytesIO()
            img.save(buf, format="JPEG", quality=80)
            return f"data:image/jpeg;base64,{base64.b64encode(buf.getvalue()).decode()}"
    except Exception:
        return None

def clean_json(raw):
    try:
        raw = re.sub(r'```.*?```', '', raw, flags=re.DOTALL)
        raw = re.sub(r'[\x00-\x1F]', '', raw)
        s = raw.find('{')
        e = raw.rfind('}') + 1
        if s >= 0 and e > s:
            return json.loads(raw[s:e])
        return {}
    except Exception:
        return {}

def stage1_solve(image_path, note, tpl):
    print("\n【阶段1】识图解题")
    img_b64 = image_to_base64(image_path)
    messages = [
        {"role": "system", "content": SYS1},
        {"role": "user", "content": [
            {"type": "text", "text": f"题型：{tpl}，要求：{note}"},
            *([{"type": "image_url", "image_url": {"url": img_b64}}] if img_b64 else [])
        ]}
    ]
    try:
        resp = requests.post(
            f"{BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": MODEL, "messages": messages, "temperature": 0.0, "max_tokens": 2000},
            timeout=TIMEOUT
        )
        return clean_json(resp.json()["choices"][0]["message"]["content"])
    except Exception as e:
        print("阶段1异常:", e)
        return {}

def stage2_storyboard(steps):
    print("\n【阶段2】生成动画分镜")
    messages = [
        {"role": "system", "content": SYS2},
        {"role": "user", "content": f"解题步骤：{steps}"}
    ]
    try:
        resp = requests.post(
            f"{BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": MODEL, "messages": messages, "temperature": 0.0, "max_tokens": 2000},
            timeout=TIMEOUT
        )
        return clean_json(resp.json()["choices"][0]["message"]["content"])
    except Exception as e:
        print("阶段2异常:", e)
        return {}

def stage3_scripts(steps):
    print("\n【阶段3】生成配音解说")
    messages = [
        {"role": "system", "content": SYS3},
        {"role": "user", "content": f"解题步骤：{steps}"}
    ]
    try:
        resp = requests.post(
            f"{BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": MODEL, "messages": messages, "temperature": 0.0, "max_tokens": 2000},
            timeout=TIMEOUT
        )
        return clean_json(resp.json()["choices"][0]["message"]["content"])
    except Exception as e:
        print("阶段3异常:", e)
        return {}

def stage4_manim(answer, steps, story):
    print("\n【阶段4】生成Manim代码")
    prompt = f"答案：{answer}\n步骤：{steps}\n分镜：{story}"
    messages = [
        {"role": "system", "content": SYS4},
        {"role": "user", "content": prompt}
    ]
    try:
        resp = requests.post(
            f"{BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"model": MODEL, "messages": messages, "temperature": 0.0, "max_tokens": 2000},
            timeout=TIMEOUT
        )
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("阶段4异常:", e)
        return ""