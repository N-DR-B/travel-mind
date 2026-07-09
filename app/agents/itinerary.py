from app.agents import BaseAgent
from app.engine.state import TravelParams
from app.tools.mock_data import MOCK_ATTRACTIONS, get_destination_info

class ItineraryAgent(BaseAgent):
    """行程编排 Agent"""
    def __init__(self):
        super().__init__("itinerary", "行程编排", "📋")

    async def run(self, travel_params: TravelParams, mcp=None) -> dict:
        destination = travel_params.get("destination", "东京")
        days = travel_params.get("days", 5)
        info = get_destination_info(destination)
        attractions = MOCK_ATTRACTIONS.get(destination, MOCK_ATTRACTIONS["东京"])
        itinerary = []
        for d in range(1, days + 1):
            daily = {"day": d, "title": f"第{d}天·{_get_day_theme(d, destination)}", "activities": _get_daily_activities(d, attractions, days)}
            itinerary.append(daily)
        return {"destination": destination, "days": days, "itinerary": itinerary, "cuisine_recommendations": info.get("cuisine", [])}

def _get_day_theme(day: int, dest: str) -> str:
    themes = {1: "抵达与初探索", 2: "经典必游", 3: "深度体验", 4: "自由探索", 5: "休闲购物", 6: "周边一日游", 7: "告别之旅"}
    return themes.get(day, "自由活动")

def _get_daily_activities(day: int, attractions: list, total_days: int) -> list:
    acts = []
    idx = (day - 1) * 2
    if idx < len(attractions):
        acts.append({"time": "上午", "activity": f"{attractions[idx]}游览", "description": f"探索{attractions[idx]}的魅力"})
    if idx + 1 < len(attractions):
        acts.append({"time": "下午", "activity": f"{attractions[idx + 1]}游览", "description": f"感受{attractions[idx + 1]}的独特风情"})
    acts.append({"time": "晚上", "activity": "品尝当地美食", "description": "推荐餐厅体验地道风味"})
    return acts
