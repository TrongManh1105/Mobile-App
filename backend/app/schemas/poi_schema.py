from typing import Optional
from pydantic import BaseModel

class POIDTO(BaseModel):
    id: str
    name: str
    category: str
    latitude: float
    longitude: float
    distance_meters: int
    walking_duration_minutes: int
    suggested_visit_minutes: int
    thumbnail_url: Optional[str] = None
    google_maps_url: Optional[str] = None
    description: Optional[str] = None

