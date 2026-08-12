# 3.1 任务拆解（Prompt Engineering 的精髓）

## 核心定律

> **Agent 的输出质量 = 你输入的质量 × 模型的推理能力**

模型再强，你给烂 prompt，它产出烂结果。Prompt Engineering 不是魔法，而是**把模糊需求翻译成模型能精确执行的指令**。

---

## 为什么"帮我写个网站"是烂 prompt

```
你：帮我写个网站
Agent：好的，什么类型的网站？
你：就是那种，有登录，能发帖子的
Agent：好的（开始写一个论坛）
你：不对不对，我要的是像微博那样的
Agent：好的（开始重写）
你：也不是微博，就是一个简单的留言板
...（10 轮后终于说清楚，但上下文已经满了）
```

问题不在于 Agent 弱，在于你没有告诉它：
1. 这个网站是干什么的（功能）
2. 谁会用（用户）
3. 有什么约束（技术栈、风格、规模）

---

## 好 Prompt 的 4 要素

### 1. 角色定义（Role）
> 你是一个 Python 后端开发者，擅长 FastAPI 和 Postgres。

告诉 Agent **它应该是谁**。不同角色会产出不同质量的代码。

### 2. 任务描述（Task）
> 写一个用户注册接口，接受用户名、邮箱、密码，返回 JWT token。

具体、可验证。不要"做一个用户系统"，要说"写一个注册接口"。

### 3. 约束条件（Constraints）
> - 密码至少 8 位，包含大小写字母和数字
> - 邮箱格式要验证
> - 用 bcrypt 做密码哈希
> - 返回的 token 有效期 7 天
> - 错误信息用中文

这是 Agent 产出的"验收标准"。

### 4. 上下文（Context）
> 项目结构在 src/api/ 下，User model 已经在 src/models/user.py 定义好了，看那个文件。

让 Agent 不需要猜。它直接读文件，产出就更准确。

---

## Plan-then-Execute 模式

你不会让一个工人不看图纸就盖房子。同样，复杂任务应该让 Agent **先规划再执行**。

### 错误方式
```
你：帮我重构整个用户模块，把 SQLAlchemy 换成 Prisma
Agent：（直接开始改代码，改到一半发现依赖关系理不清，开始胡改）
```

### 正确方式
```
你：帮我重构整个用户模块，把 SQLAlchemy 换成 Prisma。
    第一步：先分析现有 User 模块的所有文件，列出依赖关系
    第二步：给我一个迁移计划，我确认后再动手

Agent：
  分析结果：
  - src/models/user.py → 被 5 个文件引用
  - src/api/auth.py → 依赖 User model
  - src/services/user_service.py → 依赖 User model
  - ...
  
  迁移计划：
  1. 先装 prisma-client
  2. 创建 schema.prisma
  3. 改写 user.py
  4. 逐个更新 5 个引用文件
  5. 删除旧的 SQLAlchemy 依赖
  
  确认后开始？
```

**你现在确认一下，就能避免 Agent 跑偏。**

---

## 拆解公式

把大任务拆成 Agent 能一口吃下的子任务：

```
"重构用户模块"
    ↓ 拆
1. 分析现有用户模块结构（只读）
2. 新 ORM schema 设计（让 Agent 提案，你确认）
3. 实现新 model 层
4. 迁移 API 层
5. 迁移 Service 层
6. 更新测试
7. 删除旧代码
```

**每个子任务都是 Agent 能在一个会话内完成的量。**

---

## 给 Agent 提供上下文的最佳方式

### 优先级从高到低

1. **直接给它文件路径** — "读 src/models/user.py 的第 30-80 行"
2. **引用代码** — "参考 src/api/auth.py 里的 create_token 函数"
3. **粘贴关键代码** — 只说 10 行不到的，直接贴
4. **描述现有逻辑** — "我们的 User model 有 name, email, password_hash, role 四个字段"

### 不要做的事
- ❌ "你猜" — Agent 会猜错，然后你得花更多轮纠错
- ❌ 把整个项目粘贴给它 — 你的上下文立刻炸了
- ❌ 用"和上次一样"这种表述 — Agent 可能已经不记得"上次"了

---

## 实操：从模糊需求到可执行 prompt

### 输入（模糊）
> 帮我给赶酒项目加个搜索功能

### 输出（可执行）
> **角色**：你是 Vue 3 前端开发者，熟悉 Element Plus 组件库
>
> **任务**：在赶酒项目的首页（F:\baidakechaung\ganjiu\src\views\Home.vue）加一个搜索栏
>
> **约束**：
> - 搜索栏放在页面顶部，导航栏下方
> - 样式参考现有的 Element Plus 输入框风格
> - 输入关键词后按回车触发搜索，搜索结果用卡片列表展示
> - 搜索时显示 loading 状态，搜索失败显示错误提示
> - 空结果时显示"未找到相关内容"
>
> **上下文**：
> - 搜索接口是 GET /api/search?q=关键词，返回 { results: [...] }
> - 接口可能需要带 token（参考 src/utils/request.ts 的封装）
> - 现有卡片组件在 src/components/Card.vue

---

## 在 Claude Code 里的实际操作

Claude Code 有个特性：你在 prompt 里写的**文件路径会被自动识别**，Agent 会先读那些文件再回答。所以：

```
帮你写个 patch？❌ 太模糊

帮我改 src/utils/auth.ts 第 45 行的 JWT 过期时间从 1h 改成 7d ✅
精确、可执行、Agent 不会改错
```

---

## 自检清单

- [ ] 能识别一个 bad prompt 的 3 种以上问题
- [ ] 能用"角色 + 任务 + 约束 + 上下文"公式重写 prompt
- [ ] 理解 Plan-then-Execute 模式及其价值
- [ ] 能把一个大任务拆成 Agent 可执行的子任务
- [ ] 知道给 Agent 提供上下文的最佳方式（优先级排序）
