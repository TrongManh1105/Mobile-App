from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.infrastructure.db.models import NearbyPOI
from app.schemas.poi_schema import POIDTO
from app.domain.services.poi_locator import poi_locator
from app.core.config import settings

router = APIRouter()

@router.get("/nearby", response_model=List[POIDTO])
async def get_nearby_pois(
    lat: float = Query(default=settings.DEFAULT_LAT, description="Vĩ độ hiện tại"),
    lon: float = Query(default=settings.DEFAULT_LON, description="Kinh độ hiện tại"),
    available_wait_minutes: int = Query(default=20, description="Thời gian chờ món ETD (phút)"),
    max_radius_meters: int = Query(default=1000, description="Bán kính tìm kiếm (mét)"),
    db: AsyncSession = Depends(get_db)
):
    """Lấy danh sách các điểm tham quan lân cận phù hợp với thời gian chờ chế biến món."""
    result = await db.execute(select(NearbyPOI))
    all_pois = result.scalars().all()

    nearby_list = poi_locator.filter_nearby_attractions(
        all_pois=all_pois,
        user_lat=lat,
        user_lon=lon,
        available_wait_minutes=available_wait_minutes,
        max_radius_meters=max_radius_meters
    )
    return nearby_list

