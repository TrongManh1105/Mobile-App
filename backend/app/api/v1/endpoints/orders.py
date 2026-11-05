import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.infrastructure.db.models import Order, OrderItem
from app.schemas.order_schema import OrderCreateDTO, OrderResponseDTO, OrderItemCreateDTO
from app.domain.services.etd_calculator import etd_calculator
from app.domain.services.whatsapp_builder import whatsapp_order_builder

router = APIRouter()

@router.post("/", response_model=OrderResponseDTO)
async def create_and_dispatch_order(
    order_data: OrderCreateDTO,
    db: AsyncSession = Depends(get_db)
):
    """
    Tạo đơn hàng mới, tính toán ETD tự động và tạo payload tin nhắn WhatsApp/SMS.
    """
    if not order_data.items:
        raise HTTPException(status_code=400, detail="Đơn hàng phải có ít nhất một món ăn")

    # Generate unique Order ID
    order_id = f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    # Calculate total and prepare items for ETD
    total_amount = sum(it.quantity * it.unit_price for it in order_data.items)
    cart_items_for_etd = [
        {"prep_time_minutes": 10, "quantity": it.quantity}
        for it in order_data.items
    ]
    estimated_prep_time = etd_calculator.calculate_etd(cart_items_for_etd, kitchen_queue_depth=1)

    # Build WhatsApp / SMS Message Payload
    formatted_msg = whatsapp_order_builder.build_order_message(
        order_id=order_id,
        order_data=order_data,
        estimated_prep_time=estimated_prep_time,
        total_amount=total_amount
    )
    whatsapp_url, sms_url = whatsapp_order_builder.generate_dispatch_links(
        merchant_phone=order_data.merchant_phone,
        formatted_message=formatted_msg
    )

    # Persist in Database
    db_order = Order(
        id=order_id,
        customer_phone=order_data.customer_phone,
        customer_name=order_data.customer_name,
        merchant_phone=order_data.merchant_phone,
        status="CREATED",
        total_amount=total_amount,
        estimated_prep_time_minutes=estimated_prep_time,
        delivery_type=order_data.delivery_type,
        address_or_table=order_data.address_or_table,
        order_notes=order_data.order_notes,
        whatsapp_payload=whatsapp_url,
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_order)

    for it in order_data.items:
        db_item = OrderItem(
            id=str(uuid.uuid4()),
            order_id=order_id,
            dish_id=it.dish_id,
            dish_name=it.dish_name,
            quantity=it.quantity,
            unit_price=it.unit_price,
            note=it.note
        )
        db.add(db_item)

    await db.commit()

    return OrderResponseDTO(
        order_id=order_id,
        customer_phone=order_data.customer_phone,
        customer_name=order_data.customer_name,
        merchant_phone=order_data.merchant_phone,
        status="CREATED",
        total_amount=total_amount,
        estimated_prep_time_minutes=estimated_prep_time,
        delivery_type=order_data.delivery_type,
        address_or_table=order_data.address_or_table,
        order_notes=order_data.order_notes,
        formatted_message=formatted_msg,
        whatsapp_url=whatsapp_url,
        sms_url=sms_url,
        created_at=db_order.created_at,
        items=order_data.items
    )

@router.get("/{order_id}", response_model=OrderResponseDTO)
async def get_order_details(order_id: str, db: AsyncSession = Depends(get_db)):
    """Lấy thông tin chi tiết đơn hàng theo Order ID."""
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")

    items_result = await db.execute(select(OrderItem).where(OrderItem.order_id == order_id))
    items = items_result.scalars().all()

    items_dto = [
        OrderItemCreateDTO(
            dish_id=it.dish_id,
            dish_name=it.dish_name,
            quantity=it.quantity,
            unit_price=it.unit_price,
            note=it.note
        )
        for it in items
    ]

    return OrderResponseDTO(
        order_id=order.id,
        customer_phone=order.customer_phone,
        customer_name=order.customer_name or "Khách hàng",
        merchant_phone=order.merchant_phone,
        status=order.status,
        total_amount=order.total_amount,
        estimated_prep_time_minutes=order.estimated_prep_time_minutes,
        delivery_type=order.delivery_type,
        address_or_table=order.address_or_table,
        order_notes=order.order_notes,
        formatted_message="",
        whatsapp_url=order.whatsapp_payload or "",
        sms_url="",
        created_at=order.created_at,
        items=items_dto
    )

