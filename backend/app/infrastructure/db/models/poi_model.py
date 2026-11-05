from sqlalchemy import Column, String, Float, Integer
from app.core.database import Base

class NearbyPOI(Base):
    __tablename__ = "nearby_poi"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False)               # Park, Museum, Cafe, Bookstore
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    suggested_visit_minutes = Column(Integer, default=15)
    walking_duration_minutes = Column(Integer, default=5)
    thumbnail_url = Column(String, nullable=True)
    google_maps_url = Column(String, nullable=True)
    description = Column(String, nullable=True)

