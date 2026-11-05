from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.infrastructure.db.models import Dish
from app.schemas.recommendation_schema import DishDTO

router = APIRouter()

@router.get("/", response_model=List[DishDTO])
async def list_dishes(
    category: Optional[str] = Query(None, description="Lọc theo danh mục (Pho, Com, Bun, DoAnKem, DoUong, TrangMieng)"),
    is_vegetarian: Optional[bool] = Query(None, description="Lọc món ăn chay"),
    search: Optional[str] = Query(None, description="Tìm kiếm theo tên món"),
    db: AsyncSession = Depends(get_db)
):
    """Lấy danh sách thực đơn món ăn kèm bộ lọc."""
    query = select(Dish).where(Dish.is_available == True)

    if category:
        query = query.where(Dish.category == category)
    if is_vegetarian is not None:
        query = query.where(Dish.is_vegetarian == is_vegetarian)
    if search:
        query = query.where(Dish.name.ilike(f"%{search}%"))

    result = await db.execute(query)
    dishes = result.scalars().all()

    return [
        DishDTO(
            id=d.id,
            name=d.name,
            category=d.category,
            price=d.price,
            prep_time_minutes=d.prep_time_minutes,
            flavor_tags=d.flavor_tags or [],
            meal_types=d.meal_types or [],
            is_vegetarian=d.is_vegetarian,
            is_available=d.is_available,
            image_url=d.image_url
        )
        for d in dishes
    ]

@router.get("/{dish_id}", response_model=DishDTO)
async def get_dish(dish_id: str, db: AsyncSession = Depends(get_db)):
    """Lấy thông tin chi tiết một món ăn theo ID."""
    result = await db.execute(select(Dish).where(Dish.id == dish_id))
    dish = result.scalars().first()
    if not dish:
        raise HTTPException(status_code=404, detail="Món ăn không tồn tại")
    return DishDTO(
        id=dish.id,
        name=dish.name,
        category=dish.category,
        price=dish.price,
        prep_time_minutes=dish.prep_time_minutes,
        flavor_tags=dish.flavor_tags or [],
        meal_types=dish.meal_types or [],
        is_vegetarian=dish.is_vegetarian,
        is_available=dish.is_available,
        image_url=dish.image_url
    )

