from app.agents import BaseAgent
from app.engine.state import TravelParams

class OrchestratorAgent(BaseAgent):
    """总调度 Agent - 理解用户意图，分解任务"""
    def __init__(self):
        super().__init__("orchestrator", "总调度", "🧠")

    async def run(self, travel_params: TravelParams, mcp=None) -> dict:
        params = travel_params or {}
        return {
            "parsed": params,
            "plan": [
                "destination", "itinerary", "booking",
                "visa" if params.get("destination") and "国内" not in str(params.get("destination", "")) else None,
                "packing", "local"
            ],
            "message": f"收到！让我为您规划 {params.get('destination', '目的地')} 的旅程"
        }
