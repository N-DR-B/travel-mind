import asyncio, json
from typing import Any
from langgraph.graph import StateGraph, END
from app.engine.state import AgentState, TravelParams, AgentOutput
from app.tools.mcp_client import MCPClient
from app.tools.mock_data import get_destination_info
from app.agents.orchestrator import OrchestratorAgent
from app.agents.destination import DestinationAgent
from app.agents.itinerary import ItineraryAgent
from app.agents.booking import BookingAgent
from app.agents.visa import VisaAgent
from app.agents.packing import PackingAgent
from app.agents.local import LocalAgent
from app.agents.summarizer import SummarizerAgent

class TravelWorkflow:
    def __init__(self):
        self.mcp = MCPClient()
        self.orchestrator = OrchestratorAgent()
        self.destination = DestinationAgent()
        self.itinerary = ItineraryAgent()
        self.booking = BookingAgent()
        self.visa = VisaAgent()
        self.packing = PackingAgent()
        self.local = LocalAgent()
        self.summarizer = SummarizerAgent()
        self._event_queue = None
        self._all_agents = {
            "orchestrator": self.orchestrator,
            "destination": self.destination,
            "itinerary": self.itinerary,
            "booking": self.booking,
            "visa": self.visa,
            "packing": self.packing,
            "local": self.local,
            "summarizer": self.summarizer,
        }

    def set_event_queue(self, queue: asyncio.Queue):
        self._event_queue = queue

    async def _emit(self, event: str, data: dict):
        if self._event_queue:
            await self._event_queue.put({"event": event, "data": data})

    async def _run_agent(self, agent_name: str, agent: Any, params: TravelParams, outputs: dict) -> dict:
        await self._emit("agent_start", {"agent_name": agent_name, "agent_label": agent.label, "icon": agent.icon})
        try:
            result = await agent.run(params, mcp=self.mcp)
            await self._emit("agent_complete", {"agent_name": agent_name, "agent_label": agent.label, "icon": agent.icon, "result": result})
            return result
        except Exception as e:
            await self._emit("agent_error", {"agent_name": agent_name, "agent_label": agent.label, "error": str(e)})
            return {"error": str(e)}

    async def run(self, user_input: str) -> dict:
        await self.mcp.connect()
        outputs = {}
        params: TravelParams = {"destination": None, "days": None, "budget": None, "preferences": None, "origin": None}
        input_lower = user_input.lower()

        for word in ["东京","大阪","京都","北海道","冲绳","首尔","济州岛","曼谷","普吉岛","清迈","巴黎","伦敦","罗马","巴塞罗那","纽约","洛杉矶","悉尼","新加坡","马尔代夫","巴厘岛","迪拜"]:
            if word in user_input:
                params["destination"] = word
                break
        if not params["destination"]:
            import re as _re
            match = _re.search(r"去(\w+)", user_input)
            params["destination"] = match.group(1) if match else "东京"

        import re as _re2
        days_match = _re2.search(r"(\d+)\s*天", user_input)
        params["days"] = int(days_match.group(1)) if days_match else 5
        budget_match = _re2.search(r"(\d+[万万]?)\s*元", user_input)
        if budget_match:
            b = budget_match.group(1)
            params["budget"] = float(b.replace("万", "0000")) if "万" in b else float(b)
        prefs = []
        for kw in ["美食","购物","文化","自然","亲子","蜜月","独自","穷游","奢华","深度"]:
            if kw in user_input:
                prefs.append(kw)
        params["preferences"] = prefs if prefs else ["综合体验"]

        orchestrator_result = await self._run_agent("orchestrator", self.orchestrator, params, outputs)

        dest_result, visa_task = None, None
        dest_task = asyncio.create_task(self._run_agent("destination", self.destination, params, outputs))

        dest_result = await dest_task
        outputs["destination"] = dest_result

        itin_task = asyncio.create_task(self._run_agent("itinerary", self.itinerary, params, outputs))
        visa_coro = self._run_agent("visa", self.visa, params, outputs)
        visa_task = asyncio.create_task(visa_coro) if params.get("destination") else None

        outputs["itinerary"] = await itin_task
        outputs["booking"] = await self._run_agent("booking", self.booking, params, outputs)
        if visa_task:
            outputs["visa"] = await visa_task
        else:
            outputs["visa"] = {"status": "无需签证", "notes": "国内旅行"}

        pack_task = asyncio.create_task(self._run_agent("packing", self.packing, params, outputs))
        local_task = asyncio.create_task(self._run_agent("local", self.local, params, outputs))
        outputs["packing"] = await pack_task
        outputs["local"] = await local_task

        summary = await self._run_agent("summarizer", self.summarizer, params, outputs)
        outputs["summary"] = summary

        await self.mcp.disconnect()
        await self._emit("workflow_complete", {"outputs": outputs})
        return outputs
