import os, httpx
from app.tools.mock_data import get_exchange_rate as mock_rate

async def get_exchange_rate_api(base: str = "CNY", target: str = "") -> dict:
    """传统 API: 实时汇率查询 (确定性调用)"""
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"https://api.exchangerate-api.com/v4/latest/{base}", timeout=5.0)
            if resp.status_code == 200:
                data = resp.json()
                result = {"base": base, "rates": data.get("rates", {}), "source": "exchangerate-api"}
                if target:
                    result["target"] = target
                    result["rate"] = data.get("rates", {}).get(target, 0)
                return result
    except Exception:
        pass
    return mock_rate(base)
