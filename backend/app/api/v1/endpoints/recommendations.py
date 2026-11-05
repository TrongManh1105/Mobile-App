from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.infrastructure.db.models import Dish, Combo
from app.schemas.recommendation_schema import (
    RecommendationRequest,
    RecommendedDishDTO,
    ComboRecommendationDTO
)
from app.domain.services.recommendation_engine import recommendation_engine

router = APIRouter()

@router.post("/dishes", response_model=List[RecommendedDishDTO])
async def get_dish_recommendations(
    request: RecommendationRequest,
    db: AsyncSession = Depends(get_db)
):
    """Gợi ý món ăn thông minh dựa trên Content-Based Cosine Similarity."""
    result = await db.execute(select(Dish))
    all_dishes = result.scalars().all()

    recommendations = recommendation_engine.recommend_dishes(
        all_dishes=all_dishes,
        request=request
    )
    return recommendations

@router.get("/combos", response_model=List[ComboRecommendationDTO])
async def get_combo_recommendations(
    cart_dish_ids: str = Query(..., description="Danh sách ID món trong giỏ hàng, cách nhau bằng dấu phẩy (vd: pho_01,com_01)"),
    db: AsyncSession = Depends(get_db)
):
    """Gợi ý combo ưu đãi và món ăn kèm bổ trợ theo giỏ hàng hiện tại."""
    dish_id_list = [d.strip() for d in cart_dish_ids.split(",") if d.strip()]

    dishes_result = await db.execute(select(Dish))
    all_dishes = dishes_result.scalars().all()

    combos_result = await db.execute(select(Combo))
    all_combos = combos_result.scalars().all()

    combos = recommendation_engine.recommend_combos(
        all_dishes=all_dishes,
        combos=all_combos,
        cart_dish_ids=dish_id_list
    )
    return combos

