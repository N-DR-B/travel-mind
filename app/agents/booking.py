from app.agents import BaseAgent
from app.engine.state import TravelParams
from app.tools.mock_data import MOCK_FLIGHTS, MOCK_HOTELS

class BookingAgent(BaseAgent):
    """机酒比价 Agent"""
    def __init__(self):
        super().__init__("booking", "机酒比价", "💰")

    async def run(self, travel_params: TravelParams, mcp=None) -> dict:
        destination = travel_params.get("destination", "东京")
        flights = MOCK_FLIGHTS.get(destination, MOCK_FLIGHTS["东京"])
        hotels = MOCK_HOTELS.get(destination, MOCK_HOTELS["东京"])
        return {
            "destination": destination,
            "flights": flights,
            "hotels": hotels,
            "budget_estimate": {
                "flight_min": min(f["price"] for f in flights),
                "flight_max": max(f["price"] for f in flights),
                "hotel_min": min(h["price_per_night"] for h in hotels),
                "hotel_max": max(h["price_per_night"] for h in hotels),
            },
            "recommendation": f"推荐最低价航班 + 性价比酒店组合，预计总花费约{min(f['price'] for f in flights) + min(h['price_per_night'] for h in hotels) * travel_params.get('days', 5)}元"
        }
