
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

## ✨ 项目亮点

| 维度 | 说明 |
|------|------|
| **前沿架构** | 基于 LangGraph 的有向图多 Agent 编排，8 个专家 Agent 协同决策 |
| **混合 API 策略** | MCP 协议（第三方搜索/抓取）+ 传统 REST API，按调用确定性划分 |
| **SSE 实时推送** | 前端实时展示 Agent 工作流状态，每个 Agent 的处理过程可视化 |
| **SaaS 级前端** | Tailwind CSS + 深色模式 + 响应式布局，专业仪表盘风格 |
| **生产就绪** | FastAPI 异步框架 + 完整的 REST + SSE 端点 |

---

## 🎯 它能做什么

用户只需用自然语言描述旅行需求，整个系统自动协作完成：

```
输入: "我想去日本东京玩5天，预算1万左右，喜欢美食和购物"
```

| Agent | 职责 | 技术通道 |
|-------|------|----------|
| 🧠 **总调度** | 理解意图、分解任务、调度子 Agent | LLM 推理 |
| 🧭 **目的地分析** | 目的地介绍、最佳季节、当地美食推荐 | MCP 🔵 搜索攻略 |
| 📋 **行程编排** | 按天生成每日行程，上午/下午/晚上 | 传统 API |
| 💰 **机酒比价** | 航班比价、酒店推荐、预算估算 | 传统 API + Mock |
| 🛂 **签证提醒** | 签证政策查询、材料清单生成 | MCP 🔵 搜索政策 |
| 🎒 **行前清单** | 根据天气/活动生成行李清单 | 传统 API 🟢 天气 |
| 📍 **本地助手** | 汇率换算、交通建议、紧急联系方式 | 传统 API 🟢 汇率 |
| 📝 **方案汇总** | 整合所有 Agent 输出，生成完整旅行报告 | LLM 聚合 |

### 输出结果

```
📋 行程总览 — 每日行程卡片（上午/下午/晚上三段式）
💰 费用明细 — 航班价格对比表 + 酒店价格对比表
🎒 行李清单 — 按类别分组（必备品/衣物/电子产品等）
📍 实用信息 — 签证状态、汇率、当地小贴士
```

---

## 🏗 技术架构

```
┌──────────────────────────────────────────────────────────┐
│                  用户界面 (Web Browser)                    │
│         Tailwind CSS + Alpine.js + Jinja2                 │
└──────────────────────┬───────────────────────────────────┘
                       │ HTTP / SSE
┌──────────────────────▼───────────────────────────────────┐
│                  FastAPI 后端 (Python)                     │
│   ┌──────────┐ ┌──────────┐ ┌──────────────────┐        │
│   │ REST API │ │ SSE 推流 │ │ 会话/记忆管理     │        │
│   └─────┬────┘ └──────────┘ └──────────────────┘        │
└─────────┼───────────────────────────────────────────────┘
          │
┌─────────▼───────────────────────────────────────────────┐
│              LangGraph 多 Agent 编排层                    │
│                                                          │
│  ┌──────────────────────────────────────────────┐       │
│  │           Orchestrator Agent (总调度)          │       │
│  └──────┬──────┬──────┬──────┬──────┬──────┬────┘       │
│         ▼      ▼      ▼      ▼      ▼      ▼            │
│  ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐            │
│  │目的地│ │行程│ │机酒│ │签证│ │清单│ │本地│ │汇总│     │
│  └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘            │
└──────────────────────────────────────────────────────────┘
          │
┌─────────▼───────────────────────────────────────────────┐
│              工具调用层 (Hybrid API Strategy)             │
│                                                          │
│  ┌───── MCP 通道 ─────┐   ┌───── 传统 API 通道 ─────┐  │
│  │  Fetch MCP (网页抓取) │   │  天气 API (OpenWeather)  │  │
│  │  Search MCP (搜索)    │   │  汇率 API              │  │
│  └──────────────────────┘   └────────────────────────┘  │
│                                                          │
│  LLM: DeepSeek (deepseek-chat)                           │
└──────────────────────────────────────────────────────────┘
```

