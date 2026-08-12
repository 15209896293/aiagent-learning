"""
Demo 1: 最小 Agent 循环
=======================
亲手跑一个 Agent 循环，理解 Think → Act → Observe → Repeat

运行：python demo-agent-loop.py
前提：设置环境变量 DEEPSEEK_API_KEY=你的key
"""

import os
import json
from openai import OpenAI

# ── 配置 ──────────────────────────────
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "your-key-here")
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# ── 定义工具 ──────────────────────────
# 这是 Agent 的"手"——能做的事

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前的日期和时间",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算。支持加减乘除和幂运算。",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 '2 + 3 * 4' 或 'pow(2, 10)'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "在本地知识库中搜索。搜索关键词：'capitals'（首都）、'population'（人口）、'rivers'（河流）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "要搜索的关键词，如 'capitals', 'population' 等"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# ── 工具实现 ──────────────────────────
# 这些函数是真正"做事"的地方，由宿主执行，不是模型

def get_current_time():
    from datetime import datetime
    return f"现在是 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

def calculate(expression: str):
    try:
        # 安全计算：只允许数字、运算符、括号、空格
        allowed = set("0123456789+-*/()^. ")
        if not all(c in allowed for c in expression):
            return f"表达式包含不允许的字符。只支持: 数字、+-*/()、^"
        # 替换 ^ 为 **
        expression = expression.replace("^", "**")
        result = eval(expression)
        return f"计算结果: {expression} = {result}"
    except Exception as e:
        return f"计算出错: {e}"

def search_knowledge_base(query: str):
    kb = {
        "capitals": "中国首都是北京，法国首都是巴黎，日本首都是东京",
        "population": "中国约14亿，印度约14亿，美国约3.3亿",
        "rivers": "长江6397公里，黄河5464公里，亚马逊6400公里"
    }
    return kb.get(query, f"知识库中没有关于 '{query}' 的信息")

# 工具名 → 实际函数的映射
TOOL_MAP = {
    "get_current_time": get_current_time,
    "calculate": calculate,
    "search_knowledge_base": search_knowledge_base,
}

# ── Agent 循环 ────────────────────────
# 这是 Agent 的核心！Think → Act → Observe → Repeat

def agent_loop(user_input: str, max_iterations: int = 10):
    """
    Agent 循环:
    1. 把用户输入 + 工具列表发给模型
    2. 模型决定: 直接回复 还是 调用工具
    3. 如果要调工具 → 宿主执行工具 → 结果塞回去 → 回到步骤 2
    4. 如果直接回复 → 打印回复 → 结束
    """
    messages = [{"role": "user", "content": user_input}]
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        print(f"\n{'─'*50}")
        print(f"🔄 循环第 {iteration} 轮")
        print(f"📤 发送给模型: {len(str(messages))} 字符的上下文")

        # 调用 API（带工具定义）
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0.1  # 低温度 = 更确定性的输出
        )

        choice = response.choices[0]
        msg = choice.message

        # 情况 1: 模型想调用工具
        if msg.tool_calls:
            print(f"🔧 模型决定调用工具:")
            messages.append(msg)  # 把模型的 tool_call 决定加入对话

            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                print(f"   → {name}({args})")

                # 宿主执行工具！
                func = TOOL_MAP.get(name)
                if func:
                    result = func(**args)
                else:
                    result = f"错误: 未知工具 '{name}'"

                print(f"   ← 结果: {result}")
                # 把工具执行结果塞回消息列表
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

        # 情况 2: 模型直接回复（完成任务）
        else:
            print(f"✅ Agent 完成任务:")
            print(f"   {msg.content}")
            print(f"\n📊 统计: 共循环 {iteration} 轮, "
                  f"消耗 {response.usage.total_tokens} tokens, "
                  f"费用约 ¥{(response.usage.total_tokens * 2 / 1_000_000):.4f}")
            return msg.content

    print(f"⚠️ 达到最大循环次数 ({max_iterations})，Agent 被迫停止")
    return None


# ── 运行 ──────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 最小 Agent 循环 Demo")
    print("=" * 50)
    print()
    print("Agent 有三种工具可用:")
    print("  1. get_current_time - 获取当前时间")
    print("  2. calculate - 执行数学计算")
    print("  3. search_knowledge_base - 搜索本地知识库")
    print()

    # 测试 1: 需要两次工具调用的问题
    print("\n" + "="*50)
    print("测试 1: 混合工具调用")
    print("="*50)
    agent_loop("现在几点了？顺便帮我算一下 123 * 456 等于多少")

    # 测试 2: 需要知识库的问题
    print("\n" + "="*50)
    print("测试 2: 知识库搜索")
    print("="*50)
    agent_loop("中国的首都是哪里？长江有多长？")

    # 测试 3: 不需要工具的问题
    print("\n" + "="*50)
    print("测试 3: 普通对话（不需要工具）")
    print("="*50)
    agent_loop("你好，用一句话解释什么是 Python")
