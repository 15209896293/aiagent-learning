# 2.4 Skills（技能/预设工具链）

## 一句话

**Skill = 一段预写的 prompt + 工具编排，打包成一个"命令"。**

你敲 `/code-review`，背后不是一句简单的话——而是一套完整的流程被展开执行。

---

## Skill 和普通 Prompt 的区别

### 普通 Prompt
```
你："帮我审查这段代码"
Agent：看看代码，随便说几句 → 结果不固定
```

### Skill（`/code-review`）
```
你：/code-review
Agent：
  1. 加载预定义的审查维度和标准
  2. 按"正确性 bug + 简化/复用/效率"两个维度分别检查
  3. 每个发现带文件名+行号
  4. 按严重程度排序
  5. 输出结构化报告
  → 结果一致、全面、可操作
```

**Skill = 把"怎么说"这件事标准化了，你不用每次自己组织 prompt。**

---

## Claude Code 的内置 Skills

| Skill | 做什么 |
|-------|--------|
| `/code-review` | 代码审查（正确性 + 简洁性） |
| `/simplify` | 代码简化（不改逻辑，只清理） |
| `/verify` | 验证代码改动是否正确 |
| `/init` | 为新项目创建 CLAUDE.md |
| `/run` | 启动项目并验证改动 |
| `/review` | 审查 PR |
| `/security-review` | 安全审查 |
| `/deep-research` | 深度调研（搜索+验证+报告） |
| `/loop` | 定时循环执行某个操作 |

---

## Skill 内部长什么样

以 `/code-review` 为例，它的内部结构大致是：

```markdown
## 身份
你是一个代码审查者。只关注正确性和简化，不关注风格。

## 审查维度
1. 正确性 Bug：逻辑错误、空指针、边界条件、竞态
2. 简化/复用：重复代码、不必要的抽象、可删除的死代码

## 输出格式
每个发现：
- [严重程度] 文件名:行号 — 问题描述
- 建议修改：
- 不确定度（高/中/低）

## 行为规则
- 不确定的发现标注不确定度
- 只报你确信的，不凑数
- 忽略格式化、命名问题
```

当你输入 `/code-review` 时，这个 prompt 被注入到当前对话，Agent 严格按照这个框架执行。

---

## 怎么创建自己的 Skill

### Claude Code 的方式

Skill 就是 `~/.claude/skills/` 目录下的一个 `.md` 文件。

```
~/.claude/skills/
├── my-code-review.md
├── deploy-check.md
└── daily-standup.md
```

文件名就是 Skill 名（`/my-code-review`、`/deploy-check`）。

### Skill 文件结构

```markdown
---
name: deploy-check
description: 部署前检查清单：测试是否通过、环境变量是否完整、是否有未提交的改动
---

# 部署前检查

执行以下步骤：

1. 运行 `git status`，检查是否有未提交的改动
2. 运行 `npm test`（或项目对应的测试命令）
3. 检查 `.env.example` 和 `.env` 的差异，确保新增变量已配置
4. 检查是否有 TODO/FIXME/HACK 注释未处理
5. 输出检查报告：每个项目 ✅/❌，有问题的地方给修复建议

只有当所有检查通过时才说"可以部署"。
```

然后你随时可以用 `/deploy-check`。

---

## Skill vs MCP 怎么区分

很多人搞混：

| | Skill | MCP |
|---|---|---|
| 本质 | 一段文本（prompt） | 一个独立程序（Server） |
| 能做什么 | 指导 Agent 怎么做 | 给 Agent 新的能力 |
| 举例 | "按这个框架审查代码" | "控制浏览器" |
| 运行在哪 | Agent 的推理过程里 | 独立进程 |
| 安装 | 写一个 `.md` 文件 | 装一个 npm/pip 包 |

**Skill 教 Agent "怎么想"，MCP 给 Agent "怎么做"。**

---

## 什么场景适合写 Skill

| 场景 | 为什么写 Skill |
|------|----------------|
| 每次部署前都要做同样的检查 | 不用每次打字，一键 `/deploy-check` |
| 你的项目有特殊的代码规范 | 写 `/lint-check` 嵌入你的规则 |
| 重复性任务：写周报、总结 PR | 固定格式，Agent 填充内容 |
| 新成员上手项目 | 写 `/onboard` 自动生成项目介绍 |

**规则：如果你把同样的 prompt 复制粘贴了 3 次以上，就该写个 Skill。**

---

## 在你的工具里

| 工具 | Skill 支持 |
|------|------------|
| Claude Code | ✅ 完整的 Skill 系统（`/` 命令 + 自定义 skill 文件） |
| Trae | ❌ 没有 Skill 概念，但有自定义指令 |
| ZCode | ❌ 类似 Trae |

---

## 自检清单

- [ ] 能说出 Skill 和普通 prompt 的核心区别
- [ ] 知道至少 5 个 Claude Code 内置 Skill
- [ ] 能写一个自己的 Skill 文件
- [ ] 能区分 Skill vs MCP（本质 + 适用场景）
- [ ] 知道什么情况下应该写一个 Skill
