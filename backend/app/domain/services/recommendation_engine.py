from typing import List, Optional, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app.infrastructure.db.models import Dish, Combo
from app.schemas.recommendation_schema import (
    DishDTO,
    RecommendedDishDTO,
    ComboRecommendationDTO,
    RecommendationRequest
)

def get_meal_type_for_hour(hour: int) -> str:
    """Returns typical meal category based on 24h clock."""
    if 6 <= hour < 10:
        return "breakfast"
    elif 10 <= hour < 14:
        return "lunch"
    elif 14 <= hour < 17:
        return "afternoon_snack"
    elif 17 <= hour < 22:
        return "dinner"
    else:
        return "late_night"

class ContentBasedRecommendationEngine:
    @staticmethod
    def dish_to_dto(dish: Dish) -> DishDTO:
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

    def filter_candidates(
        self,
        dishes: List[Dish],
        cart_dish_ids: List[str],
        is_vegetarian: Optional[bool],
        max_price: Optional[int]
    ) -> List[Dish]:
        """Filters out unavailable items, cart items, non-vegetarian if restricted, and items over budget."""
        cart_id_set = set(cart_dish_ids)
        filtered = []
        for dish in dishes:
            if not dish.is_available:
                continue
            if dish.id in cart_id_set:
                continue
            if is_vegetarian is True and not dish.is_vegetarian:
                continue
            if max_price is not None and dish.price > max_price:
                continue
            filtered.append(dish)
        return filtered

    def recommend_dishes(
        self,
        all_dishes: List[Dish],
        request: RecommendationRequest
    ) -> List[RecommendedDishDTO]:
        """Calculates Content-Based Recommendations using Cosine Similarity."""
        # Step 1: Filter candidates
        candidates = self.filter_candidates(
            dishes=all_dishes,
            cart_dish_ids=request.cart_dish_ids,
            is_vegetarian=request.is_vegetarian,
            max_price=request.max_price
        )

        if not candidates:
            return []

        dish_map = {d.id: d for d in all_dishes}
        cart_dishes = [dish_map[d_id] for d_id in request.cart_dish_ids if d_id in dish_map]

        target_hour = request.current_time_hour if request.current_time_hour is not None else 12
        target_meal_type = get_meal_type_for_hour(target_hour)

        # Step 2: Handle Cold-Start (Cart is empty)
        if not cart_dishes:
            ranked_cold_start = []
            for candidate in candidates:
                time_boost = 1.0 if target_meal_type in (candidate.meal_types or []) else 0.5
                score = round(0.70 * time_boost, 3)
                reason = f"Món thịnh hành thích hợp cho khung giờ {target_meal_type}"
                ranked_cold_start.append((candidate, score, reason))

            ranked_cold_start.sort(key=lambda x: x[1], reverse=True)
            return [
                RecommendedDishDTO(
                    dish=self.dish_to_dto(c),
                    similarity_score=s,
                    recommendation_reason=r
                )
                for c, s, r in ranked_cold_start[:request.limit]
            ]

        # Step 3: Compute User Cart Preference Vector
        cart_vectors = [np.array(d.feature_vector, dtype=float) for d in cart_dishes if d.feature_vector]
        if not cart_vectors:
            cart_pref_vector = np.zeros(8, dtype=float)
        else:
            cart_pref_vector = np.mean(cart_vectors, axis=0)

        # Step 4: Compute Cosine Similarity against all Candidates
        candidate_vectors = [np.array(d.feature_vector, dtype=float) for d in candidates]
        if not candidate_vectors or cart_pref_vector.shape[0] == 0:
            similarities = np.zeros(len(candidates))
        else:
            cand_matrix = np.vstack(candidate_vectors)
            cart_matrix = cart_pref_vector.reshape(1, -1)
            similarities = cosine_similarity(cart_matrix, cand_matrix)[0]

        # Step 5: Score combination with contextual weights
        scored_recommendations: List[Tuple[Dish, float, str]] = []
        for i, candidate in enumerate(candidates):
            raw_sim = float(similarities[i])
            time_match = 1.0 if target_meal_type in (candidate.meal_types or []) else 0.7
            
            # Boost complementary items (Drinks & Sides)
            is_complementary = candidate.category in ["DoAnKem", "DoUong", "TrangMieng"]
            comp_boost = 1.25 if is_complementary else 1.0

            final_score = round(raw_sim * 0.55 + (time_match * 0.25) + (comp_boost * 0.20) / 1.25, 4)
            final_score = min(final_score, 1.0)

            if is_complementary:
                reason = f"Món ăn kèm/đồ uống bổ trợ hoàn hảo cho giỏ hàng (Độ tương đồng: {raw_sim:.2f})"
            else:
                reason = f"Độ tương đồng cao với khẩu vị các món đã chọn (Cosine: {raw_sim:.2f})"

            scored_recommendations.append((candidate, final_score, reason))

        # Sort by final score descending
        scored_recommendations.sort(key=lambda x: x[1], reverse=True)

        return [
            RecommendedDishDTO(
                dish=self.dish_to_dto(dish),
                similarity_score=score,
                recommendation_reason=reason
            )
            for dish, score, reason in scored_recommendations[:request.limit]
        ]

    def recommend_combos(
        self,
        all_dishes: List[Dish],
        combos: List[Combo],
        cart_dish_ids: List[str]
    ) -> List[ComboRecommendationDTO]:
        """Returns combo promotions matching current cart items."""
        dish_map = {d.id: d for d in all_dishes if d.is_available}
        cart_id_set = set(cart_dish_ids)

        recommended_combos: List[ComboRecommendationDTO] = []
        for combo in combos:
            if combo.primary_dish_id in cart_id_set:
                # Complementary item is available and not yet in cart
                if combo.complementary_dish_id in dish_map and combo.complementary_dish_id not in cart_id_set:
                    comp_dish = dish_map[combo.complementary_dish_id]
                    prim_dish = dish_map[combo.primary_dish_id]

                    orig_total = prim_dish.price + comp_dish.price
                    discounted = int(orig_total * (1.0 - combo.discount_rate))

                    recommended_combos.append(
                        ComboRecommendationDTO(
                            combo_id=combo.id,
                            combo_name=combo.combo_name or f"Combo {prim_dish.name} & {comp_dish.name}",
                            primary_dish_id=combo.primary_dish_id,
                            complementary_dish=self.dish_to_dto(comp_dish),
                            discount_rate=combo.discount_rate,
                            original_total=orig_total,
                            discounted_total=discounted
                        )
                    )

        return recommended_combos

recommendation_engine = ContentBasedRecommendationEngine()

