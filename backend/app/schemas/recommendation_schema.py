from typing import List, Optional
from pydantic import BaseModel, Field

class DishDTO(BaseModel):
    id: str
    name: str
    category: str
    price: int
    prep_time_minutes: int
    flavor_tags: List[str] = Field(default_factory=list)
    meal_types: List[str] = Field(default_factory=list)
    is_vegetarian: bool = False
    is_available: bool = True
    image_url: Optional[str] = None

class RecommendationRequest(BaseModel):
    cart_dish_ids: List[str] = Field(default_factory=list)
    user_id: Optional[str] = None
    is_vegetarian: Optional[bool] = None
    max_price: Optional[int] = None
    current_time_hour: Optional[int] = None  # 0 - 23
    limit: int = 5

class RecommendedDishDTO(BaseModel):
    dish: DishDTO
    similarity_score: float
    recommendation_reason: str

class ComboRecommendationDTO(BaseModel):
    combo_id: str
    combo_name: str
    primary_dish_id: str
    complementary_dish: DishDTO
    discount_rate: float
    original_total: int
    discounted_total: int

