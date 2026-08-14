# 4.4 Agent 产生幻觉的常见场景

## 什么是幻觉

**幻觉 = Agent 输出了看起来合理但实际错误的信息。**

它不是在故意骗你——它只是在做概率预测。"下一个最可能的词"有时候恰好不是对的。

---

## 幻觉类型 1：编造不存在的 API

```
你：帮我写一个 Python 函数，调用 OpenAI 的 vision API

Agent：
  from openai import OpenAI
  client = OpenAI()
  response = client.vision.analyze(    ← 不存在！OpenAI 没有 client.vision
      model="gpt-4-vision",
      image=image_data
  )
```

模型知道"OpenAI 有图像分析能力"，但不知道具体 API 叫什么，于是"猜"了一个看起来合理的名字。

### 怎么识别
- 你没见过的第三方库函数名 → 先查文档
- Agent 引用了你没用过的方法 → 让它附上文档链接
- 运行代码立即报 `AttributeError` / `ModuleNotFoundError`

---

## 幻觉类型 2：拼接真实 + 虚假信息

```
你：Python 的 asyncio 怎么用？

Agent：
  asyncio 是 Python 的异步库。你可以这样用：
  
  import asyncio
  
  async def main():
      result = await asyncio.gather(     ← 正确，真实存在
          fetch_data(),
          asyncio.run_in_executor(       ← 正确，真实存在
              compute_heavy()
          )
      )
      return asyncio.to_thread(process)  ← 不存在！没有这个函数
```

**真假混杂最难识别。** 你看到前两个是对的，就默认第三个也是对的。

### 怎么识别
- 每个不熟悉的 API 都单独验证（翻文档 or 跑一下）
- 如果 Agent 连续写了 5 个你不知道的 API，至少 1 个是假的
- Python：`help(function_name)` 或 `dir(module)` 快速验证

---

## 幻觉类型 3：自信地给出错误答案

```
你：React 19 有哪些新特性？

Agent：（React 18 还是最新版时）
  React 19 引入了：
  1. Server Components 原生支持     ← 正确
  2. useOptimistic hook            ← 正确
  3. 新的 useServerAction hook      ← 不存在！
  4. 内置的 AI 推理引擎            ← 完全编造
```

Agent 用自信的语气说了 4 点，2 个对 2 个假。如果你不熟悉 React 19，你全盘接受。

### 为什么这么危险
- 人的认知偏差：自信 ≈ 正确
- 但模型的自信度和正确性**没有相关性**
- 模型对自己错误的输出同样"自信"

### 怎么识别
- 对任何"你不知道"的事实保持怀疑
- "听起来太好的新特性"很可能是编的
- 查官方文档或 changelog 验证

---

## 幻觉类型 4：上下文误导

```
你（在讨论 Python 项目）：帮我写一个 User 类

Agent：
  class User:
      def __init__(self):
          self.name = ""
          this.email = ""     ← 突然变成了 JavaScript 语法！
```

Agent 在长上下文中可能混淆不同语言/框架的语法。

### 怎么识别
- 语法高亮能直接暴露（编辑器中打开看颜色异常）
- 运行时报错
- 混合风格的代码 → 警惕

---

## 为什么会有幻觉

```
幻觉 ≠ bug，是模型的基本属性。

模型的工作原理：
1. 看你的输入
2. 在自己的知识空间里找"最可能跟在后面的词"
3. 逐词生成回复

它没有"事实核查"机制。
它不知道"我不知道"。
它对"真实"和"听起来真实"没有区分能力。
```

---

## 验证 Agent 输出的方法

### 1. 运行验证（最可靠）
```bash
python the_code_agent_wrote.py
```
→ 跑不起来 = 有问题。跑起来了 ≠ 没问题（还要看逻辑）。

### 2. 文档验证
任何一个 Agent 提到的 API，如果你不熟悉，搜一下文档。30 秒的搜索比你信了错误的代码再花 30 分钟 debug 划算。

### 3. 逻辑审查
```
Agent 的逻辑：先查用户，再查订单，再关联两者
你问自己：这个流程合理吗？有没有漏掉什么？
→ 如果漏了，告诉 Agent 补充
```

### 4. 交叉验证
```
用 Agent 1 写代码 → 用 Agent 2（新会话）审查 Agent 1 的代码
→ 独立 Agent 不受 Agent 1 的上下文影响
```

### 5. 怀疑模式
```
当 Agent 输出以下内容时，提高警惕：
  - 你完全不熟悉的 API/库/框架
  - 听起来"太完美"的解决方案
  - 引用了版本号或具体数字
  - 混合了多种语言的语法
```

---

## 自检清单

- [ ] 能说出 4 种幻觉类型及其特征
- [ ] 理解幻觉的本质（概率预测，非事实核查）
- [ ] 掌握至少 3 种验证 Agent 输出的方法
- [ ] 知道"真假混杂"为什么是最危险的幻觉类型
- [ ] 有"怀疑模式"的条件反射
