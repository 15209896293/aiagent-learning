---
name: VibeHub · AI Agent 实战指南
description: 卡片式知识图鉴站，统一三块内容（术语图鉴 / 课程 / 软件库）的视觉世界。
colors:
  primary: "#3562e6"
  primary-deep: "#2a47b0"
  primary-light: "color-mix(in srgb, #3562e6 9%, #ffffff)"
  bg: "#ffffff"
  bg-soft: "#fafafa"
  bg-demo: "#f5f5f7"
  text: "#18181b"
  text-2: "#52525b"
  text-3: "#8a8a93"
  border: "#e4e4e7"
  border-light: "#f0f0f2"
  border-hover: "#d4d4d8"
typography:
  display:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"PingFang SC\", \"Helvetica Neue\", \"Microsoft YaHei\", sans-serif"
    fontSize: "clamp(1.6rem, 3.5vw, 2.4rem)"
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "-0.02em"
  body:
    fontFamily: "-apple-system, BlinkMacSystemFont, \"PingFang SC\", \"Helvetica Neue\", \"Microsoft YaHei\", sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.7
  label:
    fontFamily: "inherit"
    fontSize: "12px"
    fontWeight: 500
    lineHeight: 1
rounded:
  sm: "8px"
  md: "12px"
  lg: "16px"
spacing:
  xs: "8px"
  sm: "14px"
  md: "24px"
  lg: "32px"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#ffffff"
    rounded: "{rounded.md}"
    padding: "9px 16px"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.text-2}"
    rounded: "{rounded.md}"
    padding: "9px 14px"
    border: "1px solid {colors.border}"
  card:
    backgroundColor: "{colors.bg}"
    textColor: "{colors.text}"
    rounded: "{rounded.md}"
    padding: "20px"
    border: "1px solid {colors.border-light}"
  search-input:
    backgroundColor: "{colors.bg-soft}"
    textColor: "{colors.text}"
    rounded: "9px"
    padding: "6px 11px"
    border: "1px solid {colors.border}"
---

# Design System: VibeHub · AI Agent 实战指南

## Overview

**Creative North Star: "The Card Catalog（卡片图鉴）"**

VibeHub 是一本会呼吸的卡片图鉴。全站由整齐、可检索的卡片构成——术语卡片、课程卡片、软件卡片——它们共用同一套骨架与节奏，让读者在三块内容之间无缝漫游，像翻阅一本装帧精良的图鉴。这套系统以主站术语图鉴的既有视觉为基底，将原本割裂的三套皮肤收敛为一套：同一个品牌色、同一套圆角与阴影、同一组字体层级，从"孤儿课程站"到"软件下载库"都发出同一种声音。

设计取向是**精致克制（refined and restrained）**：以清晰的层级与充足留白承载信息，而非用装饰堆砌存在感。卡片是主角，它们安静、稳定、可预期；品牌蓝只在需要强调处出现（术语英文名、课程"下一课"、软件下载主按钮），点缀而非喧哗。整个系统服务一个学习者的心智：先找到卡片，再读懂它，然后继续翻页。

**Key Characteristics:**
- 卡片即结构：术语、课程、软件统一以卡片为最小单位，圆角 12px，一次明确的动作。
- 品牌蓝克制使用：Electric Blue 只作强调色，不铺满。
- 明暗双主题一等公民：暗色下所有表面、边框、文字同步切换，不落下一个角落。
- 中文优先的中性排版：正文 15px/1.7，正文行宽 65–75ch，让长文可读。
- 导航闭环：术语图鉴 / 课程 / 软件库三块互相可达，同一套顶栏语言。

## Colors

主色取 Electric Blue（电光蓝），从主站深湛蓝微调而来，更现代的色相；中性色沿用主站的暖灰阶，暗色主题以同族深灰取代。

### Primary
- **Electric Blue** (`#3562e6`): 品牌主色。用于主按钮、活跃导航、术语英文名、链接高亮、重点强调。作为强调色，单屏占比控制在 ≤10%。
- **Deep Indigo** (`#2a47b0`): Electric Blue 的加深态。用于主按钮 hover、焦点环。
- **Blue Halo** (`color-mix(in srgb, #3562e6 9%, #ffffff)` / 暗色下 `14%`): 极淡的品牌底色，用于导航 hover 背景、聚焦光晕、选中态。

### Neutral
- **Paper** (`#ffffff` / 暗色 `#0a0a0c`): 页面背景，卡片表面。
- **Soft Paper** (`#fafafa` / `#101013`): 次级表面，搜索框、侧边栏、hover 的温和底色。
- **Demo Stage** (`#f5f5f7` / `#151518`): 代码演示/示例块的容器底。
- **Ink** (`#18181b` / `#f4f4f5`): 正文文字。
- **Ink Soft** (`#52525b` / `#a1a1aa`): 次级文字、描述。
- **Ink Faint** (`#8a8a93` / `#6b6b73`): 占位符、辅助标签、角标。
- **Hairline** (`#e4e4e7` / `#26262b`): 主边框。
- **Hairline Soft** (`#f0f0f2` / `#1c1c20`): 卡片分隔、浅边框。

### Named Rules
**The Rarity Rule.** Electric Blue 是稀缺资源，单屏强调占比 ≤10%。它的稀有度就是它的力量——当一个元素被标蓝，读者知道这是关键。
**The Warm Gray Rule.** 中性色从不取纯灰，而是带暖相的灰阶，让白色底更柔和、暗色底更有层次。

## Typography

**Display/Headline Font:** -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", "Microsoft YaHei", sans-serif
**Body Font:** 同上（系统字体栈，中文优先）
**Label/Mono Font:** "SF Mono", "JetBrains Mono", "Cascadia Code", Consolas, monospace（仅代码/数据）

