import random


def web_search(query: str) -> str:
    mock_results = {
        "股票": "股票是公司所有权的凭证。A股交易时间为周一至周五9:30-15:00，T+1制度，主板涨跌幅±10%。",
        "python": "Python是一种高级编程语言，广泛用于AI、数据分析、Web开发。最新稳定版为Python 3.12。",
        "人工智能": "人工智能(AI)是计算机科学的一个分支，旨在创建能模拟人类智能的系统。2024-2025年大模型(LLM)是最热门方向。",
        "机器学习": "机器学习是AI的子领域，通过数据训练模型来做预测。常见算法包括决策树、SVM、神经网络等。",
    }
    for key, value in mock_results.items():
        if key in query:
            return f"搜索结果: {value}"
    return f"搜索结果: 关于「{query}」的信息，请参考相关专业资料。"


WEB_SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "搜索互联网获取最新信息。输入搜索关键词，返回搜索结果摘要。",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索关键词"
                }
            },
            "required": ["query"]
        }
    }
}
