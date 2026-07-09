from app.agents import BaseAgent
from app.engine.state import TravelParams
from app.tools.mock_data import MOCK_PACKING_LISTS, get_destination_info

class PackingAgent(BaseAgent):
    """行前清单 Agent"""
    def __init__(self):
        super().__init__("packing", "行前清单", "🎒")

    async def run(self, travel_params: TravelParams, mcp=None) -> dict:
        destination = travel_params.get("destination", "东京")
        info = get_destination_info(destination)
        country = info.get("country", "日本")
        packing = MOCK_PACKING_LISTS.get(country, MOCK_PACKING_LISTS.get("日本", {}))
        days = travel_params.get("days", 5)
        return {
            "destination": destination,
            "country": country,
            "days": days,
            "essentials": packing.get("essentials", []),
            "clothing": packing.get("clothing", []),
            "electronics": packing.get("electronics", []),
            "health": packing.get("health", []),
            "other": packing.get("other", []),
            "weather_tip": f"{destination}当前天气适宜，建议携带{packing.get('clothing', ['舒适衣物'])}",
        }
