from __future__ import annotations
from pydantic import BaseModel
from typing import Optional


class TravelRequest(BaseModel):
    """用户旅行需求输入"""
    message: str
    session_id: Optional[str] = "default"


class AgentStatus(BaseModel):
    """Agent 工作状态"""
    agent_name: str
    agent_label: str
    status: str  # pending / running / completed / error
    message: Optional[str] = None
    icon: str = "🤖"


class WorkflowEvent(BaseModel):
    """SSE 事件"""
    event: str  # agent_start / agent_complete / agent_error / workflow_complete
    data: AgentStatus | dict


class TravelPlan(BaseModel):
    """最终旅行方案"""
    destination: Optional[str] = None
    days: Optional[int] = None
    budget: Optional[float] = None
    itinerary: Optional[list] = None
    booking: Optional[dict] = None
    visa: Optional[dict] = None
    packing: Optional[list] = None
    local_info: Optional[dict] = None
    summary: Optional[str] = None
