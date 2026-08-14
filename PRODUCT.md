# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

静态 HTML + 内联 CSS/JS（无框架、无构建步骤）。根级共享 `style.css` 即将引入，三块子站以相对路径 `../style.css` 引用。

## Users

- 有编程基础（能写 Python）、但不知道怎么用 Agent 干活的开发者。
- 用 Claude Code / Trae / ZCode 但说不清其工作机制的学习者。
- 需要判断"什么时候用 Agent、什么时候不用"的从业者。

## Product Purpose

把 AI Agent 从"科普"变成"可上手的实战手册"：让有编程基础的人读完后能用 Agent 真正干活。全站分三块内容：
- **术语图鉴**（根 `index.html`）：Vibe Coding / AI Agent 术语查询与概念卡片，带搜索与明暗主题。
- **课程站**（`courses/`，13 页）：按模块顺序的实战课程，每篇配自检清单。
- **软件站**（`software/`）：AI 相关工具软件的分类下载索引。

## Positioning

不是泛泛科普，而是"每篇读完后能回答末尾自检清单"的实战手册。每个概念都在 Claude Code / Trae / ZCode 三个工具里标注体现，让学习者知道同样的能力在不同工具里怎么用。

## Operating Context

- 用户按模块顺序阅读，每篇 15–30 分钟。
- 三块内容共用同一个学习者的心智模型，需要一致的视觉与导航体验。
- `demos/` 目录提供可运行的 Python 脚本。
- 课程站当前是孤儿站（与主站/软件站零互链），需打通导航闭环。

## Capabilities and Constraints

- 纯静态 HTML，无框架、无构建、无外部资源依赖，需保持可离线双击打开。
- 主站已有明暗双主题（`data-theme` + 设计令牌），课程站与软件站需接入同一视觉世界。
- 课程站当前无移动端断点、无明暗主题，是三块中最需补齐的。
- `software-downloads/` 下的 `.md` 下载清单不属前端界面，本次不改动。

## Brand Commitments

- 对外展示/教学站，注重品牌一致性。
- 品牌主色以主站 `--brand:#3559d8` 为基底（对外展示用）。
- 语言为简体中文，网站名以现有标题为准（VibeHub · Vibe Coding 术语图鉴 等）。

## Evidence on Hand

- `README.md`：定位、模块地图、目标读者（已确认采用知识图鉴站定位）。
- `index.html`（根，307KB）：术语图鉴，成熟视觉（主站设计令牌 + 明暗主题）。
- `software/index.html`（33KB）：软件站，复用主站令牌 + 左侧分类侧边栏。
- `courses/index.html` + `courses/lesson-1…11`：课程站，独立的深蓝黑 Slate 暗色风格，13 页。
- 无真实用户数据、无定价、无部署目标（本地/静态托管待定）。

## Product Principles

1. **三块内容是一个产品**——统一的视觉系统与导航闭环，不因目录划分而割裂。
2. **知识可自查**——每篇以自检清单收尾，读者能验证自己的理解。
3. **实战优先**——概念在三个真实工具中标注体现，而非空谈。
4. **可离线可用**——纯静态、无构建、无外部依赖，双击即可打开。
5. **默认可访问**——明暗主题、移动端断点、对比度是底线，不是加分项。

## Accessibility & Inclusion

- 对外教学站，需保证明暗双主题下的文字对比度（正文 ≥4.5:1）。
- 需补齐移动端（课程站当前无断点）。
- 键盘可达、可聚焦为默认要求。
