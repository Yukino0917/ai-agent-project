import os
from openai import OpenAI


def get_client():
    api_key = os.environ.get("OPENAI_API_KEY", "")
    base_url = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
    return OpenAI(api_key=api_key, base_url=base_url)


def chat(messages: list, model: str = None, tools: list = None) -> dict:
    client = get_client()
    model = model or os.environ.get("LLM_MODEL", "gpt-4o-mini")
    kwargs = {
        "model": model,
        "messages": messages,
        "max_tokens": 2048,
        "temperature": 0.7,
    }
    if tools:
        kwargs["tools"] = tools
    return client.chat.completions.create(**kwargs)


def simple_chat(user_input: str, history: list = None) -> str:
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_input})
    response = chat(messages)
    return response.choices[0].message.content
