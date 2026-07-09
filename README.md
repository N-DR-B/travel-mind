<div align="center">
  <img src="https://img.shields.io/badge/Python-3.13+-blue?style=flat&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.115+-green?style=flat&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/LangGraph-1.1+-purple?style=flat" alt="LangGraph">
  <img src="https://img.shields.io/badge/DeepSeek-OpenAI%20Compatible-red?style=flat" alt="DeepSeek">
  <img src="https://img.shields.io/badge/MCP-Protocol-orange?style=flat" alt="MCP">
  <br>
  <img src="https://img.shields.io/badge/Status-Active-success?style=flat" alt="Status">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat" alt="License">
</div>

<div align="center">
  <h1>🧳 TravelMind — 多智能体旅行管家</h1>
  <p><strong>Multi-Agent Travel Concierge powered by DeepSeek + LangGraph</strong></p>
  <p>一个由 <strong>8 个 AI Agent</strong> 协同工作、<strong>MCP 协议</strong>驱动的智能旅行规划系统</p>
  <br>
  <p align="center">
    <img src="https://github.com/N-DR-B/travel-mind/raw/main/.github/screenshot.png" alt="TravelMind Screenshot" width="800">
  </p>
</div>

---

## 项目亮点

| 维度 | 说明 |
|------|------|
| **多 Agent 架构** | 基于 LangGraph 的有向图编排，8 个专家 Agent 协同决策 |
| **混合 API 策略** | MCP 协议（第三方搜索/抓取）+ 传统 REST API，按调用确定性划分 |
| **SSE 实时推送** | Agent 工作流状态通过 SSE 实时推送到前端，导航栏紧凑状态指示 |
| **SaaS 级前端 v3** | 全屏布局 + 深海军蓝配色 + 深浅主题自适应 + 混合字号层级 |
| **生产就绪** | FastAPI 异步框架 + 完整的 REST + SSE 端点 |

### 前端设计

TravelMind 的前端采用专业仪表盘风格设计，具有以下特点：

- **全屏无留白**：100vh × 100vw 布局，左侧 340px 对话栏 + 右侧主内容区，无浪费空间
- **层次化排版**：22px 主标题 → 14px 卡片标题 → 12px 正文 → 10px 标签，字号递进清晰
- **模块大小错落**：全宽 Hero 卡片 → 三列日程卡片 → 两列高矮混合详情网格，打破单调
- **Agent 状态紧凑**：Agent 工作流从可视化管道改为导航栏紧凑数字指示，不干扰主界面
- **深色主题**：支持系统偏好自动切换深色/浅色模式

---

## 它能做什么

用户只需用自然语言描述旅行需求，整个系统自动协作完成：

```
输入: "我想去日本东京玩5天，预算1万左右，喜欢美食和购物"
```

| Agent | 职责 | 技术通道 |
|-------|------|----------|
| 🧠 **总调度** | 理解意图、分解任务、调度子 Agent | LLM 推理 |
| 🧭 **目的地分析** | 目的地介绍、最佳季节、当地美食推荐 | MCP 搜索攻略 |
| 📋 **行程编排** | 按天生成每日行程，上午/下午/晚上分段 | 传统 API |
| 💰 **机酒比价** | 航班比价、酒店推荐、预算估算 | 传统 API + Mock |
| 🛂 **签证提醒** | 签证政策查询、材料清单生成 | MCP 搜索政策 |
| 🎒 **行前清单** | 根据天气/活动生成行李清单 | 传统 API 天气查询 |
| 📍 **本地助手** | 汇率换算、交通建议、紧急联系方式 | 传统 API 汇率查询 |
| 📝 **方案汇总** | 整合所有 Agent 输出，生成完整旅行报告 | LLM 聚合 |

### 输出结果

- 📋 **行程总览** — 每日行程卡片（上午/下午/晚上三段式），标签栏切换视图
- 💰 **费用明细** — 航班价格对比表 + 酒店价格对比表，最低价高亮标注
- 🎒 **行李清单** — 按类别分组（必备品/衣物/电子产品/健康防护），勾选框样式
- 📍 **实用信息** — 签证状态、汇率、当地小贴士

---

## 技术架构

### 系统架构图

```
用户界面 (Web Browser)
  Tailwind CSS + Alpine.js + Jinja2
  全屏布局 | 深色模式 | 混合字号
        |
        | HTTP / SSE
        |
FastAPI 后端 (Python)
  REST API | SSE 推流 | 会话/记忆管理
        |
LangGraph 多 Agent 编排层
        |
  Orchestrator Agent (总调度)
    |     |     |     |     |     |     |
  目的地  行程  机酒  签证  清单  本地  汇总
        |
工具调用层 (Hybrid API Strategy)
  MCP 通道         |   传统 API 通道
  Fetch / Search   |   天气 / 汇率
```

### 混合 API 策略

