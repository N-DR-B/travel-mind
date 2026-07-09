import json
from app.agents import BaseAgent
from app.engine.state import TravelParams

class SummarizerAgent(BaseAgent):
    """汇总报告 Agent"""
    def __init__(self):
        super().__init__("summarizer", "方案汇总", "📝")

    async def run(self, travel_params: TravelParams, mcp=None, agent_outputs: dict = None) -> dict:
        outputs = agent_outputs or {}
        dest = outputs.get("destination", {})
        itinerary = outputs.get("itinerary", {})
        booking = outputs.get("booking", {})
        visa = outputs.get("visa", {})
        packing = outputs.get("packing", {})
        local = outputs.get("local", {})
        dest_name = travel_params.get("destination", dest.get("destination", "目的地"))
        days = travel_params.get("days", itinerary.get("days", 5))
        budget = travel_params.get("budget", booking.get("budget_estimate", {}).get("hotel_min", 0))

        summary = f"""# {dest_name} {days}日旅行方案

## 目的地概览
{dest.get('description', '')}

**最佳季节**: {dest.get('best_season', '全年适宜')}
**语言**: {dest.get('language', '')} | **货币**: {dest.get('currency', '')}

## 行程安排
共{days}天精彩旅程，涵盖{dest_name}核心景点与地道体验。

## 预算参考
- 机票: {booking.get('budget_estimate', {}).get('flight_min', '待查询')}元起
- 住宿: {booking.get('budget_estimate', {}).get('hotel_min', '待查询')}元/晚起

## 出行准备
签证: {visa.get('status', '待查询')} | 汇率: {local.get('exchange_rate', '待查询')}

祝您旅途愉快！"""
        return {"destination": dest_name, "days": days, "summary": summary, "all_outputs": outputs}
