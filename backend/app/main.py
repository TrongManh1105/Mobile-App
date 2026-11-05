from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from app.core.config import settings
from app.core.database import init_db
from app.api.v1.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure database tables exist and seed if empty
    await init_db()
    try:
        from app.infrastructure.db.seed import seed_database
        await seed_database()
    except Exception as e:
        print(f"Auto-seed notification: {e}")
    yield
    # Shutdown

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Backend AI Engine cho Ứng Dụng Đặt Đồ Ăn Trợ Lý Giọng Nói (Voice-Assisted Food Ordering App)",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router v1
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.api_route("/", methods=["GET", "HEAD"], tags=["Root"])
async def root(request: Request):
    """
    Nếu truy cập từ trình duyệt web (Chrome, Safari, Edge...): Mở thẳng giao diện App Mobile.
    Nếu gọi từ API client hoặc test: Trả về JSON trạng thái.
    """
    accept = request.headers.get("accept", "")
    user_agent = request.headers.get("user-agent", "").lower()
    is_browser = any(br in user_agent for br in ["mozilla", "chrome", "safari", "edge", "mobile"])

    if is_browser and "text/html" in accept:
        html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())

    return JSONResponse({
        "status": "online",
        "service": settings.PROJECT_NAME,
        "docs_url": "/docs",
        "api_v1": settings.API_V1_STR
    })

@app.api_route("/app", methods=["GET", "HEAD"], response_class=HTMLResponse, tags=["Demo App"])
async def demo_app():
    """Giao diện mô phỏng trải nghiệm thực tế trên trình duyệt."""
    html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Interactive Demo App is ready</h1>")

@app.api_route("/health", methods=["GET", "HEAD"], tags=["Health"])
async def health_check():
    return {"status": "healthy"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

