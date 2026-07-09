from app.agents import BaseAgent
from app.engine.state import TravelParams
from app.tools.mock_data import get_exchange_rate, get_destination_info

class LocalAgent(BaseAgent):
    """本地助手 Agent"""
    def __init__(self):
        super().__init__("local", "本地助手", "📍")

    async def run(self, travel_params: TravelParams, mcp=None) -> dict:
        destination = travel_params.get("destination", "东京")
        info = get_destination_info(destination)
        rate = get_exchange_rate("CNY")
        target_currency = info.get("currency", "JPY").split("(")[-1].strip(")") if "(" in info.get("currency", "") else "JPY"
        return {
            "destination": destination,
            "country": info.get("country", ""),
            "language": info.get("language", ""),
            "currency": info.get("currency", ""),
            "timezone": info.get("timezone", ""),
            "exchange_rate": f"1 CNY = {rate.get('rates', {}).get(target_currency, 'N/A')} {target_currency}",
            "emergency": {"police": "110", "ambulance": "119/120", "embassy": "请查询中国驻当地使领馆联系方式"},
            "transport_tips": info.get("tips", []),
            "local_cuisine": info.get("cuisine", []),
        }
