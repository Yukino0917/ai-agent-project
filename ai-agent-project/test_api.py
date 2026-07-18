import os
from openai import OpenAI

api_key = os.environ.get("OPENAI_API_KEY", "")
base_url = os.environ.get("LLM_BASE_URL", "https://api.xiaomimimo.com/v1")
model = os.environ.get("LLM_MODEL", "mimo-v2.5")

print(f"Base URL: {base_url}")
print(f"Model: {model}")
print(f"Key starts with: {api_key[:10]}...")

client = OpenAI(api_key=api_key, base_url=base_url)
try:
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "hello"}],
        max_tokens=50
    )
    print("SUCCESS!")
    print(resp.choices[0].message.content)
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
