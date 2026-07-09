from app.agents import BaseAgent
from app.engine.state import TravelParams
from app.tools.mock_data import MOCK_VISA_INFO, get_destination_info

class VisaAgent(BaseAgent):
    """签证提醒 Agent - MCP 搜索最新签证政策"""
    def __init__(self):
        super().__init__("visa", "签证提醒", "🛂")

    async def run(self, travel_params: TravelParams, mcp=None) -> dict:
        destination = travel_params.get("destination", "东京")
        info = get_destination_info(destination)
        country = info.get("country", destination)
        visa = MOCK_VISA_INFO.get(country, MOCK_VISA_INFO.get("日本", {}))
        result = {"country": country, "destination": destination}
        if visa.get("visa_required"):
            result.update({"status": "需要签证", "visa_type": visa.get("type", ""), "processing_days": visa.get("processing_days", ""),
                           "fee": visa.get("fee", ""), "materials": visa.get("materials", []), "notes": visa.get("notes", "")})
        else:
            result.update({"status": "免签", "visa_type": visa.get("type", "免签"), "max_stay": "30天",
                           "requirements": visa.get("materials", []), "notes": visa.get("notes", "")})
        return result
