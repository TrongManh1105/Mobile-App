import pytest
from app.domain.services.etd_calculator import etd_calculator
from app.domain.services.poi_locator import poi_locator
from app.infrastructure.db.models import NearbyPOI

def test_etd_calculator_single_and_multiple_items():
    # 1 item quantity 1
    cart1 = [{"prep_time_minutes": 8, "quantity": 1}]
    etd1 = etd_calculator.calculate_etd(cart1, kitchen_queue_depth=0)
    assert etd1 >= 8

    # 1 item quantity 3 -> extra time added
    cart2 = [{"prep_time_minutes": 8, "quantity": 3}]
    etd2 = etd_calculator.calculate_etd(cart2, kitchen_queue_depth=0)
    assert etd2 > etd1

    # Kitchen queue load added
    etd3 = etd_calculator.calculate_etd(cart2, kitchen_queue_depth=3)
    assert etd3 > etd2

def test_haversine_distance_and_poi_filtering():
    # Hanoi coordinates
    center_lat, center_lon = 21.0285, 105.8542

    sample_pois = [
        NearbyPOI(
            id="poi_close",
            name="Nhà Sách Gần",
            category="Bookstore",
            latitude=21.0290,
            longitude=105.8545,  # ~60 meters away
            suggested_visit_minutes=15,
            thumbnail_url=None,
            google_maps_url=None,
            description="Gần sát bên"
        ),
        NearbyPOI(
            id="poi_far",
            name="Địa Điểm Rất Xa",
            category="Park",
            latitude=21.0800,
            longitude=105.9200,  # > 5 km away
            suggested_visit_minutes=30,
            thumbnail_url=None,
            google_maps_url=None,
            description="Quá xa để đi bộ"
        )
    ]

    # Filter with 20 minutes wait time and max radius 1000m
    results = poi_locator.filter_nearby_attractions(
        all_pois=sample_pois,
        user_lat=center_lat,
        user_lon=center_lon,
        available_wait_minutes=20,
        max_radius_meters=1000
    )

    assert len(results) == 1
    assert results[0].id == "poi_close"
    assert results[0].distance_meters < 500
    assert results[0].walking_duration_minutes <= 5

