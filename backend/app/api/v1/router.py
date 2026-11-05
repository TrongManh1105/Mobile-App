from fastapi import APIRouter
from app.api.v1.endpoints import dishes, recommendations, poi, orders, voice, tracking

api_router = APIRouter()

api_router.include_router(dishes.router, prefix="/dishes", tags=["Dishes & Menu"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
api_router.include_router(poi.router, prefix="/poi", tags=["Nearby POI"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders & WhatsApp Dispatch"])
api_router.include_router(voice.router, prefix="/voice", tags=["Voice Stream & NLU"])
api_router.include_router(tracking.router, tags=["Real-time Order Tracking"])