### 混合 API 策略（面试亮点 🔥）

```
核心原则: 按「调用确定性」划分

  ┌─────────────────────┐
  │  调用是否固定？     │
  ├─────────┬───────────┤
  │   是    │    否     │
  ├─────────┼───────────┤
  │ 传统API │   MCP    │
  │ 天气/汇率│ 搜索/抓取 │
  │ 记忆存储 │ 签证查询  │
  └─────────┴───────────┘
```

- **确定性高的基础服务**（天气、汇率）→ 传统 REST API，保证稳定性和响应速度
- **不确定性高的信息服务**（搜索攻略、抓取网页）→ MCP 协议，Agent 动态发现和决策

---

## 🛠 技术栈

| 类别 | 技术 | 用途 |
|------|------|------|
| 语言 | Python 3.13+ | 后端运行时 |
| Web 框架 | FastAPI 0.115+ | REST + SSE 端点 |
| Agent 框架 | LangGraph 1.1+ | 多 Agent 有向图编排 |
| LLM | DeepSeek (deepseek-chat) | 智能推理与规划 |
| 协议 | MCP (Model Context Protocol) | 第三方工具标准化调用 |
| 前端 | Tailwind CSS + Alpine.js | 响应式 UI + 交互 |
| 模板 | Jinja2 | 服务端渲染 |
| 数据库 | SQLite + 内存存储 | 会话与偏好记忆 |
| 实时通信 | Server-Sent Events (SSE) | Agent 工作流状态推送 |

---

## 🚀 快速开始

### 前置条件

- Python 3.13+
- pip 或 uv 包管理器

### 安装与运行

```bash
# 克隆仓库
git clone https://github.com/N-DR-B/travel-mind.git
cd travel-mind

# 安装依赖（使用 pip 或 uv）
pip install -r requirements.txt

# 配置环境变量（可选，不配置走模拟数据）
cp .env.example .env
# 编辑 .env 填入 DEEPSEEK_API_KEY（可选）

# 启动服务
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

打开浏览器访问 **http://localhost:8000** 🎉

### 快速体验

在输入框输入以下任一示例即可看到完整工作流：

| 示例 | 说明 |
|------|------|
| `去日本东京玩5天，预算1万` | 🇯🇵 东京行程 + 机酒比价 + 签证 |
| `泰国曼谷带家人玩一周，喜欢美食` | 🇹🇭 曼谷家庭美食之旅 |
| `去巴黎度蜜月，7天预算3万` | 🇫🇷 巴黎浪漫之旅 |
| `新加坡自由行4天，购物为主` | 🇸🇬 新加坡购物游 |

---

## 📂 项目结构

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

## 🌟 面试话术速查

> **Q: 为什么用 MCP + 传统 API 混合？**
>
> "按调用确定性划分：确定性高的基础服务（天气、汇率）用传统 REST API 保证稳定性；不确定性高的信息服务（搜索攻略、网页抓取）用 MCP 协议让 Agent 动态发现和决策，既发挥了 Agent 的灵活性，又保证了核心服务的稳定性和响应速度。"

> **Q: 为什么用 LangGraph？**
>
> "LangGraph 天然支持有向图的工作流编排，每个 Agent 是一个节点，可以精确控制串行和并行的执行顺序，同时内置状态管理机制，非常适合多 Agent 协作场景。"

> **Q: 8 个 Agent 是怎么协作的？**
>
> "总调度 Agent 先理解用户意图，然后并行启动多个子 Agent（如目的地分析和行程编排同时运行），上下游有依赖关系的 Agent 串行等待（如机酒比价需要行程编排的结果），最后汇总 Agent 整合所有输出。"

---

## 📄 开源协议

MIT License © 2025 TravelMind

---

<div align="center">
  <sub>Built with ❤️ using DeepSeek + LangGraph + FastAPI</sub>
</div>
