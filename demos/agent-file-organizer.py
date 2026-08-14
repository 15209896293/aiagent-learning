"""
Agent Demo: 文件整理 Agent
==========================
一个完整的、能实际运行的文件整理 Agent。
根据文件扩展名自动分类移动到对应文件夹。

这个脚本展示了一个完整 Agent 的所有组件:
- System Prompt（人设）
- Tool Schema（工具定义）
- Agent 循环（Think → Act → Observe）
- 安全边界（危险操作拦截）

用法：
  1. 设置 DEEPSEEK_API_KEY 环境变量
  2. python agent-file-organizer.py /path/to/folder

示例：
  python agent-file-organizer.py ./fixtures
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from openai import OpenAI


# ═══════════════════════════════════════
# 配置
# ═══════════════════════════════════════

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "your-key-here")
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# 文件类型 → 目标文件夹映射
CATEGORY_RULES = {
    "图片": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "文档": [".pdf", ".doc", ".docx", ".txt", ".md", ".xlsx", ".pptx", ".csv", ".json"],
    "代码": [".py", ".js", ".ts", ".html", ".css", ".java", ".go", ".rs", ".cpp", ".c", ".h"],
    "压缩包": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "视频": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
    "音频": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
    "安装包": [".exe", ".msi", ".dmg", ".deb", ".apk"],
    "其他": []  # fallback
}


# ═══════════════════════════════════════
# 工具实现（Agent 的"手"）
# ═══════════════════════════════════════

def scan_directory(directory: str) -> str:
    """
    扫描目录，返回所有文件的信息。
    只扫描文件，不递归子目录。
    """
    path = Path(directory)
    if not path.exists():
        return f"❌ 目录不存在: {directory}"
    if not path.is_dir():
        return f"❌ 不是目录: {directory}"

    files = []
    for f in path.iterdir():
        if f.is_file():
            stat = f.stat()
            size_kb = stat.st_size / 1024
            mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            ext = f.suffix.lower()
            category = get_category(ext)
            files.append({
                "name": f.name,
                "ext": ext,
                "size_kb": round(size_kb, 1),
                "modified": mtime,
                "category": category
            })

    if not files:
        return f"📂 {directory} 是空的，没有文件。"

    lines = [f"📂 {directory} 中有 {len(files)} 个文件:"]
    for f in sorted(files, key=lambda x: x['category']):
        lines.append(
            f"  [{f['category']}] {f['name']} "
            f"({f['size_kb']}KB, {f['modified']})"
        )
    return "\n".join(lines)


def get_category(ext: str) -> str:
    """根据扩展名判断文件类别"""
    for category, extensions in CATEGORY_RULES.items():
        if ext in extensions:
            return category
    return "其他"


def move_file(file_name: str, source_dir: str, target_category: str) -> str:
    """
    将文件移动到对应类别的子文件夹中。
    如果目标文件夹不存在则自动创建。
    """
    source = Path(source_dir) / file_name
    if not source.exists():
        return f"❌ 文件不存在: {source}"

    if target_category not in CATEGORY_RULES:
        return f"❌ 未知类别: {target_category}。可选: {list(CATEGORY_RULES.keys())}"

    # 创建目标文件夹
    target_dir = Path(source_dir) / target_category
    target_dir.mkdir(exist_ok=True)

    target = target_dir / file_name

    # 处理重名
    if target.exists():
        stem = target.stem
        suffix = target.suffix
        target = target_dir / f"{stem}_副本{suffix}"
        if target.exists():
            return f"⚠️ 目标位置已有同名文件且副本也存在: {file_name}"

    shutil.move(str(source), str(target))
    return f"✅ 已移动: {file_name} → {target_category}/"


def undo_last_move(file_name: str, source_dir: str, target_category: str) -> str:
    """撤销上一次移动操作"""
    target_dir = Path(source_dir) / target_category
    source = target_dir / file_name
    dest = Path(source_dir) / file_name

    if not source.exists():
        return f"❌ 无法撤销: {source} 不存在"

    shutil.move(str(source), str(dest))
    return f"↩️ 已撤销: {target_category}/{file_name} → {file_name}"


# 工具 Schema（告诉模型它能做什么）
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "scan_directory",
            "description": "扫描目录中的所有文件，列出文件名、大小、修改时间、类别。在整理文件之前必须先扫描了解情况。",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "要扫描的目录的绝对路径"
                    }
                },
                "required": ["directory"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "move_file",
            "description": "将一个文件移动到对应类别的子文件夹。类别包括: 图片、文档、代码、压缩包、视频、音频、安装包、其他。",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {
                        "type": "string",
                        "description": "要移动的文件名（不含路径，只给文件名）"
                    },
                    "source_dir": {
                        "type": "string",
                        "description": "文件所在的目录的绝对路径"
                    },
                    "target_category": {
                        "type": "string",
                        "description": "目标类别，如 '图片'、'文档'、'代码' 等"
                    }
                },
                "required": ["file_name", "source_dir", "target_category"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "undo_last_move",
            "description": "撤销上一次移动操作，把文件移回原位。仅在用户要求撤销时使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_name": {"type": "string"},
                    "source_dir": {"type": "string"},
                    "target_category": {"type": "string"}
                },
                "required": ["file_name", "source_dir", "target_category"]
            }
        }
    }
]

TOOL_MAP = {
    "scan_directory": scan_directory,
    "move_file": move_file,
    "undo_last_move": undo_last_move,
}

# ═══════════════════════════════════════
# System Prompt（Agent 的"人设"）
# ═══════════════════════════════════════

SYSTEM_PROMPT = """你是一个文件整理助手。你的任务是帮助用户整理文件夹中的文件。

