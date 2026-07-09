from __future__ import annotations
from typing import Optional

class MCPClient:
    """MCP 客户端 - 连接第三方 MCP 服务器
    混合策略: MCP 用于 Agent 自主决策的工具（搜索、网页抓取等）
    """

    def __init__(self):
        self._connected = False
        self._search_db = {
            "东京": [{"title": "东京旅游攻略2026 - 必去景点TOP10", "url": "#", "snippet": "东京融合了传统与现代..."}],
            "大阪": [{"title": "大阪美食与景点完全指南", "url": "#", "snippet": "大阪被称为日本的厨房..."}],
            "首尔": [{"title": "首尔旅行攻略 - K-pop与韩屋", "url": "#", "snippet": "首尔是一座充满活力的城市..."}],
            "曼谷": [{"title": "曼谷自由行攻略 - 寺庙与美食", "url": "#", "snippet": "曼谷是东南亚最热门的旅行目的地..."}],
            "巴黎": [{"title": "巴黎旅行完全攻略 - 浪漫之都", "url": "#", "snippet": "从埃菲尔铁塔到卢浮宫..."}],
            "新加坡": [{"title": "新加坡4日游攻略 - 花园城市", "url": "#", "snippet": "新加坡虽小但精彩无限..."}],
        }

    async def connect(self) -> bool:
        self._connected = True
        return True

    async def search(self, query: str, max_results: int = 5) -> list[dict]:
        """MCP 搜索 - Agent 按需调用 (不确定性工具)"""
        results = []
        for keyword, data in self._search_db.items():
            if keyword in query:
                results.extend(data)
        if not results:
            results = [{"title": f"{query}相关信息", "url": "#", "snippet": f"关于{query}的搜索结果..."}]
        return results[:max_results]

    async def fetch_page(self, url: str) -> Optional[str]:
        """MCP 抓取 - Agent 按需获取网页内容"""
        return f"从 {url} 获取到的内容摘要..."

    async def disconnect(self) -> None:
        self._connected = False
