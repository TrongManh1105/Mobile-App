import pytest
from app.infrastructure.db.models import Dish, Combo
from app.domain.services.recommendation_engine import (
    recommendation_engine,
    RecommendationRequest
)

@pytest.fixture
def sample_dishes():
    return [
        Dish(
            id="pho_01",
            name="Phở Bò Tái Nạm",
            category="Pho",
            price=65000,
            prep_time_minutes=8,
            flavor_tags=["dam_da", "nong"],
            meal_types=["breakfast", "lunch", "dinner"],
            is_vegetarian=False,
            is_available=True,
            feature_vector=[1.0, 0.0, 0.0, 0.0, 0.8, 0.1, 0.9, 0.65]
        ),
        Dish(
            id="pho_chay",
            name="Phở Chay Nấm Hương",
            category="Pho",
            price=50000,
            prep_time_minutes=7,
            flavor_tags=["thanh", "nong"],
            meal_types=["breakfast", "lunch"],
            is_vegetarian=True,
            is_available=True,
            feature_vector=[1.0, 0.0, 0.0, 0.0, 0.4, 0.0, 0.8, 0.50]
        ),
        Dish(
            id="com_suon",
            name="Cơm Tấm Sườn Bì",
            category="Com",
            price=60000,
            prep_time_minutes=10,
            flavor_tags=["dam_da", "beo"],
            meal_types=["lunch", "dinner"],
            is_vegetarian=False,
            is_available=True,
            feature_vector=[0.0, 1.0, 0.0, 0.0, 0.85, 0.3, 0.7, 0.60]
        ),
        Dish(
            id="quay_gion",
            name="Quẩy Giòn",
            category="DoAnKem",
            price=10000,
            prep_time_minutes=1,
            flavor_tags=["gion"],
            meal_types=["breakfast", "lunch"],
            is_vegetarian=True,
            is_available=True,
            feature_vector=[0.3, 0.0, 0.0, 0.0, 0.2, 0.0, 0.1, 0.10]
        ),
        Dish(
            id="tra_da",
            name="Trà Đá Thảo Mộc",
            category="DoUong",
            price=5000,
            prep_time_minutes=1,
            flavor_tags=["mat_lanh", "thanh"],
            meal_types=["breakfast", "lunch", "dinner", "afternoon_snack"],
            is_vegetarian=True,
            is_available=True,
            feature_vector=[0.0, 0.0, 0.0, 1.0, 0.1, 0.0, 0.0, 0.05]
        ),
        Dish(
            id="che_buoi",
            name="Chè Bưởi",
            category="TrangMieng",
            price=25000,
            prep_time_minutes=2,
            flavor_tags=["ngot_thanh"],
            meal_types=["afternoon_snack"],
            is_vegetarian=True,
            is_available=True,
            feature_vector=[0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.1, 0.25]
        ),
        Dish(
            id="mon_het_hang",
            name="Món Đã Hết Hàng",
            category="Pho",
            price=40000,
            prep_time_minutes=5,
            flavor_tags=["nong"],
            meal_types=["breakfast"],
            is_vegetarian=True,
            is_available=False,  # Out of stock
            feature_vector=[1.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.5, 0.40]
        )
    ]

@pytest.fixture
def sample_combos():
    return [
        Combo(
            id="combo_01",
            primary_dish_id="pho_01",
            complementary_dish_id="quay_gion",
            discount_rate=0.10,
            combo_name="Combo Phở & Quẩy"
        )
    ]

def test_recommendation_cold_start_user(sample_dishes):
    """Test 1: Cold-start user with empty cart receives trending suggestions."""
    req = RecommendationRequest(cart_dish_ids=[], current_time_hour=8, limit=3)
    results = recommendation_engine.recommend_dishes(sample_dishes, req)
    
    assert len(results) > 0
    assert len(results) <= 3
    # Top suggestion in the morning should be suitable for breakfast
    assert "breakfast" in results[0].dish.meal_types

def test_recommendation_time_contextual(sample_dishes):
    """Test 2: Time-contextual recommendations differ based on hour."""
    # Morning (08:00)
    morning_req = RecommendationRequest(cart_dish_ids=[], current_time_hour=8)
    morning_res = recommendation_engine.recommend_dishes(sample_dishes, morning_req)
    assert any("breakfast" in d.dish.meal_types for d in morning_res)

    # Afternoon snack (15:00)
    afternoon_req = RecommendationRequest(cart_dish_ids=[], current_time_hour=15)
    afternoon_res = recommendation_engine.recommend_dishes(sample_dishes, afternoon_req)
    # Afternoon should promote snacks / drinks
    afternoon_categories = [d.dish.category for d in afternoon_res]
    assert "TrangMieng" in afternoon_categories or "DoUong" in afternoon_categories

def test_recommendation_dietary_vegetarian(sample_dishes):
    """Test 3: Vegetarian user must receive 100% vegetarian dishes."""
    req = RecommendationRequest(
        cart_dish_ids=["pho_chay"],
        is_vegetarian=True,
        limit=5
    )
    results = recommendation_engine.recommend_dishes(sample_dishes, req)
    
    assert len(results) > 0
    for item in results:
        assert item.dish.is_vegetarian is True

def test_recommendation_budget_filter(sample_dishes):
    """Test 4: Budget limit constraint is strictly respected."""
    max_budget = 30000
    req = RecommendationRequest(
        cart_dish_ids=["pho_01"],
        max_price=max_budget,
        limit=5
    )
    results = recommendation_engine.recommend_dishes(sample_dishes, req)
    
    assert len(results) > 0
    for item in results:
        assert item.dish.price <= max_budget

def test_recommendation_out_of_stock_exclusion(sample_dishes):
    """Test 5: Out of stock items (is_available=False) must be excluded."""
    req = RecommendationRequest(cart_dish_ids=[], limit=10)
    results = recommendation_engine.recommend_dishes(sample_dishes, req)
    
    recommended_ids = [d.dish.id for d in results]
    assert "mon_het_hang" not in recommended_ids

def test_recommendation_combos(sample_dishes, sample_combos):
    """Test 6: Complementary combo recommendation matches items in cart."""
    combos = recommendation_engine.recommend_combos(
        all_dishes=sample_dishes,
        combos=sample_combos,
        cart_dish_ids=["pho_01"]
    )
    assert len(combos) == 1
    assert combos[0].combo_id == "combo_01"
    assert combos[0].complementary_dish.id == "quay_gion"
    assert combos[0].discounted_total < combos[0].original_total

