from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class OrderItemCreateDTO(BaseModel):
    dish_id: str
    dish_name: str
    quantity: int = 1
    unit_price: int
    note: Optional[str] = None

class OrderCreateDTO(BaseModel):
    customer_phone: str = Field(..., json_schema_extra={"example": "0912345678"})
    customer_name: str = Field(default="Khách hàng", json_schema_extra={"example": "Nguyễn Văn A"})
    merchant_phone: str = Field(default="0987654321", json_schema_extra={"example": "0987654321"})
    delivery_type: str = Field(default="DineIn", json_schema_extra={"example": "DineIn"})  # DineIn, Takeaway, Delivery
    address_or_table: str = Field(default="Bàn 1", json_schema_extra={"example": "Bàn 5"})
    order_notes: Optional[str] = None
    items: List[OrderItemCreateDTO]

class OrderResponseDTO(BaseModel):
    order_id: str
    customer_phone: str
    customer_name: str
    merchant_phone: str
    status: str
    total_amount: int
    estimated_prep_time_minutes: int
    delivery_type: str
    address_or_table: str
    order_notes: Optional[str] = None
    formatted_message: str
    whatsapp_url: str
    sms_url: str
    created_at: datetime
    items: List[OrderItemCreateDTO]
