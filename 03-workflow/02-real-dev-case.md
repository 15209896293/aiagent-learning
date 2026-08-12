# 3.2 驱动 Agent 完成真实开发任务

## 三个完整案例，从头到尾

每个案例都遵循同一流程：
```
需求分析 → 任务拆解 → Agent 执行 → 验证 → 修改 → 完成
```

---

## 案例 1：从零搭建一个数据看板页面

### 需求
> 做一个数据看板，展示用户增长、活跃度、收入三个指标的趋势图

### Step 1：需求分析（你做的）

先问自己 3 个问题：
- 数据从哪来？（API 接口、静态 JSON、数据库？）
- 技术栈是什么？（React/Vue/Vanilla？图表库？）
- 谁看？（技术团队 or 老板？→ 决定精度和样式）

假设答案：API 接口、React + ECharts、给老板看。

### Step 2：任务拆解

```
1. 创建 Dashboard 组件骨架
2. 写 API 调用逻辑（三个接口）
3. 集成 ECharts 画折线图
4. 加日期选择器和自动刷新
5. 加 loading/error/empty 状态处理
```

### Step 3：Agent 执行

```
你（第 1 轮）：
你是 React 开发者，用 ECharts 做数据可视化。
任务：创建 Dashboard 组件，展示三个指标的趋势图。
数据来源：
- GET /api/stats/users?range=7d → { dates: [], values: [] }
- GET /api/stats/activity?range=7d
- GET /api/stats/revenue?range=7d

先读 src/api/ 了解现有请求封装方式，再写代码。
在 src/pages/Dashboard.tsx 创建组件。

Agent：（读 api 文件）→（写 Dashboard 组件）

你（第 2 轮）：
试跑有报错吗？如果有，修一下。

Agent：（跑 npm run dev）→ 有报错 →（修）

你（第 3 轮）：
加上日期范围选择器（最近 7 天/30 天/90 天），放在图表上方，用 Ant Design 的 DatePicker.RangePicker。

Agent：（装 antd 依赖）→（加选择器）→（联动 API 请求）

你（第 4 轮）：
加上这三个状态：
- 加载中：图表位置显示 Spin 加载动画
- 请求失败：显示 Alert 错误提示 + 重试按钮
- 数据为空：显示 Empty 组件

Agent：（加三种状态的处理）
```

### Step 4：验证

```
你：跑一下，截图给我看

Agent：（跑浏览器 → 截图）
→ 确保三个图表都渲染了
→ 确保日期选择器切换后数据刷新
→ 确保 loading/error/empty 三种状态都能正确显示
```

---

## 案例 2：分析数据并生成报告

### 需求
> 用户调研报告里有一堆问卷数据（CSV），分析用户痛点分布并生成图表

### Step 1：需求分析

CSV 在哪？什么格式？输出什么格式？

### Step 2-3：执行

```
你（第 1 轮）：
你是一个数据分析师。读取 F:\baidakechaung\用户调研报告.docx，提取里面的问卷数据。
如果有 CSV 导出文件，直接读 CSV。分析以下维度：
1. 用户痛点出现频率（Top 10）
2. 不同年龄段用户的痛点差异
3. 用户满意度平均分

Agent：（读文件 → 提取数据 → 清洗 → 分析）

你（第 2 轮）：
用 matplotlib 画三张图：
1. 痛点频率柱状图（Top 10）
2. 年龄段 vs 满意度箱线图
3. 痛点词云

存到 charts/ 目录，然后生成一份 summary.md 总结关键发现。

Agent：（装 matplotlib）→（画图）→（写总结）
```

---

## 案例 3：调试一段你不熟悉的代码

### 需求
> 用户登录功能偶尔 500 报错，你看不懂后端代码

### Step 1：让 Agent 先理解

```
你：我不熟悉这个项目的后端。帮我理解 src/api/auth.py 里的登录逻辑。
    用中文解释流程，标注每个步骤涉及的函数和文件。

Agent：
  登录流程：
  1. 接收 POST /api/login → src/api/auth.py:login()
  2. 验证用户名密码 → src/services/auth_service.py:verify_user()
  3. 查数据库 → src/models/user.py:User.query.filter_by()
  4. 生成 JWT → src/utils/token.py:create_token()
  5. 返回 token 给前端
  
  可能的 500 错误点：
  - 数据库连接断开（verify_user 里没有 try-catch）
  - JWT 秘钥未配置（token.py 从环境变量读 SECRET_KEY）
  - 用户不存在时没返回 401，而是抛异常
```

### Step 2：让 Agent 定位问题

```
你：看看可能出错的地方，加日志。然后在本地跑测试，看能不能重现 500。

Agent：（加日志 → 跑测试 → 分析输出）
→ "500 是因为 SECRET_KEY 环境变量在测试环境没设置，token.py 抛了 KeyError"
```

### Step 3：修 + 防

```
你：修这个问题。另外，给 token.py 加上默认值和明显的错误提示，
    下次再有人遇到这个坑能 3 秒定位。

Agent：（加 try-catch + 清晰的错误消息）→（更新文档）
```

---

## 驱动 Agent 的通用规则

### 每轮只做一件事
> "写组件" ✅
> "写组件 + 写测试 + 写文档 + 重构旧代码" ❌

一轮给太多任务 → Agent 会遗漏 → 你花更多轮纠错。

### 从"只读"开始
> 先让它读代码、分析结构、出方案 → 你确认 → 再动手改。

这比直接改错了再回滚效率高得多。

### 每改一步就验证
> "改了 auth.py，跑一下相关测试看看"

不要等改完 5 个文件再一次性验证——出错了你不知道哪个文件改坏的。

### 给 Agent 反馈要具体
> "第 45 行的过期时间改成 7d" ✅
> "不太对，再改改" ❌

具体反馈让 Agent 在下一轮就修正。模糊反馈 = 浪费 3 轮。

---

## 自检清单

- [ ] 能按"需求分析 → 拆解 → 执行 → 验证"流程驱动 Agent
- [ ] 会使用 Plan-then-Execute（先让 Agent 分析，确认后再动手）
- [ ] 掌握"每轮只做一件事 + 从只读开始 + 每步验证 + 具体反馈"四规则
- [ ] 知道调试不熟悉代码的策略（先理解 → 再定位 → 修 + 防）
