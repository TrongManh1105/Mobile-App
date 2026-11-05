import re
from typing import List, Tuple, Optional
from app.schemas.voice_schema import VoiceNLUResult, ExtractedItem

# Vietnamese number mapping
NUMBER_MAP = {
    "một": 1, "mot": 1, "1": 1,
    "hai": 2, "2": 2,
    "ba": 3, "3": 3,
    "bốn": 4, "bon": 4, "tư": 4, "4": 4,
    "năm": 5, "nam": 5, "5": 5,
    "sáu": 6, "sau": 6, "6": 6,
    "bảy": 7, "bay": 7, "7": 7,
    "tám": 8, "tam": 8, "8": 8,
    "chín": 9, "chin": 9, "9": 9,
    "mười": 10, "muoi": 10, "10": 10,
    "đôi": 2, "cặp": 2
}

CONFIRM_KEYWORDS = [
    "xác nhận", "xac nhan", "đặt đơn", "dat don", "thanh toán", "thanh toan",
    "đặt luôn", "dat luon", "chốt đơn", "chot don", "đồng ý", "dong y"
]

REMOVE_KEYWORDS = [
    "bỏ", "bo", "xóa", "xoa", "hủy", "huy", "bớt", "bot"
]

SEARCH_KEYWORDS = [
    "tìm", "tim", "có món", "co mon", "xem", "cho xem", "thực đơn", "thuc don"
]

NOTE_PATTERNS = [
    r"(ít cay|it cay)",
    r"(nhiều hành|nhieu hanh)",
    r"(không hành|khong hanh)",
    r"(không cay|khong cay)",
    r"(nhiều đá|nhieu da)",
    r"(ít đá|it da)",
    r"(ít đường|it duong)",
    r"(nước béo|nuoc beo)",
    r"(nước trong|nuoc trong)"
]

class VoiceNLUPipeline:
    def parse_transcript(self, text: str, confidence: float = 0.95) -> VoiceNLUResult:
        """Parses Vietnamese voice transcript into actionable structured Intent and Slots."""
        clean_text = text.strip()
        lower_text = clean_text.lower()

        # Step 1: Check confidence threshold (< 0.65 triggers Reprompt)
        if confidence < 0.65 or not clean_text:
            return VoiceNLUResult(
                intent="Unknown",
                raw_transcript=clean_text,
                confidence_score=confidence,
                items=[],
                tts_response="Tôi chưa nghe rõ, bạn có thể nói lại tên món ăn được không?"
            )

        # Step 2: Check Confirm Order Intent
        for kw in CONFIRM_KEYWORDS:
            if kw in lower_text:
                return VoiceNLUResult(
                    intent="ConfirmOrder",
                    raw_transcript=clean_text,
                    confidence_score=confidence,
                    tts_response="Đã nhận lệnh xác nhận đơn hàng. Đang chuẩn bị tin nhắn gửi đến quán."
                )

        # Step 3: Check Remove Item Intent
        for kw in REMOVE_KEYWORDS:
            if lower_text.startswith(kw) or f" {kw} " in lower_text:
                target = re.sub(r"^(bỏ|xóa|hủy|bớt|ra khỏi giỏ|khỏi giỏ)\s*", "", lower_text)
                target = re.sub(r"\s*(ra khỏi giỏ|khỏi giỏ|đi).*$", "", target).strip()
                return VoiceNLUResult(
                    intent="RemoveFromCart",
                    raw_transcript=clean_text,
                    confidence_score=confidence,
                    target_item=target,
                    tts_response=f"Đã xóa món {target} ra khỏi giỏ hàng."
                )

        # Step 4: Check Search Intent
        for kw in SEARCH_KEYWORDS:
            if lower_text.startswith(kw) or f" {kw} " in lower_text:
                query = re.sub(r"^(tìm kiếm|tìm quán|tìm món|tìm|có món|cho xem|xem)\s*", "", lower_text)
                query = re.sub(r"\s*(không|gần đây|nhé).*$", "", query).strip()
                return VoiceNLUResult(
                    intent="SearchDish",
                    raw_transcript=clean_text,
                    confidence_score=confidence,
                    target_item=query,
                    tts_response=f"Đang tìm kiếm món {query} cho bạn."
                )

        # Step 5: Check Add To Cart Intent
        # Extracts items separated by "và", ",", "cộng"
        extracted_items = self._extract_food_items(lower_text)
        if extracted_items:
            items_summary = ", ".join([f"{it.quantity} {it.dish_name}" for it in extracted_items])
            return VoiceNLUResult(
                intent="AddToCart",
                raw_transcript=clean_text,
                confidence_score=confidence,
                items=extracted_items,
                tts_response=f"Đã thêm {items_summary} vào giỏ hàng."
            )

        # Fallback Search
        return VoiceNLUResult(
            intent="SearchDish",
            raw_transcript=clean_text,
            confidence_score=confidence,
            target_item=clean_text,
            tts_response=f"Đang tìm món {clean_text} trong thực đơn."
        )

    def _extract_food_items(self, text: str) -> List[ExtractedItem]:
        """Extracts food items, quantities, and notes from phrase."""
        # Split segments on 'và', 'cộng', ','
        segments = re.split(r",|\s+và\s+|\s+cộng\s+", text)
        items: List[ExtractedItem] = []

        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue

            # Remove prefixes like "cho", "thêm", "lấy", "mua"
            seg = re.sub(r"^(cho tôi|cho em|cho mình|cho|thêm|lấy|mua|đặt)\s+", "", seg).strip()

            # Extract note
            note = None
            for pattern in NOTE_PATTERNS:
                m = re.search(pattern, seg)
                if m:
                    note = m.group(1)
                    seg = re.sub(pattern, "", seg).strip()
                    break

            # Extract quantity
            qty = 1
            # Check prefix words like "2 bát", "1 cốc", "3 phần", "hai phần"
            match_num = re.match(r"^(\d+|một|mot|hai|ba|bốn|bon|năm|nam|sáu|sau|bảy|bay|tám|tam|chín|chin|mười)\s*(bát|tô|phần|đĩa|cốc|ly|chén|suất|hộp)?\s*", seg)
            if match_num:
                num_token = match_num.group(1)
                qty = NUMBER_MAP.get(num_token, 1)
                seg = seg[match_num.end():].strip()

            if seg:
                # Capitalize dish name words
                dish_name = " ".join([w.capitalize() for w in seg.split()])
                items.append(ExtractedItem(
                    dish_name=dish_name,
                    quantity=qty,
                    note=note
                ))

        return items

voice_nlu_pipeline = VoiceNLUPipeline()

