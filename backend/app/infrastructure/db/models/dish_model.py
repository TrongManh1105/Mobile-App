from sqlalchemy import Column, String, Integer, Boolean, JSON
from app.core.database import Base

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)  # Pho, Com, Mi, Nuoc, TrangMieng, DoAnKem
    price = Column(Integer, nullable=False)                # VNĐ
    prep_time_minutes = Column(Integer, default=10)        # Base prep time
    flavor_tags = Column(JSON, default=list)               # ["dam_da", "nong", "thanh"]
    meal_types = Column(JSON, default=list)                # ["breakfast", "lunch", "dinner"]
    is_vegetarian = Column(Boolean, default=False)
    is_available = Column(Boolean, default=True)
    feature_vector = Column(JSON, default=list)            # Dense numerical vector for Cosine Sim
    image_url = Column(String, nullable=True)

