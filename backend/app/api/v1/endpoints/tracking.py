import json
import logging
from typing import Dict, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db, AsyncSessionLocal
from app.infrastructure.db.models import Order

router = APIRouter()
logger = logging.getLogger("tracking")

# In-memory connection manager for order tracking
class OrderTrackingManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, order_id: str, websocket: WebSocket):
        await websocket.accept()
        if order_id not in self.active_connections:
            self.active_connections[order_id] = set()
        self.active_connections[order_id].add(websocket)
        logger.info(f"Client connected for tracking order {order_id}")

    def disconnect(self, order_id: str, websocket: WebSocket):
        if order_id in self.active_connections:
            self.active_connections[order_id].discard(websocket)
            if not self.active_connections[order_id]:
                del self.active_connections[order_id]
        logger.info(f"Client disconnected from tracking order {order_id}")

    async def broadcast_status(self, order_id: str, status: str, message: str = ""):
        if order_id in self.active_connections:
            payload = {
                "event_type": "ORDER_STATUS_UPDATED",
                "order_id": order_id,
                "status": status,
                "message": message
            }
            dead_sockets = set()
            for ws in self.active_connections[order_id]:
                try:
                    await ws.send_json(payload)
                except Exception:
                    dead_sockets.add(ws)
            for ds in dead_sockets:
                self.active_connections[order_id].discard(ds)

tracking_manager = OrderTrackingManager()

@router.websocket("/ws/orders/{order_id}/tracking")
async def track_order_websocket(order_id: str, websocket: WebSocket):
    """WebSocket endpoint for tracking real-time order status updates."""
    await tracking_manager.connect(order_id, websocket)
    try:
        # Send initial status
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Order).where(Order.id == order_id))
            order = result.scalars().first()
            if order:
                await websocket.send_json({
                    "event_type": "INITIAL_STATUS",
                    "order_id": order.id,
                    "status": order.status,
                    "estimated_prep_time_minutes": order.estimated_prep_time_minutes
                })

        while True:
            # Keep-alive ping
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        tracking_manager.disconnect(order_id, websocket)
    except Exception as e:
        logger.error(f"Error in tracking websocket: {e}")
        tracking_manager.disconnect(order_id, websocket)

@router.patch("/orders/{order_id}/status")
async def update_order_status(
    order_id: str,
    status: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    """Cập nhật trạng thái đơn hàng (CONFIRMED, PREPARING, READY, COMPLETED, CANCELLED)."""
    valid_statuses = ["CREATED", "CONFIRMED", "PREPARING", "READY", "COMPLETED", "CANCELLED"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Trạng thái không hợp lệ. Phải là một trong: {valid_statuses}")

    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")

    order.status = status
    await db.commit()

    # Broadcast to tracking clients
    status_messages = {
        "CONFIRMED": "Quán đã xác nhận đơn hàng của bạn!",
        "PREPARING": "Bếp đang chế biến món ăn. Đồng hồ đếm ngược đã kích hoạt!",
        "READY": "Món ăn đã chế biến xong! Mời bạn đến quầy nhận món.",
        "COMPLETED": "Đơn hàng đã hoàn thành. Cảm ơn quý khách!",
        "CANCELLED": "Đơn hàng đã được hủy."
    }
    msg = status_messages.get(status, f"Trạng thái đơn hàng: {status}")
    await tracking_manager.broadcast_status(order_id, status, msg)

    return {"order_id": order_id, "status": status, "message": msg}

