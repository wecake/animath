import json
import requests
import os
import base64
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

# 加载项目根目录.env
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(env_path)

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_API_BASE")
TIMEOUT_VL = 120
TIMEOUT_CHAT = 180

# 千问2.5 模型固定
VL_MODEL = "qwen2.5-vl-72b-instruct"
CHAT_MODEL = "qwen2.5-72b-instruct"

# 图片压缩转base64（适配千问要求）
def safe_img_to_base64(img_path):
    if not img_path or not os.path.exists(img_path):
        return None
    try:
        with Image.open(img_path) as img:
            img.thumbnail((900, 900))
            buf = BytesIO()
            img.save(buf, format="JPEG", quality=75)
            b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
            return f"data:image/jpeg;base64,{b64}"
    except Exception:
        return None

# 千问VL 识别数学题干
def recognize_math_question(image_base64):
    if not image_base64:
        return ""
    try:
        messages = [{
            "role": "user",
            "content": [
                {"type":"text","text":"只精准提取图片里初中数学几何完整题干，只输出题目原文，不要解释、不要步骤、不要多余文字。"},
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
        resp = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=TIMEOUT_VL
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        return ""

# 主生成入口：兼容原有调用参数，前端不用改
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
            "answer": "未配置百炼API_KEY",
            "steps": ["请在.env配置OPENAI_API_KEY"],
            "scripts": ["配置密钥后重试"],
            "storyboard": [],
            "manim_code": ""
        }

    # 识图兜底逻辑
    ocr_text = recognize_math_question(image_base64) if image_base64 else ""
    user_input = prompt_text.strip()
    final_question = ocr_text if ocr_text else user_input

    if not final_question:
        return {
            "answer": "未获取题目",
            "steps": ["图片识别失败，请手动填写题干"],
            "scripts": ["请手动补充题目文字"],
            "storyboard": [],
            "manim_code": ""
        }

    # 组装题型提示词
    try:
        from app.prompt_template import build_prompt
        final_prompt = build_prompt(final_question, tpl_type, custom_rule, script_rule, story_rule)
    except Exception:
        final_prompt = final_question

    # 千问2.5 生成全套内容
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
        resp = requests.post(
            f"{BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=TIMEOUT_CHAT
        )
        content = resp.json()["choices"][0]["message"]["content"]

        # 容错提取JSON
        try:
            s = content.find("{")
            e = content.rfind("}") + 1
            if s >= 0 and e > 0:
                return json.loads(content[s:e])
            raise Exception("无合法JSON")
        except Exception:
            return {
                "answer": "生成格式异常",
                "steps": [content[:150] + "..."],
                "scripts": ["请重新生成一次"],
                "storyboard": [],
                "manim_code": ""
            }
    except Exception as e:
        return {
            "answer": f"请求异常：{str(e)[:60]}",
            "steps": ["接口超时或网络异常"],
            "scripts": ["稍后重试"],
            "storyboard": [],
            "manim_code": ""
        }