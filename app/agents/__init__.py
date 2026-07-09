from app.engine.state import TravelParams, AgentOutput
from app.tools.mock_data import get_destination_info, MOCK_VISA_INFO, get_exchange_rate
from app.tools.mcp_client import MCPClient
import json, re

class BaseAgent:
    """所有 Agent 的基类"""
    def __init__(self, name: str, label: str, icon: str = "🤖"):
        self.name = name
        self.label = label
        self.icon = icon

    async def run(self, travel_params: TravelParams, mcp: MCPClient) -> dict:
        raise NotImplementedError

def _extract_json(text: str) -> dict:
    """从 LLM 输出中提取 JSON"""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("\n", 1)[0]
        if text.endswith("```"):
            text = text[:-3]
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}