工作流程：
1. 用户告诉你一个目录路径
2. 你先用 scan_directory 工具扫描目录，了解有什么文件
3. 你告诉用户文件的分类情况
4. 用户确认后，你用 move_file 逐个（或批量）移动文件

行为规则：
- 移动文件前必须先扫描
- 每次移动前告诉用户你要做什么
- 如果一个文件已经有分类好了的文件夹，跳过它
- 不要移动文件夹（目录），只移动文件
- 遇到不知道类型的文件，放到"其他"类别
- 如果用户说"撤销"，用 undo_last_move

安全规则：
- 绝对不要移动 .exe, .msi, .dmg, .apk 等可执行文件（安装包类别跳过）
- 不要移动隐藏文件（以 . 开头的文件）
- 不要操作 C:\\Windows, C:\\Program Files 等系统目录
"""


# ═══════════════════════════════════════
# Agent 循环
# ═══════════════════════════════════════

def agent_loop(user_input: str, max_iterations: int = 20):
    """
    完整的 Agent 循环:
    Think (模型推理) → Act (宿主执行工具) → Observe (结果回传) → Repeat
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]

    for i in range(max_iterations):
        print(f"\n🔄 第 {i+1} 轮...")

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0.1
        )

        msg = response.choices[0].message

        if msg.tool_calls:
            # 模型想调用工具
            messages.append(msg)
            for tc in msg.tool_calls:
                name = tc.function.name
                args = json.loads(tc.function.arguments)
                print(f"  🔧 {name}({json.dumps(args, ensure_ascii=False)})")

                func = TOOL_MAP.get(name)
                if func:
                    result = func(**args)
                else:
                    result = f"❌ 未知工具: {name}"

                print(f"  📋 {result[:100]}{'...' if len(result) > 100 else ''}")
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result
                })
        else:
            # 模型直接回复
            print(f"  💬 {msg.content}")
            return msg.content

    return "⚠️ 达到最大循环次数"


# ═══════════════════════════════════════
# 主程序
# ═══════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 文件整理 Agent")
    print("=" * 60)

    # 获取目标目录
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        # 默认用 fixtures
        target_dir = os.path.join(os.path.dirname(__file__), "fixtures")
        print(f"💡 未指定目录，使用默认: {target_dir}")
        print(f"💡 用法: python agent-file-organizer.py /path/to/folder")

    # 确保目录存在
    Path(target_dir).mkdir(parents=True, exist_ok=True)

    print(f"\n🎯 目标目录: {target_dir}")
    print("\n键入 '整理' 开始整理，键入 '撤销' 撤销上一步，键入 '退出' 结束\n")

    # 交互循环
    while True:
        user_input = input("👤 你: ").strip()
        if not user_input:
            continue
        if user_input in ("退出", "quit", "exit", "q"):
            print("👋 再见！")
            break

        # 把目标目录自动加到用户输入里
        full_input = f"目标目录: {target_dir}\n用户指令: {user_input}"
        response = agent_loop(full_input)
        print(f"\n🤖 Agent: {response}")
