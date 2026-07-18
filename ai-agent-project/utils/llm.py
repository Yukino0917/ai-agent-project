from openai import OpenAI
from config.settings import OPENAI_API_KEY, LLM_BASE_URL, LLM_MODEL, MAX_TOKENS, TEMPERATURE


def get_client():
    return OpenAI(api_key=OPENAI_API_KEY, base_url=LLM_BASE_URL)


def chat(messages: list[dict], model: str = None, tools: list = None) -> dict:
    client = get_client()
    kwargs = {
        "model": model or LLM_MODEL,
        "messages": messages,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
    }
    if tools:
        kwargs["tools"] = tools
    return client.chat.completions.create(**kwargs)


def simple_chat(user_input: str, history: list[dict] = None) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_input})
    response = chat(messages)
    return response.choices[0].message.content


SYSTEM_PROMPT = """你是一个智能助手 Agent。你可以：
1. 回答各种知识问题
2. 使用计算器工具进行数学计算
3. 从知识库中检索信息来回答问题

回答时请：
- 用中文回答
- 如果需要计算，调用 calculator 工具
- 如果涉及专业知识，先检索知识库再回答
- 回答简洁明了，适合普通用户理解
"""
