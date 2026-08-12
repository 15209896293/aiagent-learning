# 2.5 Hooks（钩子/自动化触发器）

## 一句话

**Hook = "每当 X 发生时，自动执行 Y"。**

不需要你手动触发，Agent 在特定事件发生时自动跑一段逻辑。

---

## 为什么需要 Hooks

没有 Hook：
```
你在 Claude Code 里写完代码
→ 你手动说 "帮我运行测试"
→ Agent 跑测试
→ 测试失败了
→ 你手动说 "帮我修这个测试失败"
→ Agent 改代码
→ 你又手动说 "帮我再跑一次测试"
```

有 Hook：
```
你在 Claude Code 里写完代码
→ Claude Code 检测到文件保存
→ Hook 自动触发：跑测试
→ 测试失败
→ Hook 自动通知你
→ 你让 Agent 修 → Agent 改代码
→ 文件保存 → Hook 又自动跑测试
→ 测试通过
→ Hook 通知你 "全部通过 ✅"
```

---

## Claude Code 的 Hook 体系

Hook 在 `settings.json` 里配置，支持的事件：

### 事件类型

| 事件 | 触发时机 | 典型用途 |
|------|----------|----------|
| `PreToolUse` | 工具**调用前** | 拦截危险操作 |
| `PostToolUse` | 工具**执行后** | 记录操作日志 |
| `Notification` | 各种通知 | 转发到手机/企业微信 |
| `Stop` | Agent 完成一轮回复 | 自动执行下一步 |
| `SessionStart` | 会话开始 | 加载项目上下文 |
| `UserPromptSubmit` | 用户提交消息 | 自动补充信息 |

---

## 实际例子

### 例子 1：拦截 rm -rf

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "command": "echo 'COMMAND' | grep -q 'rm -rf' && echo 'BLOCKED: rm -rf' && exit 1 || exit 0"
      }
    ]
  }
}
```

当 Agent 想执行 Bash 工具时，如果命令里有 `rm -rf`，Hook 直接拦截。

### 例子 2：自动记录所有文件修改

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "echo \"$(date): Modified $(echo '$TOOL_INPUT' | jq -r '.file_path')\" >> ~/.claude/logs/file-changes.log"
      }
    ]
  }
}
```

每次 Agent 修改文件后，自动记录到日志。

### 例子 3：切换项目时自动加载 Memory

```json
{
  "hooks": {
    "SessionStart": [
      {
        "command": "cat ~/.claude/projects/$(basename $PWD)/memory/MEMORY.md 2>/dev/null || true"
      }
    ]
  }
}
```

进入项目目录时自动加载项目记忆。

---

## Hook 的工作原理

```
事件发生（PreToolUse / PostToolUse / ...）
    ↓
匹配规则（matcher：这个事件是不是我们要处理的）
    ↓
执行命令（command：bash 脚本或程序）
    ↓
读取输出（stdout）
    ↓
决定行为
    ├── PreToolUse：输出决定是否拦截（exit 1 = 拦截）
    ├── PostToolUse：输出注入到上下文
    ├── Notification：输出作为通知内容
    └── Stop：输出作为新 prompt 自动执行
```

---

## Hook 的变量

Hook 命令里可以用环境变量获取上下文：

| 变量 | 含义 |
|------|------|
| `$TOOL_NAME` | 正在调用的工具名 |
| `$TOOL_INPUT` | 工具的输入参数（JSON） |
| `$PWD` | 当前工作目录 |
| `$SESSION_ID` | 当前会话 ID |

---

## Hook vs Skill vs MCP

| | Hook | Skill | MCP |
|---|---|---|---|
| 谁触发 | 事件自动触发 | 你手动 `/command` | Agent 需要时调用 |
| 时机 | 被动（事件驱动） | 主动（你发命令） | 主动（Agent 决定） |
| 本质 | bash 脚本 | 一段 prompt | 独立程序 |
| 典型场景 | 安全拦截、日志、通知 | 审查、检查、部署流程 | 浏览器、数据库、外部 API |

---

## Hook 的注意事项

1. **Hook 是在本地执行的 shell 命令**，不在 Agent 推理中，不影响 token 消耗
2. **Hook 执行失败不会导致 Agent 崩溃**，只记录日志
3. **不要用 Hook 做太重的事**——每次保存文件都跑耗时 30 秒的脚本 = 灾难
4. **Hook 的 stdout 可能被注入到上下文**，注意不要泄露敏感信息

---

## 在你的工具里

| 工具 | Hook 支持 |
|------|-----------|
| Claude Code | ✅ 完整 Hook 系统（settings.json） |
| Trae | ❌ 没有公开的 Hook API |
| ZCode | ❌ 不支持 |

**Hook 是 Claude Code 的高级特性。** 暂时你可能不需要自定义 Hook，但要知道它存在——当你有一天觉得"每次都要手动做 X 好烦"，就想到 Hook。

---

## 自检清单

- [ ] 能解释 Hook 的本质（事件驱动自动化）
- [ ] 知道至少 4 种 Claude Code 的 Hook 事件类型
- [ ] 能写一个简单的 Hook 配置（拦截危险命令）
- [ ] 能区分 Hook vs Skill vs MCP
- [ ] 理解 Hook 是 shell 脚本执行，不消耗 token
