import json
import requests
from dotenv import load_dotenv
import os
from app.prompt_template import build_prompt

load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("LLM_BASE_URL")
MODEL = os.getenv("LLM_MODEL")

def generate_animation(question):
    prompt = build_prompt(question)
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }
    resp = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=data, timeout=180)
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"]
    start = content.find('{')
    end = content.rfind('}') + 1
    return json.loads(content[start:end])