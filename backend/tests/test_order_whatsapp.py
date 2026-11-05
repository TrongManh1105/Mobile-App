import pytest
from app.domain.services.whatsapp_builder import whatsapp_order_builder
from app.schemas.order_schema import OrderCreateDTO, OrderItemCreateDTO

def test_whatsapp_order_builder_formatting_and_links():
    order_data = OrderCreateDTO(
        customer_phone="0912345678",
        customer_name="Nguyễn Văn Test",
        merchant_phone="0987654321",
        delivery_type="DineIn",
        address_or_table="Bàn 3",
        order_notes="Nhiều hành, ít bánh",
        items=[
            OrderItemCreateDTO(
                dish_id="pho_01",
                dish_name="Phở Bò Tái Nạm",
                quantity=2,
                unit_price=65000,
                note="Nhiều hành"
            ),
            OrderItemCreateDTO(
                dish_id="drink_01",
                dish_name="Trà Đá Thảo Mộc",
                quantity=2,
                unit_price=5000,
                note=None
            )
        ]
    )

    msg = whatsapp_order_builder.build_order_message(
        order_id="ORD-TEST-001",
        order_data=order_data,
        estimated_prep_time=15,
        total_amount=140000
    )

    assert "ORD-TEST-001" in msg
    assert "Phở Bò Tái Nạm (x2) - 130.000đ" in msg
    assert "Trà Đá Thảo Mộc (x2) - 10.000đ" in msg
    assert "140.000 VNĐ" in msg
    assert "Nhiều hành, ít bánh" in msg
    assert "Bàn 3" in msg

    wa_url, sms_url = whatsapp_order_builder.generate_dispatch_links(
        merchant_phone=order_data.merchant_phone,
        formatted_message=msg
    )

    assert wa_url.startswith("https://wa.me/84987654321?text=")
    assert sms_url.startswith("sms:0987654321?body=")

