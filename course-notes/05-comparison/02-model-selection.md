# 5.2 模型选型实战

## 一张决策矩阵

| 任务类型 | 推荐模型 | 为什么 |
|----------|----------|--------|
| 复杂重构、架构设计 | Claude Opus / GPT-5 | 推理最强 |
| 日常开发、写功能 | Claude Sonnet | 性价比最优 |
| 简单脚本、翻译 | Claude Haiku / GPT-4o-mini | 快且便宜 |
| 数学推理、逻辑推导 | Claude Opus / DeepSeek-R1 | 推理模型 |
| 中文内容、文案 | DeepSeek-V3 | 中文最好 |
| 长文档分析 | Gemini 2.5 Pro | 200 万上下文 |
| 省钱省到极致 | DeepSeek-V3 | 比 Claude 便宜 80%+ |

---

## 实际测试：同一个任务，三个模型

### 任务
> 用 Python 写一个文件监控脚本，监控 `./data/` 目录，当有新文件时自动解析 CSV 并存入 SQLite

### Claude Sonnet（$3/$15 per 1M tokens）

```python
import os
import csv
import sqlite3
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CSVHandler(FileSystemEventHandler):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS csv_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT,
                    row_data TEXT,
                    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith('.csv'):
            return
        self._import_csv(event.src_path)
    
    def _import_csv(self, filepath: str):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = [dict(row) for row in reader]
            
            with sqlite3.connect(self.db_path) as conn:
                for row in rows:
                    conn.execute(
                        "INSERT INTO csv_data (filename, row_data) VALUES (?, ?)",
                        (os.path.basename(filepath), str(row))
                    )
            print(f"Imported {len(rows)} rows from {filepath}")
        except Exception as e:
            print(f"Error importing {filepath}: {e}")

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(CSVHandler("data.db"), "./data/", recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

**评价：** 结构清晰，有错误处理，用了合适的库（watchdog）、参数化 SQL（防注入）、utf-8 编码、KeyboardInterrupt 优雅退出。**可以直接用。**

### DeepSeek-V3（¥2/¥8 per 1M tokens）

同样的 prompt，DeepSeek 的实现：
- 也是用的 watchdog
- 但可能会加更多中文注释
- 可能会过度设计（加了配置文件、日志系统、命令行参数解析）
- 代码量可能是 Claude 的 2-3 倍

**评价：** 也能跑，但"工程化"过度——你只想要一个监控脚本，它给你整了个框架。

### GPT-4o-mini（$0.15/$0.60 per 1M tokens）

同样的 prompt，GPT-4o-mini：
- 可能不用 watchdog，而是自己写了一个简陋的文件轮询
- 错误处理更少
- 可能有小 bug（比如忘了处理 csv.DictReader 的编码）

**评价：** 能用但需要检查。便宜是真的便宜。

---

## 推理模型 vs 通用模型

### 通用模型（Claude Sonnet / GPT-4o / DeepSeek-V3）
```
输入 → 输出
一句话过来，直接开始生成回复
→ 速度快、成本低
→ 复杂推理可能不完整
```

### 推理模型（Claude Opus with thinking / DeepSeek-R1 / o1）
```
输入 → 内部思考（你看不到）→ 输出
模型在回复前会"自言自语"一段推理过程
→ 速度慢、成本高（思考过程也计费）
→ 复杂逻辑更准确
```

### 什么时候用推理模型
```
✅ 需要多步推理：数学证明、复杂算法设计
✅ 需要权衡多种方案：架构选型、重构策略
✅ 容易出错的逻辑：并发代码、边界条件复杂的函数

❌ 简单问答、代码翻译、格式转换
❌ 已知需求的常规开发（Sonnet 足够）
```

### 代价
```
通用模型：你只付 output 的 token
推理模型：你付 thinking token + output token
         → thinking 可能有几千到几万 token
         → 费用是通用模型的 2-5 倍
```

---

## 开源模型能替代吗（本地跑 vs 云 API）

### 优势
- 免费（不计 token，不计次数）
- 数据不出本机（隐私）
- 可以微调

### 劣势
- 需要 GPU（最低 16GB 显存，推荐 24GB+）
- 设置复杂（Ollama、vLLM、量化、模型下载）
- 能力差距：同等数量参数的本地模型 < 云模型
- 没有内置的 Tool Calling 支持（需要自己实现）

### 你的情况
你是大一学生，估计没有 4090。所以：
- **不要考虑本地跑大模型**
- 继续用 DeepSeek API（便宜 + 够用）
- 如果以后有 GPU 了，可以试试 Qwen 2.5 的本地部署

---

## 你的模型选择策略

```
日常主力：DeepSeek-V3（省钱）
核心策略：需要强推理时切 Claude Sonnet
         → Claude Code 里 /model sonnet /model deepseek 切换

免费额度：Trae（字节免费），能省则省

什么时候不要省：
  → 复杂 bug 调试（省的几毛钱不够浪费的时间）
  → 安全敏感的代码审查（需要用最强的模型）
  → 学习新概念（好的解释比便宜的解释值钱）
```

---

## 自检清单

- [ ] 能根据任务类型选择合适的模型
- [ ] 知道推理模型和通用模型的区别及代价
- [ ] 理解开源模型本地部署的门槛
- [ ] 有自己的模型选择策略（不只是"用最便宜的"或"用最贵的"）
