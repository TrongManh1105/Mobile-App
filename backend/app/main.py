from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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

@app.get("/app", response_class=HTMLResponse, tags=["Demo App"])
async def demo_app():
    """Giao diện mô phỏng trải nghiệm thực tế trên trình duyệt."""
    html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Interactive Demo App is ready</h1>")

@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "docs_url": "/docs",
        "api_v1": settings.API_V1_STR
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

