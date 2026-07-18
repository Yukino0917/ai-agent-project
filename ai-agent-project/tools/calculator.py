import math


def calculator(expression: str) -> str:
    safe_dict = {
        "abs": abs, "round": round, "min": min, "max": max,
        "sum": sum, "pow": pow, "int": int, "float": float,
        "pi": math.pi, "e": math.e,
        "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "ceil": math.ceil, "floor": math.floor,
    }
    try:
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        return f"计算结果: {expression} = {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"


CALCULATOR_TOOL = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "执行数学计算。输入一个数学表达式字符串，返回计算结果。支持基本运算和常用数学函数。",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "数学表达式，如 '2 + 3 * 4' 或 'sqrt(144)'"
                }
            },
            "required": ["expression"]
        }
    }
}
