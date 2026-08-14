# 2.3 MCP（Model Context Protocol）

## 一句话

**MCP = Agent 的"插件协议"。** 就像浏览器的 Chrome 扩展、VS Code 的插件市场——MCP 让 Agent 能接入外部工具和数据源。

---

## 为什么需要 MCP

内置工具有限：

```
Claude Code 内置：读文件 ✅  查数据库 ❌  看网页 ❌  操作 GitHub ❌
```

如果每个外部服务都需要 Claude Code 团队自己写集成，永远覆盖不完。所以 Anthropic 发布了 MCP——一个**标准协议**，第三方按这个协议写 Server，Agent 就能无缝对接。

---

## MCP 怎么工作的

```
┌──────────────────┐
│   Claude Code     │  ← Agent 宿主
│   (MCP Client)    │
└──────┬───────────┘
       │ MCP 协议（JSON-RPC over stdio/HTTP）
       ├──────────────┐
       ↓              ↓
┌─────────────┐ ┌─────────────┐
│ MCP Server  │ │ MCP Server  │  ← 独立进程
│ (文件系统)   │ │ (GitHub)    │
│             │ │             │
│ 能做的事：   │ │ 能做的事：   │
│ 读/写文件   │ │ 管理 PR     │
│ 搜索目录    │ │ 查看 commits│
│ 获取文件元数据│ │ 创建 issue  │
└─────────────┘ └─────────────┘
```

**核心架构：**
- MCP Server 是一个独立进程，跑在你的机器上
- Claude Code 通过 MCP 协议与 Server 通信
- Server 暴露"工具列表"给 Claude Code
- Claude Code 的 Agent 看到这些工具就像看到内置工具一样，可以直接调用

---

## 常见的 MCP Server

| MCP Server | 能干什么 | 什么时候用 |
|------------|----------|------------|
| **filesystem** | 安全地读/写/搜索文件 | 让 Agent 操作指定目录 |
| **github** | 管理 PR、Issue、Actions | 用 Agent 做代码审查、自动发 PR |
| **postgres** | 查询数据库 | Agent 帮你查数据 |
| **playwright** | 控制浏览器 | Agent 自动测试网页、截图 |
| **brave-search** | 搜索网络 | Agent 查找最新信息 |
| **memory** | 持久化记忆 | Agent 跨会话记住偏好 |
| **docker** | 管理容器 | Agent 操作 Docker |

---

## MCP 的生命周期

```
1. 配置
   在 claude_desktop_config.json 或 settings.json 里声明：
   {
     "mcpServers": {
       "playwright": {
         "command": "npx",
         "args": ["@anthropic-ai/mcp-server-playwright"]
       }
     }
   }

2. 启动
   Claude Code 启动时，自动拉起配置的 MCP Server 进程

3. 工具发现
   MCP Server 告诉 Claude Code：
   "我有这些工具：browser_navigate, browser_click, browser_snapshot..."

4. Agent 调用
   用户说 "帮我打开百度截图"
   → Agent 决定调用 browser_navigate("https://baidu.com")
   → Claude Code 通过 MCP 协议发给 playwright MCP Server
   → Server 执行，返回结果
   → Agent 继续调用 browser_take_screenshot()
   → Server 执行，返回截图

5. 关闭
   Claude Code 退出时，自动关闭 MCP Server 进程
```

---

## MCP 的超能力示例

### 例子：用 Agent 操作浏览器

```
你：帮我登录 GitHub，看看我有哪些未读通知

Agent 的工具链：
1. browser_navigate("https://github.com/login")
2. browser_snapshot() → 看到登录表单
3. browser_type("用户名输入框", "你的用户名")
4. browser_type("密码输入框", "你的密码")
5. browser_click("Sign in 按钮")
6. browser_navigate("https://github.com/notifications")
7. browser_snapshot() → 看到通知列表
8. "你有 3 条未读通知：..."
```

每一步都是 MCP Server 在真实浏览器中执行。

### 例子：Agent 直接查数据库

```
你：帮我查一下昨天注册的用户有多少个

Agent 的工具链：
1. mcp_postgres_query("SELECT COUNT(*) FROM users WHERE created_at > '2026-07-02'")
2. "昨天注册了 128 个用户"
```

---

## MCP 的安全模型（这是关键）

> ⚠️ **MCP Server 跑在你的机器上，权限和你一样大。**

如果你装了一个恶意的 MCP Server，它可以：
- 读你所有文件
- 删你文件
- 发网络请求（攻击内网）
- 执行命令

### 安全规则

1. **只装你信任的 MCP Server**
2. **看源码**：这个 Server 到底做了什么
3. **限制目录**：filesystem MCP Server 只给特定目录权限，别给 `/` 或 `C:\`
4. **不用时关掉**：配置里不需要的 Server 删掉
5. **审权限**：如果一个 MCP Server 要求的权限让你不舒服，别装

---

## MCP vs 内置工具 vs API

| | 内置工具 | MCP | 直接调 API |
|---|---|---|---|
| 谁提供 | Claude Code 内置 | 第三方开发 | 你自己写代码 |
| 怎么装 | 开箱即用 | 配置文件声明 | 需要编程 |
| 灵活性 | 固定 | 中等 | 最高 |
| 安全性 | 经过 Anthropic 审查 | 取决于开发者 | 你自己掌握 |

---

## 在你的工具里

| 工具 | MCP 支持 |
|------|----------|
| Claude Code | ✅ 完整支持，通过 settings.json 配置 |
| Trae | ⚠️ 不支持或有限支持 |
| ZCode | ⚠️ 取决于版本 |

**MCP 是 Claude Code 的独占优势。** 这也是为什么 Claude Code 能做的事比 Trae/ZCode 多——它可以通过 MCP 接入任意外部工具。

---

## 你的 Claude Code 已经在用 MCP

你现在已经配了两个 MCP Server：
- `computer-control` — 文件操作和命令执行
- `playwright` — 浏览器自动化

去看看你的 `settings.json` 就明白了。

---

## 自检清单

- [ ] 能解释 MCP 是什么以及为什么需要它
- [ ] 能画出 MCP Client-Server 架构图
- [ ] 知道至少 3 种常见的 MCP Server 和它们的用途
- [ ] 理解 MCP 的安全模型和风险
- [ ] 知道你的 Claude Code 已装了哪些 MCP Server
- [ ] 能区分 MCP vs 内置工具 vs 直接 API 调用