**Character:** 系统字体 + 中文优先，保证任何环境都清晰可读；层级靠字重与字号拉开，不用渐变或花哨字体博眼球。

### Hierarchy
- **Display** (700, clamp(1.6rem,3.5vw,2.4rem), 1.25, -0.02em): 页面主标题、hero 标题。仅用于页面级标题。
- **Headline** (650, 1.25rem, 1.4): 区块标题、卡片标题。
- **Title** (620, 16px, 1.4): 卡片内标题（术语名、课程名、软件名）。
- **Body** (400, 15px, 1.7): 正文、描述。行宽控制在 65–75ch。
- **Label** (500, 12px, 1, normal): 辅助标签、面包屑、状态角标、输入占位符。

### Named Rules
**The Weight Rule.** 层级一律靠字重与字号表达，不用渐变文字、不用下划线装饰。

## Layout

- **内容容器**: 最大宽度 `--maxw:880px`（软件站放宽至 1080px 容纳侧边栏），居中，水平内边距 24px（窄屏 16px）。
- **卡片网格**: 术语卡片桌面两列、窄屏单列（`@media(max-width:720px)`）；软件站为 顶栏 + 左侧 sticky 侧边栏 + 卡片网格。
- **间距节奏**: 紧凑分组（xs 8px 内聚）、疏朗分块（md 24px / lg 32px 分隔）。标题上方的间距大于标题下方的间距。
- **响应式断点**: 760px 以下隐藏导航菜单项（移动端收纳）、侧边栏变横向滚动条、搜索框收窄。

## Elevation & Depth

系统以**柔和分层**而非硬阴影传达深度。静态卡片近乎平铺，靠 1px 浅边框分隔；交互（hover）时才浮现柔和阴影与轻微上浮。暗色主题下阴影加深以在深底上保层次。

### Shadow Vocabulary
- **Card Rest** (`0 1px 2px rgba(0,0,0,.04), 0 4px 14px rgba(0,0,0,.05)`; 暗色 `0 1px 2px rgba(0,0,0,.4), 0 6px 18px rgba(0,0,0,.35)`): 卡片默认——极轻，几乎感知不到。
- **Card Float** (hover: 同 card-rest 上浮 `translateY(-3px)`): 交互态浮现。
- **Floating** (`0 8px 30px rgba(0,0,0,.12)`; 暗色 `0 12px 40px rgba(0,0,0,.6)`): 浮层、弹窗、下拉。

### Named Rules
**The Flat-by-Default Rule.** 表面静止时是平的，只以边框勾勒；阴影是状态的响应（hover / 浮层），不是日常装饰。

## Shapes

- **表单语言**: 圆角，统一以 8–16px 阶梯呈现。卡片 12px、按钮 9–12px、输入 9px、标记 7px。
- **边框**: 1px 细边框（Hairline），hover 加深为 Hairline Hover；聚焦用 3px 品牌淡光晕（`box-shadow:0 0 0 3px var(--brand-light)`）而非粗边框。

## Components

### Buttons
- **Shape:** 圆角 9–12px，无硬阴影。
- **Primary:** Electric Blue 底 + 白字（`9px 16px`），hover 变 Deep Indigo。
- **Ghost:** 透明底 + Ink Soft 字 + 1px Hairline 边框，hover 边框加深。
- **Hover / Focus:** 0.15s 过渡；focus-visible 显示 3px Blue Halo 焦点环。

### Cards / Containers
- **Corner Style:** 圆角 12px。
- **Background:** Paper（暗色同族深灰）。
- **Shadow Strategy:** 参考 Elevation——静止近平，hover 上浮浮现柔和阴影。
- **Border:** 1px Hairline Soft，hover 加深。
- **Internal Padding:** 20px（卡片内距节奏）。
- 卡片头：中文名（Title 级）+ 英文名（Electric Blue 标注）+ 可交互星标（右侧，hover 转琥珀 #f5a623）。

### Inputs / Fields
- **Style:** Soft Paper 底 + 1px Hairline 边框，圆角 9px。
- **Focus:** 边框转品牌蓝 + 3px Blue Halo 光晕（`box-shadow:0 0 0 3px var(--brand-light)`）。
- **Placeholder:** Ink Faint。

### Navigation
- **Style:** sticky 顶栏，毛玻璃 `backdrop-filter`，白底 86% 透明度 + 1px 底部浅边框。
- **Typography:** 导航项 14px Ink Soft；活跃项 Electric Blue + 600 字重；hover 淡蓝底。
- **Mobile:** ≤760px 隐藏菜单项，保留 logo / 搜索 / 主题切换图标按钮。

### Chips / Tags
- **Style:** 12px Ink Faint 标签字，或品牌淡底 + 品牌字（如键盘快捷键芯片 `.key-chip`），圆角 7px。

## Do's and Don'ts

### Do:
- **Do** 用卡片承载术语、课程、软件内容，圆角 12px + 1px 浅边框。
- **Do** 让品牌蓝做强调而非铺陈，单屏 ≤10%。
- **Do** 用字重与字号表达层级，正文行宽 65–75ch。
- **Do** 让明暗主题覆盖所有表面，暗色下用同族深灰 + 加深阴影。
- **Do** 保持三块导航闭环（术语图鉴 / 课程 / 软件库互通）。

### Don't:
- **Don't** 用渐变文字或 emoji 充当图标——图标用统一描边的 SVG。
- **Don't** 让卡片双层嵌套（卡片里套卡片永远错）。
- **Don't** 用纯灰中性色，取暖灰阶。
- **Don't** 把阴影当日常装饰——阴影只响应状态。
- **Don't** 用 >1px 的彩色 border-left/right 做卡片强调。
