# 2.2 内置工具（Agent 自带的能力）

## Claude Code 的工具箱

Claude Code 启动时，自带一套工具。你在对话中看到的每一次文件读写、搜索、命令执行，都是这些工具在工作。

### 完整工具清单

```
文件操作
├── Read       读取文件（你就是用这个看到代码的）
├── Write      创建/覆写文件
├── Edit       精确替换文件中的字符串
└── Glob       按文件名模式搜索（找所有 *.ts 文件）

搜索
├── Grep       按内容搜索（正则匹配）
└── Bash       执行 shell 命令（可以跑 find/grep/...）

Agent
├── Agent      启动一个子 Agent 做独立任务
└── Task       创建/跟踪任务列表

网络
├── WebSearch  搜索网页（需要权限）
└── WebFetch   抓取网页内容

会话管理
├── AskUserQuestion  问你选择题
├── EnterPlanMode    进入规划模式
└── ExitPlanMode     退出规划模式
```

---

## 每个工具的边界和危险区

### Read
```
安全区 ✅ 读取源文件、配置文件、文档
危险区 ⚠️  读取密钥文件（.env, credentials.json）后内容进入上下文
        → 如果你的对话历史被泄露，密钥也跟着泄露
红线   🛑 不要在 Agent 里让它读你的 ~/.ssh/id_rsa
```

### Write
```
安全区 ✅ 创建新文件、写 demo 代码
危险区 ⚠️  覆写已存在的文件（Write 会直接覆盖，没有确认）
        → 如果路径写错，可能覆盖到不相关的文件
红线   🛑 不要在你不认识的目录里用 Write
```

### Edit
```
安全区 ✅ 改一小段代码
危险区 ⚠️  old_string 必须完全匹配（空格、换行都对齐），否则失败
        → 模型可能"发明"一段看起来像但不存在的代码来匹配
红线   🛑 不要让 Agent 在没有 Read 过的情况下直接 Edit
```

### Bash
```
安全区 ✅ 运行开发命令：npm test、git status、python demo.py
危险区 ⚠️  任何有副作用的命令：npm install -g、git push、rm
        → Bash 用你的用户权限运行，能做的事你都能做
红线   🛑 rm -rf、git push --force、curl | bash、chmod 777
```

### Agent
```
安全区 ✅ 让子 Agent 去独立探索代码库
危险区 ⚠️  子 Agent 也有完整的工具权限，可以改文件
        → 你可能不知道子 Agent 改了什么东西
红线   🛑 多个 Agent 同时改同一个文件（冲突）
```

---

## Trae 的内置工具

| 工具 | 能力 |
|------|------|
| 代码补全 | 实时补全你正在写的代码 |
| Chat | 侧边栏对话 |
| Inline Edit | 选中代码 → 告诉 AI 怎么改 → 自动替换 |
| Terminal | 跑终端命令 |
| 文件操作 | 读/写/搜索项目文件 |

Trae 的工具比 Claude Code 更"GUI 化"——你看不到工具调用的 JSON，看到的是 UI 变化。

---

## ZCode 的内置工具

ZCode 的工具体系类似 Trae——侧重在 IDE 内的代码操作：
- 代码生成和编辑
- 文件搜索
- 终端集成
- 部分版本控制操作

---

## 每种工具的能力边界

一个误区：以为 Agent 有工具就什么都能做。

```
Agent 能做到的           Agent 做不到的
─────────────────────    ─────────────────
读任何文本文件            读二进制文件（图片、exe、zip 里的内容）
写/改源代码               保证代码能编译/运行
搜索代码内容              理解你的业务逻辑
跑 shell 命令             登录需要交互式认证的服务
浏览网页（需要 MCP）       直接操作数据库（需要 MCP）
读项目结构                记住你上周的对话（上下文限制）
```

---

## 工具使用的最佳实践

### 1. 读文件：Read 优先于 Bash cat
Read 工具的结果有行号、能点击跳转。Bash cat 输出是纯文本。Agent 应该优先用 Read。

### 2. 搜索内容：Grep 优先于 Bash grep
Grep 工具支持正则、多行模式、文件类型过滤。比手动拼 bash grep 命令可靠。

### 3. 编辑文件：Edit 优先于 Write
Edit 只改指定部分，Write 会覆盖整个文件。修改一个函数的时候用 Edit，创建新文件时用 Write。

### 4. 终端操作：只跑你懂的
如果 Agent 提出了一个你看不懂的 shell 命令，先让它解释再批准。

---

## 自检清单

- [ ] 能列出 Claude Code 的 5 种以上内置工具
- [ ] 知道 Read / Write / Edit / Bash 各自的安全边界
- [ ] 理解 Edit 的 old_string 匹配为什么容易失败
- [ ] 能分辨 Agent "能做到"和"做不到"的事
- [ ] 知道什么时候用 Read 而不是 Bash cat
