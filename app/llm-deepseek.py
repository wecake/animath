import json
import requests
import os
import base64
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

# 加载环境
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(env_path)

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_API_BASE", "https://api.deepseek.com/v1")
TIMEOUT_VL = 120
TIMEOUT_CHAT = 180

VL_MODEL = "deepseek-vl-7b-chat"
CHAT_MODEL = os.getenv("OPENAI_MODEL", "deepseek-v4-flash")

# 图片压缩
def safe_img_to_base64(img_path):
    if not img_path or not os.path.exists(img_path):
        return None
    try:
        with Image.open(img_path) as img:
            img.thumbnail((800, 800))
            buf = BytesIO()
            img.save(buf, format="JPEG", quality=70)
            b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
            return f"data:image/jpeg;base64,{b64}"
    except:
        return None

# 识图
def recognize_math_question(image_base64):
    if not image_base64:
        return ""
    try:
        messages = [{
            "role": "user",
            "content": [
                {"type":"text","text":"请只输出图片中的数学题目原文，不要其他内容"},
                {"type":"image_url","image_url":{"url":image_base64}}
            ]
        }]
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": VL_MODEL,
            "messages": messages,
            "temperature": 0.0
        }
        resp = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload, timeout=TIMEOUT_VL)
        return resp.json()["choices"][0]["message"]["content"].strip()
    except:
        return ""

# 【终极防御】生成动画，任何错误都不崩
def generate_animation(
    prompt_text: str,
    tpl_type: str = "阿氏圆",
    image_base64: str = None,
    custom_rule: str = "",
    script_rule: str = "",
    story_rule: str = ""
):
    if not API_KEY:
        return {
            "answer": "无密钥",
            "steps": ["请配置OPENAI_API_KEY"],
            "scripts": ["请配置密钥"],
            "storyboard": [],
            "manim_code": ""
        }

    # 识图 + 题目获取
    ocr_text = recognize_math_question(image_base64) if image_base64 else ""
    user_input = prompt_text.strip()
    final_question = ocr_text if ocr_text else user_input

    if not final_question:
        return {
            "answer": "未识别题目",
            "steps": ["请上传题目图片或填写文字说明"],
            "scripts": ["请上传图片或填写文字"],
            "storyboard": [],
            "manim_code": ""
        }

    # 提示词
    try:
        from app.prompt_template import build_prompt
        final_prompt = build_prompt(final_question, tpl_type, custom_rule, script_rule, story_rule)
    except:
        final_prompt = final_question

    # 请求
    try:
        messages = [{"role":"user","content":final_prompt}]
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": CHAT_MODEL,
            "messages": messages,
            "temperature": 0.1,
            "max_tokens": 4096
        }
        resp = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload, timeout=TIMEOUT_CHAT)
        content = resp.json()["choices"][0]["message"]["content"]

        # ======================
        # 【终极防御 JSON】
        # ======================
        try:
            s = content.find("{")
            e = content.rfind("}") + 1
            if s >= 0 and e > 0:
                return json.loads(content[s:e])
            else:
                raise Exception("无JSON")
        except:
            return {
                "answer": "生成失败（模型未返回JSON）",
                "steps": [content[:100] + "..."],
                "scripts": ["生成失败，请重试"],
                "storyboard": [],
                "manim_code": ""
            }

    except Exception as e:
        return {
            "answer": f"请求异常：{str(e)[:50]}",
            "steps": ["API请求超时或失败"],
            "scripts": ["请稍后重试"],
            "storyboard": [],
            "manim_code": ""
        }