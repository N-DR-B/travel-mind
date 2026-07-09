from app.agents import BaseAgent
from app.engine.state import TravelParams, AgentOutput
from app.tools.mock_data import get_destination_info
from app.tools.mcp_client import MCPClient

class DestinationAgent(BaseAgent):
    """目的地分析 Agent - 使用 MCP 搜索 + 传统API天气"""
    def __init__(self):
        super().__init__("destination", "目的地分析", "🧭")

    async def run(self, travel_params: TravelParams, mcp: MCPClient) -> dict:
        destination = travel_params.get("destination", "东京")
        info = get_destination_info(destination)
        search_results = await mcp.search(f"{destination}旅游攻略")
        return {
            "destination": destination,
            "country": info.get("country", ""),
            "language": info.get("language", ""),
            "currency": info.get("currency", ""),
            "best_season": info.get("best_season", ""),
            "description": info.get("description", ""),
            "cuisine": info.get("cuisine", []),
            "tips": info.get("tips", []),
            "search_results": search_results,
        }