按 **调用确定性** 划分：

| 通道 | 适用场景 | 特点 |
|------|---------|------|
| **传统 REST API** | 天气查询、汇率换算、会话记忆 | 固定 endpoint，输入输出确定，保证稳定性 |
| **MCP 协议** | 搜索攻略、抓取网页、签证政策查询 | 不确定性高，Agent 按需发现和调用 |

核心原则：确定性高的基础服务用传统 API，不确定性高的信息服务用 MCP 让 Agent 自主决策。

---

## 技术栈

| 类别 | 技术 | 用途 |
|------|------|------|
| 语言 | Python 3.13+ | 后端运行时 |
| Web 框架 | FastAPI 0.115+ | REST + SSE 端点 |
| Agent 框架 | LangGraph 1.1+ | 多 Agent 有向图编排 |
| LLM | DeepSeek (deepseek-chat) | 智能推理与规划 |
| 协议 | MCP (Model Context Protocol) | 第三方工具标准化调用 |
| 前端 | Tailwind CSS + Alpine.js | 全屏响应式 UI + 交互 |
| 模板 | Jinja2 | 服务端渲染 |
| 数据库 | SQLite + 内存存储 | 会话与偏好记忆 |
| 实时通信 | Server-Sent Events (SSE) | Agent 工作流状态推送 |

---

## 快速开始

### 前置条件

- Python 3.13+
- pip 包管理器

### 安装与运行

```bash
# 克隆仓库
git clone https://github.com/N-DR-B/travel-mind.git
cd travel-mind

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（可选，不配置走模拟数据）
cp .env.example .env
# 编辑 .env 填入 DEEPSEEK_API_KEY（可选）

# 启动服务
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

打开浏览器访问 **http://localhost:8000**

### 快速体验

| 输入示例 | 说明 |
|---------|------|
| 去日本东京玩5天，预算1万 | 东京行程 + 机酒比价 + 签证 |
| 泰国曼谷带家人玩一周，喜欢美食 | 曼谷家庭美食之旅 |
| 去巴黎度蜜月，7天预算3万 | 巴黎浪漫之旅 |
| 新加坡自由行4天，购物为主 | 新加坡购物游 |

---

## 项目结构

```
travel-mind/
├── app/
│   ├── agents/           # 8 个 Agent 实现
│   │   ├── orchestrator.py   🧠 总调度
│   │   ├── destination.py    🧭 目的地分析
│   │   ├── itinerary.py      📋 行程编排
│   │   ├── booking.py        💰 机酒比价
│   │   ├── visa.py           🛂 签证提醒
│   │   ├── packing.py        🎒 行前清单
│   │   ├── local.py          📍 本地助手
│   │   └── summarizer.py     📝 方案汇总
│   ├── engine/           # LangGraph 工作流引擎
│   │   ├── graph.py          # 工作流编排
│   │   └── state.py          # 状态定义
│   ├── tools/            # 工具调用层
│   │   ├── mcp_client.py     # MCP 客户端
│   │   ├── weather.py        # 传统 API: 天气
│   │   ├── exchange.py       # 传统 API: 汇率
│   │   ├── memory.py         # 传统 API: 记忆
│   │   └── mock_data.py      # 模拟数据
│   ├── web/              # Web 层
│   │   ├── routes.py         # REST + SSE 端点
│   │   └── schemas.py        # 数据模型
│   ├── templates/        # Jinja2 模板
│   │   ├── base.html
│   │   └── index.html        # 主页面
│   └── static/           # 静态资源
│       ├── css/style.css
│       └── js/app.js
├── requirements.txt
├── .env.example
└── README.md
```

---

## 架构设计思路

### 为什么选择 LangGraph？

LangGraph 天然支持有向图的 Agent 工作流编排，每个 Agent 是一个独立节点，可以精确控制串行和并行的执行顺序，同时内置状态管理机制，适合多 Agent 协作场景。

### 8 个 Agent 的协作流程

1. 总调度 Agent 先理解用户意图，提取目的地、天数、预算等参数
2. 目的地分析和行程编排并行运行
3. 机酒比价依赖行程编排的结果，串行等待
4. 签证提醒、行前清单、本地助手并行运行，互相独立
5. 汇总 Agent 整合所有输出，生成结构化旅行方案
6. SSE 实时推送每个 Agent 的状态变化到导航栏状态指示

### 前端设计演进

| 版本 | 特点 |
|------|------|
| v1 | 左对话右内容 + Agent 管道可视化 + 简单卡片 |
| v2 | 居中布局 + Hero 卡片 + 暖色调 |
| **v3** | **全屏布局 + 深海军蓝配色 + 隐藏 Agent 流程 + 混合字号模块错落** |

---

## 开源协议

MIT License

---

<div align="center">
  <sub>Built with using DeepSeek + LangGraph + FastAPI</sub>
</div>
