from sqlalchemy import Column, String, Boolean, DateTime, JSON
from datetime import datetime, timezone
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    is_vegetarian = Column(Boolean, default=False)
    preferred_flavors = Column(JSON, default=list)  # e.g. ["cay", "chua_ngot"]
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

