import math
from typing import List, Tuple
from app.infrastructure.db.models import NearbyPOI
from app.schemas.poi_schema import POIDTO

EARTH_RADIUS_METERS = 6371000  # 6,371 km
WALKING_SPEED_METERS_PER_MIN = 80  # ~4.8 km/h

class POILocator:
    @staticmethod
    def haversine_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> int:
        """Calculates great-circle distance between two GPS coordinates in meters."""
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2.0) ** 2 + \
            math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

        distance = EARTH_RADIUS_METERS * c
        return int(round(distance))

    def filter_nearby_attractions(
        self,
        all_pois: List[NearbyPOI],
        user_lat: float,
        user_lon: float,
        available_wait_minutes: int,
        max_radius_meters: int = 1000
    ) -> List[POIDTO]:
        """
        Finds nearby POIs matching user's location and available preparation waiting time.
        Condition: RoundTripWalkingTime + SuggestedVisitTime <= available_wait_minutes + 10 mins
        """
        results: List[Tuple[NearbyPOI, int, int]] = []

        for poi in all_pois:
            distance = self.haversine_distance_meters(user_lat, user_lon, poi.latitude, poi.longitude)
            if distance > max_radius_meters:
                continue

            # Calculate walking time one-way and round-trip
            walk_one_way = max(int(round(distance / WALKING_SPEED_METERS_PER_MIN)), 1)
            walk_round_trip = walk_one_way * 2

            # Dynamically suggest visit/stroll time fitting the wait budget
            suggested_visit = poi.suggested_visit_minutes or 10
            if available_wait_minutes > walk_round_trip:
                suggested_visit = min(suggested_visit, max(available_wait_minutes - walk_round_trip, 5))

            results.append((poi, distance, walk_one_way, suggested_visit))

        # Sort by distance ascending (closest first)
        results.sort(key=lambda x: x[1])

        return [
            POIDTO(
                id=poi.id,
                name=poi.name,
                category=poi.category,
                latitude=poi.latitude,
                longitude=poi.longitude,
                distance_meters=dist,
                walking_duration_minutes=walk_mins,
                suggested_visit_minutes=visit_time,
                thumbnail_url=poi.thumbnail_url,
                google_maps_url=poi.google_maps_url or f"https://maps.google.com/?q={poi.latitude},{poi.longitude}",
                description=poi.description
            )
            for poi, dist, walk_mins, visit_time in results
        ]

poi_locator = POILocator()

