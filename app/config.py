import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    deepseek_base_url: str = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    deepseek_model: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    weather_api_key: str = os.getenv("WEATHER_API_KEY", "")

    mcp_fetch_enabled: bool = os.getenv("MCP_FETCH_ENABLED", "true").lower() == "true"
    mcp_search_enabled: bool = os.getenv("MCP_SEARCH_ENABLED", "true").lower() == "true"

    app_secret_key: str = os.getenv("APP_SECRET_KEY", "travel-mind-dev-key")
    app_debug: bool = os.getenv("APP_DEBUG", "true").lower() == "true"
    app_title: str = "TravelMind - 多智能体旅行管家"


settings = Settings()
