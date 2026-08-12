"""
Demo 2: Tool Calling 深入
==========================
展示单轮 vs 多轮 tool call、工具链编排、Function Schema 调试

运行：python demo-tool-calling.py
前提：设置环境变量 DEEPSEEK_API_KEY=你的key
"""

import os
import json
from openai import OpenAI

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "your-key-here")
client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")
MODEL = "deepseek-chat"

# ── 一个更复杂的工具体系 ──────────────

def read_file(file_path: str) -> str:
    """模拟读文件"""
    mock_files = {
        "/project/config.json": '{"port": 8080, "debug": true, "db_host": "localhost"}',
        "/project/src/main.py": 'import config\nport = config.port\nprint(f"Server on {port}")',
        "/project/README.md": '# My Project\nA demo project for AI Agent learning'
    }
    content = mock_files.get(file_path)
    if content:
        return f"[文件内容]\n{content}"
    return f"错误: 文件不存在 - {file_path}"

def search_code(pattern: str) -> str:
    """模拟搜索代码库"""
    codebase = {
        "import config": ["/project/src/main.py:1"],
        "print": ["/project/src/main.py:3"],
        "port": ["/project/src/main.py:2", "/project/config.json:1"],
    }
    results = codebase.get(pattern, [])
    if results:
        return f"找到 {len(results)} 处匹配:\n" + "\n".join(f"  {r}" for r in results)
    return f"未找到 '{pattern}'"

def run_command(command: str) -> str:
    """模拟运行命令（实际不执行，只是演示）"""
    if "rm -rf" in command or "delete" in command.lower():
        return "⚠️ 危险命令被拦截"
    if "python" in command and "main.py" in command:
        return "Server on 8080\nServer started successfully"
    return f"命令已执行: {command}\n(模拟执行，实际未运行)"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "读取文件内容。返回文件的完整文本。",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "文件的绝对路径"
                    }
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_code",
            "description": "在代码库中搜索指定模式。返回匹配的文件路径和行号。",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "要搜索的文本模式"
                    }
                },
                "required": ["pattern"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "在终端中执行命令，返回输出。危险命令会被自动拦截。",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "要执行的 shell 命令"
                    }
                },
                "required": ["command"]
            }
        }
    }
]

TOOL_MAP = {
    "read_file": read_file,
    "search_code": search_code,
    "run_command": run_command,
}


def agent_loop(user_input: str, max_iterations: int = 15):
    """与 demo-agent-loop.py 相同的循环逻辑"""
    messages = [{"role": "user", "content": user_input}]
    tool_calls_made = []

    for i in range(max_iterations):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0.1
        )

        msg = response.choices[0].message

        if msg.tool_calls:
            messages.append(msg)
            for tc in msg.tool_calls:
                name = tc.function.name
                args = json.loads(tc.function.arguments)
                func = TOOL_MAP.get(name)
                result = func(**args) if func else f"未知工具: {name}"
                tool_calls_made.append(f"{name}({json.dumps(args, ensure_ascii=False)})")
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result
                })
        else:
            usage = response.usage
            return {
                "answer": msg.content,
                "tool_calls": tool_calls_made,
                "iterations": i + 1,
                "tokens": usage.total_tokens,
                "cost": usage.total_tokens * 2 / 1_000_000
            }

    return {"answer": "超时", "tool_calls": tool_calls_made, "iterations": max_iterations}


# ── 对比实验 ──────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("🔬 Tool Calling 深入对比实验")
    print("=" * 60)

    # 实验 1: 简单单轮调用（模型只需调一次工具）
    print("\n" + "="*60)
    print("实验 1: 简单单轮 ─ 读一个文件")
    print("="*60)
    result = agent_loop("帮我读一下 /project/config.json 的内容，告诉我端口号是多少")
    print(f"回答: {result['answer']}")
    print(f"工具调用链: {' → '.join(result['tool_calls'])}")
    print(f"循环轮次: {result['iterations']}, Tokens: {result['tokens']}, 费用: ¥{result['cost']:.4f}")

    # 实验 2: 多轮工具链（需要多次调用）
    print("\n" + "="*60)
    print("实验 2: 多轮工具链 ─ 搜索 + 读 + 分析")
    print("="*60)
    result = agent_loop(
        "帮我找一下项目里哪些文件用到了 'port'，然后读一下这些文件的内容，"
        "总结 port 的配置情况"
    )
    print(f"回答: {result['answer']}")
    print(f"工具调用链: {' → '.join(result['tool_calls'])}")
    print(f"循环轮次: {result['iterations']}, Tokens: {result['tokens']}, 费用: ¥{result['cost']:.4f}")

    # 实验 3: 工具结果不理想时 Agent 调整策略
    print("\n" + "="*60)
    print("实验 3: 错误恢复 ─ 读不存在的文件")
    print("="*60)
    result = agent_loop(
        "读一下 /project/nonexistent.py 然后告诉我内容"
    )
    print(f"回答: {result['answer']}")
    print(f"工具调用链: {' → '.join(result['tool_calls'])}")
    print(f"循环轮次: {result['iterations']}, Tokens: {result['tokens']}, 费用: ¥{result['cost']:.4f}")

    # 汇总对比
    print("\n" + "="*60)
    print("📊 对比总结")
    print("="*60)
    print("实验 1 (单轮): 快、便宜、适合简单任务")
    print("实验 2 (多轮): 慢、贵、能完成复杂任务")
    print("实验 3 (错误): Agent 会尝试调整，但可能浪费 token")
    print()
    print("💡 关键 insight:")
    print("   每一次 Tool Call = 一次 API 请求 = 一次计费")
    print("   多轮工具链虽然强大，但成本是单轮的好几倍")
