import json
import requests
import os
import base64
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

# ======================
# 加载环境配置
# ======================
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(env_path)

# 千问VL 识图专用
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "").strip()
QWEN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
QWEN_VL_MODEL = "qwen2.5-vl-72b-instruct"

# DeepSeek 解题+生成代码专用
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
# 改用官方合法模型，避免400
DEEPSEEK_MODEL = "deepseek-chat"

TIMEOUT_VL = 120
TIMEOUT_CHAT = 180

# ======================
# 工具：图片压缩转base64
# ======================
def safe_img_to_base64(img_path):
    if not img_path:
        print("[DEBUG] 无图片路径，返回None")
        return None
    try:
        with Image.open(img_path) as img:
            img.thumbnail((900, 900))
            buf = BytesIO()
            img.save(buf, format="JPEG", quality=75)
            b64 = base64.b64encode(buf.getvalue()).decode()
            print(f"[DEBUG] 图片转base64成功，长度：{len(b64)}")
            return f"data:image/jpeg;base64,{b64}"
    except Exception as e:
        print(f"[ERROR] 图片转base64失败: {e}")
        return None

# ======================
# 1. 千问VL 识图（最全调试）
# ======================
def recognize_by_qwen_vl(image_base64):
    print("\n---------- 千问VL 识图开始 ----------")

    if not QWEN_API_KEY:
        print("[ERROR] 未配置 QWEN_API_KEY，跳过识图")
        return ""
    if not image_base64:
        print("[DEBUG] 无图片base64，跳过识图")
        return ""

    messages = [{
        "role": "user",
        "content": [
            {"type":"text","text":"请只输出图片中的初中数学几何题目原文，不要解释、不要步骤、不要多余文字。"},
            {"type":"image_url","image_url":{"url":image_base64}}
        ]
    }]

    payload = {
        "model": QWEN_VL_MODEL,
        "messages": messages,
        "temperature": 0.0
    }

    print("[DEBUG] 识图模型：", QWEN_VL_MODEL)
    print("[DEBUG] 正在请求千问VL接口...")

    try:
        resp = requests.post(
            f"{QWEN_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {QWEN_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=TIMEOUT_VL
        )
        print(f"[DEBUG] 千问VL HTTP状态码: {resp.status_code}")

        if resp.status_code != 200:
            print(f"[ERROR] 千问VL 接口异常响应: {resp.text[:300]}")
            return ""

        data = resp.json()
        print(f"[DEBUG] 响应顶层键: {list(data.keys())}")

        if "choices" not in data:
            print("[ERROR] 千问VL 返回无 choices 字段")
            return ""
        if len(data["choices"]) == 0:
            print("[ERROR] 千问VL choices 为空列表")
            return ""

        content = data["choices"][0]["message"]["content"].strip()
        print(f"[DEBUG] 识别到题干：\n{content}")
        print("---------- 千问VL 识图结束 ----------\n")
        return content

    except Exception as e:
        print(f"[ERROR] 千问VL 请求异常: {e}")
        return ""

# ======================
# 2. DeepSeek 解题 + 生成Manim代码（全调试）
# ======================
def generate_by_deepseek(question, tpl_type="阿氏圆"):
    print("\n---------- DeepSeek 生成开始 ----------")

    if not DEEPSEEK_API_KEY:
        print("[ERROR] 未配置 DEEPSEEK_API_KEY")
        return {
            "answer": "未配置DeepSeek密钥",
            "steps": ["请在.env配置DEEPSEEK_API_KEY"],
            "scripts": ["请配置密钥"],
            "storyboard": [],
            "manim_code": ""
        }

    # 组装提示词
    try:
        from app.prompt_template import build_prompt
        prompt = build_prompt(question, tpl_type)
        print(f"[DEBUG] 已组装提示词，长度：{len(prompt)}")
    except Exception as e:
        print(f"[ERROR] 组装提示词失败: {e}，直接使用原题干")
        prompt = question

    messages = [{"role": "user", "content": prompt}]
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
        "temperature": 0.1,
        "max_tokens": 4096
    }

    print("[DEBUG] 生成模型：", DEEPSEEK_MODEL)
    print("[DEBUG] 正在请求DeepSeek接口...")

    try:
        resp = requests.post(
            f"{DEEPSEEK_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=TIMEOUT_CHAT
        )

        print(f"[DEBUG] DeepSeek HTTP状态码: {resp.status_code}")
        if resp.status_code != 200:
            print(f"[ERROR] DeepSeek 400/异常响应: {resp.text[:500]}")
            return {
                "answer": f"DeepSeek接口错误{resp.status_code}",
                "steps": ["模型名错误或密钥错误"],
                "scripts": ["请检查模型/密钥"],
                "storyboard": [],
                "manim_code": ""
            }

        data = resp.json()
        print(f"[DEBUG] DeepSeek响应顶层键: {list(data.keys())}")

        if "choices" not in data or len(data["choices"]) == 0:
            print("[ERROR] DeepSeek 无合法choices")
            return {
                "answer": "返回结构异常",
                "steps": ["API无有效返回"],
                "scripts": ["请重试"],
                "storyboard": [],
                "manim_code": ""
            }

        content = data["choices"][0]["message"]["content"]
        print(f"[DEBUG] DeepSeek返回内容长度: {len(content)}")
        print("[DEBUG] 开始提取JSON块...")

        # 提取JSON
        try:
            s_idx = content.find("{")
            e_idx = content.rfind("}") + 1
            if s_idx < 0 or e_idx <= s_idx:
                raise ValueError("未找到首尾{}")

            json_str = content[s_idx:e_idx]
            result = json.loads(json_str)
            print("[DEBUG] JSON解析成功，获取完整结构")
            print("---------- DeepSeek 生成结束 ----------\n")
            return result

        except Exception as e:
            print(f"[ERROR] JSON解析失败: {e}")
            print(f"[DEBUG] 模型返回原文片段：\n{content[:300]}...")
            return {
                "answer": "JSON格式异常",
                "steps": [content[:200]],
                "scripts": ["生成格式不合规，请重试"],
                "storyboard": [],
                "manim_code": ""
            }

    except Exception as e:
        print(f"[ERROR] DeepSeek 请求整体异常: {e}")
        return {
            "answer": f"请求异常：{str(e)[:60]}",
            "steps": ["超时或网络错误"],
            "scripts": ["稍后重试"],
            "storyboard": [],
            "manim_code": ""
        }

# ======================
# 主入口（兼容原有调用，不动前端）
# ======================
def generate_animation(
    prompt_text: str,
    tpl_type: str = "阿氏圆",
    image_base64: str = None,
    custom_rule="", script_rule="", story_rule=""
):
    print("\n===== 【全局开始】AI生成流程 =====")
    print(f"[DEBUG] 页面补充文字：{prompt_text}")
    print(f"[DEBUG] 是否有图片：{image_base64 is not None}")
    print(f"[DEBUG] 题型模板：{tpl_type}")

    # 1. 千问识图
    ocr_text = recognize_by_qwen_vl(image_base64)

    # 2. 优先级：识图 > 手动输入
    user_input = prompt_text.strip()
    final_question = ocr_text if ocr_text else user_input
    print(f"[DEBUG] 最终使用题干：\n{final_question}")

    if not final_question:
        print("[ERROR] 识图和手动输入均为空")
        return {
            "answer": "未获取有效题目",
            "steps": ["图片识别失败，请手动填写完整题干"],
            "scripts": ["请手动补充题目文字"],
            "storyboard": [],
            "manim_code": ""
        }

    # 3. 交给DeepSeek生成全套
    return generate_by_deepseek(final_question, tpl_type)