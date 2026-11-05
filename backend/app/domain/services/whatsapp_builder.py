import urllib.parse
from datetime import datetime
from typing import List
from app.schemas.order_schema import OrderCreateDTO, OrderItemCreateDTO

class WhatsAppOrderBuilder:
    @staticmethod
    def format_currency_vnd(amount: int) -> str:
        """Formats integer amount to Vietnamese currency string (e.g. 150.000)."""
        return f"{amount:,}".replace(",", ".")

    def build_order_message(
        self,
        order_id: str,
        order_data: OrderCreateDTO,
        estimated_prep_time: int,
        total_amount: int
    ) -> str:
        """Formats order payload into structured text message."""
        time_str = datetime.now().strftime("%H:%M - %d/%m/%Y")

        item_lines = []
        for idx, it in enumerate(order_data.items, 1):
            subtotal = it.quantity * it.unit_price
            line = f"  {idx}. {it.dish_name} (x{it.quantity}) - {self.format_currency_vnd(subtotal)}đ"
            if it.note:
                line += f"\n     👉 Ghi chú: {it.note}"
            item_lines.append(line)

        items_formatted = "\n".join(item_lines)
        notes = order_data.order_notes or "Không có"

        message = (
            "🍱 [ĐƠN HÀNG MỚI - TỰ ĐỘNG TỪ VOICE FOOD APP] 🍱\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🔖 Mã đơn: #{order_id}\n"
            f"⏰ Thời gian: {time_str}\n"
            f"👤 Khách hàng: {order_data.customer_name} ({order_data.customer_phone})\n"
            f"📍 Nhận tại: {order_data.delivery_type} - {order_data.address_or_table}\n\n"
            "📋 CHI TIẾT MÓN ĂN:\n"
            f"{items_formatted}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 TỔNG CỘNG: {self.format_currency_vnd(total_amount)} VNĐ\n"
            f"⏳ Thời gian dự kiến: ~{estimated_prep_time} phút\n"
            f"💬 Ghi chú đơn: {notes}\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "👉 Vui lòng gửi tin nhắn này để xác nhận đơn hàng với quán!"
        )
        return message

    def generate_dispatch_links(
        self,
        merchant_phone: str,
        formatted_message: str
    ) -> tuple[str, str]:
        """Generates encoded WhatsApp URL and SMS fallback URL."""
        # Normalize phone: replace leading '0' with '84' for international format
        clean_phone = merchant_phone.strip().replace(" ", "").replace("-", "")
        if clean_phone.startswith("0"):
            intl_phone = "84" + clean_phone[1:]
        elif not clean_phone.startswith("84") and not clean_phone.startswith("+"):
            intl_phone = "84" + clean_phone
        else:
            intl_phone = clean_phone.replace("+", "")

        encoded_text = urllib.parse.quote(formatted_message)
        whatsapp_url = f"https://wa.me/{intl_phone}?text={encoded_text}"
        sms_url = f"sms:{clean_phone}?body={encoded_text}"

        return whatsapp_url, sms_url

whatsapp_order_builder = WhatsAppOrderBuilder()

