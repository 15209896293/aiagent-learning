# 2.1 Tool Calling 底层机制

## 模型不会"执行"任何东西

这是最重要的一个认知：

**大语言模型只能输出文本。它不能执行代码、不能读文件、不能发 HTTP 请求、不能操作数据库。**

它唯一能做的是：**生成一段文本**。

那 Agent 是怎么"做事"的？秘密在于 Tool Calling——模型输出一段特殊的 JSON，告诉宿主程序"我想调用这个工具"，宿主程序替它执行，把结果回传给模型。

---

## 完整生命周期

```
┌─────────────────────────────────────────────────────┐
│  1. 你发送消息                                        │
│     "帮我读一下 config.json 的内容"                    │
│     ↓                                                │
│  2. 模型推理                                          │
│     "用户想读文件，我有 read_file 工具可用，            │
│      参数 file_path 应该是 'config.json'"              │
│     ↓                                                │
│  3. 模型输出（不是回复文本！）                           │
│     {                                                │
│       "tool": "read_file",                            │
│       "parameters": { "file_path": "config.json" }    │
│     }                                                │
│     ↓                                                │
│  4. 宿主程序（Claude Code / 你的 Python 代码）收到 JSON│
│     宿主程序真实地读取 config.json                     │
│     ↓                                                │
│  5. 宿主程序把结果塞回给模型                            │
│     [Tool Result] {"content": "{\"port\": 8080}...",  │
│                    "file_path": "config.json"}        │
│     ↓                                                │
│  6. 模型再次推理                                      │
│     "config.json 里写的是 port: 8080，端口 8080"       │
│     ↓                                                │
│  7. 模型输出真正的回复                                 │
│     "你的配置文件里端口设置是 8080"                     │
└─────────────────────────────────────────────────────┘
```

关键点：
- 步骤 2-3：模型**决定**调用什么工具，但**不执行**工具
- 步骤 4：**宿主程序**才是真正的执行者
- 步骤 5-6：执行结果**塞回上下文**，模型基于结果继续推理
- 如果模型需要再调用工具（比如读另一个文件），返回步骤 2

---

## Function Schema（工具定义）

在调用 API 时，你把可用的工具以 JSON Schema 形式传过去：

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "读取一个文件的内容",
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
            "name": "write_file",
            "description": "创建或覆盖一个文件",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "文件的绝对路径"
                    },
                    "content": {
                        "type": "string",
                        "description": "要写入的内容"
                    }
                },
                "required": ["file_path", "content"]
            }
        }
    }
]
```

每个工具的定义包含：
- **name**：工具名（模型用这个名字来"叫"工具）
- **description**：描述（模型靠这个理解工具的用途）
- **parameters**：参数 Schema（模型按这个格式输出参数）

---

## 工具描述的技巧

### 描述决定模型会不会正确使用工具

**❌ 不好的：**
```json
{"name": "search", "description": "搜索东西"}
```
→ 模型不知道搜什么、返回什么、参数是什么

**✅ 好的：**
```json
{
    "name": "search_codebase",
    "description": "在代码库中搜索正则匹配的内容。返回匹配的文件路径和行号。用于查找函数定义、变量引用、或特定模式。",
    "parameters": {
        "pattern": {
            "description": "要搜索的正则表达式。例如 'def login' 或 'import.*os'"
        },
        "directory": {
            "description": "搜索的目录路径（绝对路径）"
        }
    }
}
```

### 规则

1. **描述要精确**：说明工具做什么、返回什么
2. **说明使用场景**：什么时候该用这个工具而不是别的
3. **参数描述要有例子**：模型通过例子理解参数格式
4. **区分相似工具**：如果有 `read_file` 和 `search_content`，在描述里说清楚什么时候用哪个

---

## 单轮 vs 多轮工具链

### 单轮
模型调用一次工具，拿到结果，回复用户。
```
用户：config.json 里端口是多少？
模型 → read_file("config.json")
宿主 → 文件内容
模型 → "端口是 8080"
```

### 多轮工具链
模型连续调用多个工具，形成执行链。
```
用户：帮我找到所有用了 axios 的文件，把其中的 axios 调用改成 fetch

模型 → search_content(pattern="import axios")
宿主 → ["src/api.ts", "src/utils.ts", "src/login.ts"]
模型 → read_file("src/api.ts")
宿主 → 文件内容...
模型 → read_file("src/utils.ts")
宿主 → 文件内容...
模型 → read_file("src/login.ts")
宿主 → 文件内容...
模型 → write_file("src/api.ts", 改后的内容)
宿主 → 写入成功
模型 → write_file("src/utils.ts", 改后的内容)
宿主 → 写入成功
模型 → write_file("src/login.ts", 改后的内容)
宿主 → 写入成功
模型 → "已完成，修改了 3 个文件"
```

**每一次调用都是一次完整的 API 请求。** 这个例子用了 7 次 API 请求（1 次搜索 + 3 次读 + 3 次写）。

---

## Tool Calling 与 Agent 循环的区别

很多人混淆这两个概念：

| | Tool Calling | Agent 循环 |
|---|---|---|
| 定义 | 模型调用工具的**单次能力** | 模型在循环中**持续调用工具直到完成任务** |
| 谁控制 | 模型自己决定要不要调 | 宿主程序写 while 循环 |
| 代码量 | API 自带支持 | 需要自己或用框架实现 |

Agent 循环 = Tool Calling + while 循环（详见模块三 3.4 和第 11 课）

---

## 在你的工具里

| 工具 | Tool Calling 实现 |
|------|-------------------|
| Claude Code | 内置了 read/write/edit/search/bash 等几十种工具 |
| Trae | 内置工具（读文件、改代码、跑命令） |
| ZCode | 类似内置工具集 |

**你看不到 JSON，但每次 Agent 读文件/改代码时，背后都是 Tool Calling 在运作。**

---

## 自检清单

- [ ] 能画出 Tool Calling 的 7 步完整生命周期
- [ ] 能写出一个规范的 Function Schema
- [ ] 知道描述质量如何影响模型的工具使用准确率
- [ ] 能区分单轮工具调用和多轮工具链
- [ ] 理解 Tool Calling 和 Agent 循环的区别
- [ ] 知道 Claude Code 每一次读/写文件背后都是一次 Tool Call
