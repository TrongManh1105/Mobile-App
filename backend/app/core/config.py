import os
from typing import List
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Voice-Assisted Food Ordering Backend")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./food_app.db")
    CORS_ORIGINS: List[str] = ["*"]
    DEFAULT_LAT: float = float(os.getenv("DEFAULT_LAT", "21.0285"))
    DEFAULT_LON: float = float(os.getenv("DEFAULT_LON", "105.8542"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()

