import os, httpx
from app.config import settings

async def get_weather(city: str, days: int = 7) -> dict:
    """传统 API: 获取城市天气预报 (确定性调用)"""
    if not settings.weather_api_key or settings.weather_api_key == "your-weather-api-key-here":
        return _mock_weather(city)
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://api.openweathermap.org/data/2.5/forecast",
                params={"q": city, "appid": settings.weather_api_key, "units": "metric", "lang": "zh_cn"}
            )
            return _parse_weather_response(resp.json(), city) if resp.status_code == 200 else _mock_weather(city)
    except Exception:
        return _mock_weather(city)

def _parse_weather_response(data: dict, city: str) -> dict:
    forecasts = []
    for item in data.get("list", [])[:5]:
        forecasts.append({
            "date": item["dt_txt"].split()[0],
            "temp": round(item["main"]["temp"]),
            "feels_like": round(item["main"]["feels_like"]),
            "humidity": item["main"]["humidity"],
            "description": item["weather"][0]["description"],
            "icon": item["weather"][0]["icon"],
        })
    return {"city": city, "country": data.get("city", {}).get("country", ""), "forecasts": forecasts, "source": "openweathermap"}

def _mock_weather(city: str) -> dict:
    return {
        "city": city, "country": "Mock",
        "forecasts": [
            {"date": "2026-07-10", "temp": 28, "feels_like": 31, "humidity": 65, "description": "晴", "icon": "01d"},
            {"date": "2026-07-11", "temp": 26, "feels_like": 28, "humidity": 70, "description": "多云", "icon": "02d"},
            {"date": "2026-07-12", "temp": 27, "feels_like": 30, "humidity": 68, "description": "晴转多云", "icon": "03d"},
            {"date": "2026-07-13", "temp": 25, "feels_like": 27, "humidity": 75, "description": "小雨", "icon": "10d"},
            {"date": "2026-07-14", "temp": 29, "feels_like": 32, "humidity": 60, "description": "晴", "icon": "01d"},
        ],
        "source": "mock"
    }
