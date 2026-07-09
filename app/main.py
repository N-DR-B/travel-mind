import uvicorn
import jinja2
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from pathlib import Path
from app.config import settings
from app.web.routes import router as api_router

app = FastAPI(title=settings.app_title, debug=settings.app_debug)
BASE_DIR = Path(__file__).parent

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Create Jinja2 env with stable caching to avoid LRUCache TypeError
_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(BASE_DIR / "templates")),
    autoescape=True,
    auto_reload=False,
    cache_size=0,
)
templates = Jinja2Templates(env=_jinja_env)

app.include_router(api_router)

AGENTS_META = [
    {"name": "orchestrator", "label": "总调度", "icon": "🧠"},
    {"name": "destination", "label": "目的地分析", "icon": "🧭"},
    {"name": "itinerary", "label": "行程编排", "icon": "📋"},
    {"name": "booking", "label": "机酒比价", "icon": "💰"},
    {"name": "visa", "label": "签证提醒", "icon": "🛂"},
    {"name": "packing", "label": "行前清单", "icon": "🎒"},
    {"name": "local", "label": "本地助手", "icon": "📍"},
    {"name": "summarizer", "label": "方案汇总", "icon": "📝"},
]

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "agents": AGENTS_META, "title": settings.app_title})

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.app_debug)
