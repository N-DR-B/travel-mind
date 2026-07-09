from typing import TypedDict, Optional, Annotated, List
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage

class TravelParams(TypedDict):
    destination: Optional[str]
    days: Optional[int]
    budget: Optional[float]
    preferences: Optional[list[str]]
    origin: Optional[str]

class AgentOutput(TypedDict, total=False):
    destination_info: Optional[dict]
    itinerary: Optional[list[dict]]
    booking: Optional[dict]
    visa: Optional[dict]
    packing: Optional[list]
    local_info: Optional[dict]

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    user_input: str
    travel_params: Optional[TravelParams]
    current_agent: str
    agent_outputs: Optional[AgentOutput]
    error: Optional[str]
    status: Optional[dict]
    summary: Optional[str]
