from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True)
    customer_phone = Column(String, nullable=False, index=True)
    customer_name = Column(String, default="Khách hàng")
    merchant_phone = Column(String, default="0987654321")
    status = Column(String, default="CREATED", index=True)  # CREATED, CONFIRMED, PREPARING, READY, COMPLETED, CANCELLED
    total_amount = Column(Integer, nullable=False, default=0)
    estimated_prep_time_minutes = Column(Integer, default=15)
    delivery_type = Column(String, default="DineIn")        # DineIn, Takeaway, Delivery
    address_or_table = Column(String, default="Bàn 1")
    order_notes = Column(String, nullable=True)
    whatsapp_payload = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String, primary_key=True, index=True)
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)
    dish_id = Column(String, ForeignKey("dishes.id"), nullable=False)
    dish_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Integer, nullable=False)
    note = Column(String, nullable=True)

    order = relationship("Order", back_populates="items")

