import asyncio, json, uuid
from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
from app.web.schemas import TravelRequest
from app.engine.graph import TravelWorkflow
from app.tools.memory import MemoryStore

router = APIRouter()
memory = MemoryStore()
workflows = {}

@router.get("/api/agents")
async def get_agents():
    return JSONResponse({"agents": [
        {"name": "orchestrator", "label": "总调度", "icon": "🧠"},
        {"name": "destination", "label": "目的地分析", "icon": "🧭"},
        {"name": "itinerary", "label": "行程编排", "icon": "📋"},
        {"name": "booking", "label": "机酒比价", "icon": "💰"},
        {"name": "visa", "label": "签证提醒", "icon": "🛂"},
        {"name": "packing", "label": "行前清单", "icon": "🎒"},
        {"name": "local", "label": "本地助手", "icon": "📍"},
        {"name": "summarizer", "label": "方案汇总", "icon": "📝"},
    ]})

@router.post("/api/travel")
async def start_travel(req: TravelRequest):
    session_id = req.session_id or str(uuid.uuid4())
    memory.add_message(session_id, "user", req.message)
    queue = asyncio.Queue()
    wf = TravelWorkflow()
    wf.set_event_queue(queue)
    workflows[session_id] = {"workflow": wf, "queue": queue}
    return JSONResponse({"session_id": session_id, "message": "工作流已启动"})

async def event_generator(session_id: str):
    wf_data = workflows.get(session_id)
    if not wf_data:
        yield f"data: {json.dumps({'event': 'error', 'data': {'message': 'Session not found'}})}\n\n"
        return
    queue = wf_data["queue"]
    wf = wf_data["workflow"]
    history = memory.get_history(session_id)
    user_msg = history[-1]["content"] if history else ""

    async def run_and_stream():
        try:
            result = await wf.run(user_msg)
            memory.add_message(session_id, "assistant", str(result))
        except Exception as e:
            await queue.put({"event": "workflow_error", "data": {"error": str(e)}})
        finally:
            await queue.put(None)

    asyncio.create_task(run_and_stream())
    while True:
        event = await queue.get()
        if event is None:
            break
        yield f"data: {json.dumps(event, ensure_ascii=False, default=str)}\n\n"
    yield f"data: {json.dumps({'event': 'done'})}\n\n"
    if session_id in workflows:
        del workflows[session_id]

@router.get("/api/travel/stream/{session_id}")
async def stream_travel(session_id: str):
    return StreamingResponse(event_generator(session_id), media_type="text/event-stream", headers={
        "Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"
    })

@router.get("/api/history/{session_id}")
async def get_history(session_id: str):
    history = memory.get_history(session_id)
    prefs = memory.get_all_preferences(session_id)
    return JSONResponse({"history": history, "preferences": prefs, "session_id": session_id})
