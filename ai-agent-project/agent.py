import json
from utils.llm import chat
from tools.calculator import calculator, CALCULATOR_TOOL
from tools.knowledge import search_knowledge, KNOWLEDGE_TOOL
from tools.web_search import web_search, WEB_SEARCH_TOOL

SYSTEM_PROMPT = """你是一个智能助手 Agent。你可以：
1. 回答各种知识问题
2. 使用 calculator 工具进行数学计算
3. 使用 search_knowledge 工具从知识库检索信息
4. 使用 web_search 工具搜索互联网信息

回答时请：
- 用中文回答
- 如果用户问的问题需要计算，先调用 calculator 工具
- 如果涉及专业知识，先调用 search_knowledge 工具检索知识库
- 如果需要最新信息，调用 web_search 工具
- 回答简洁明了，适合普通用户理解
- 如果不确定答案，请诚实告知
"""

TOOLS = [CALCULATOR_TOOL, KNOWLEDGE_TOOL, WEB_SEARCH_TOOL]

TOOL_MAP = {
    "calculator": calculator,
    "search_knowledge": search_knowledge,
    "web_search": web_search,
}


class Agent:
    def __init__(self):
        self.history = []
        self.max_rounds = 5

    def run(self, user_input: str) -> str:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": user_input})

        for round_num in range(self.max_rounds):
            response = chat(messages, tools=TOOLS)
            message = response.choices[0].message

            if message.tool_calls:
                messages.append(message.model_dump())
                for tool_call in message.tool_calls:
                    func_name = tool_call.function.name
                    func_args = json.loads(tool_call.function.arguments)

                    if func_name in TOOL_MAP:
                        result = TOOL_MAP[func_name](**func_args)
                    else:
                        result = f"未知工具: {func_name}"

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result),
                    })
            else:
                final_answer = message.content
                self.history.append({"role": "user", "content": user_input})
                self.history.append({"role": "assistant", "content": final_answer})
                if len(self.history) > 20:
                    self.history = self.history[-20:]
                return final_answer

        return "抱歉，处理过程中出现了问题，请重试。"

    def clear_history(self):
        self.history = []

