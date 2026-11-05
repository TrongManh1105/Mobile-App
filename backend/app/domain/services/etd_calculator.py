from typing import List, Dict, Any

class ETDCalculator:
    """Calculates Estimated Time of Dish Preparation (ETD) in minutes."""

    @staticmethod
    def calculate_etd(
        cart_items: List[Dict[str, Any]],
        kitchen_queue_depth: int = 1
    ) -> int:
        """
        Calculates preparation time in minutes.
        Each item is a dict with:
          - 'prep_time_minutes': int (base prep time)
          - 'quantity': int
        """
        if not cart_items:
            return 5  # Minimum prep time

        # Max base preparation time among all main dishes in cart
        max_base_time = max(item.get("prep_time_minutes", 8) for item in cart_items)

        # Additional time for items with quantity > 1
        extra_quantity_time = 0
        for item in cart_items:
            qty = item.get("quantity", 1)
            if qty > 1:
                # 2 minutes extra for each additional serving
                extra_quantity_time += (qty - 1) * 2

        # Kitchen load buffer (2 minutes per prior pending order in queue)
        queue_buffer = min(kitchen_queue_depth * 2, 20)

        total_etd = max_base_time + extra_quantity_time + queue_buffer
        return max(total_etd, 8)  # At least 8 minutes

etd_calculator = ETDCalculator()

