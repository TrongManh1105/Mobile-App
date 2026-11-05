import pytest
from app.domain.services.voice_pipeline import voice_nlu_pipeline

def test_voice_nlu_add_to_cart_multiple_items():
    """Test parsing complex AddToCart with quantities, multiple items and special notes."""
    query = "Cho 2 bát phở bò tái nạm ít cay và 1 trà đá"
    result = voice_nlu_pipeline.parse_transcript(query)

    assert result.intent == "AddToCart"
    assert len(result.items) == 2
    
    # First item: 2 Phở Bò Tái Nạm, ít cay
    assert result.items[0].quantity == 2
    assert "Phở Bò Tái Nạm" in result.items[0].dish_name
    assert result.items[0].note == "ít cay"

    # Second item: 1 Trà Đá
    assert result.items[1].quantity == 1
    assert "Trà Đá" in result.items[1].dish_name

def test_voice_nlu_confirm_order():
    """Test recognizing ConfirmOrder intent."""
    queries = [
        "Xác nhận đặt đơn",
        "Thanh toán cho tôi",
        "Đặt luôn đi",
        "Chốt đơn hàng này nhé"
    ]
    for q in queries:
        result = voice_nlu_pipeline.parse_transcript(q)
        assert result.intent == "ConfirmOrder"

def test_voice_nlu_remove_item():
    """Test recognizing RemoveFromCart intent."""
    query = "Bỏ quẩy ra khỏi giỏ"
    result = voice_nlu_pipeline.parse_transcript(query)
    assert result.intent == "RemoveFromCart"
    assert "quẩy" in result.target_item

def test_voice_nlu_search():
    """Test recognizing SearchDish intent."""
    query = "Tìm quán bún chả gần đây"
    result = voice_nlu_pipeline.parse_transcript(query)
    assert result.intent == "SearchDish"
    assert "bún chả" in result.target_item

def test_voice_nlu_low_confidence_reprompt():
    """Test exception handling: Low confidence score triggers friendly reprompt."""
    query = "ư a ơ... khó nghe quá"
    result = voice_nlu_pipeline.parse_transcript(query, confidence=0.45)
    assert result.intent == "Unknown"
    assert "chưa nghe rõ" in result.tts_response

def test_voice_nlu_followup_and_prefix_cleaning():
    """Test follow-up phrases with compound prefixes, suffixes, and unit words."""
    test_cases = [
        ("thêm 1 quẩy giòn", 1, "Quẩy Giòn"),
        ("cho thêm 1 quẩy giòn", 1, "Quẩy Giòn"),
        ("thêm 1 nước uống gì đó", 1, "Nước Uống"),
        ("cho tôi thêm 2 cốc trà đá không đường", 2, "Trà Đá"),
        ("gọi thêm 1 đĩa quẩy giòn nữa nhé", 1, "Quẩy Giòn"),
        ("thêm một ổ bánh mì thịt nướng", 1, "Bánh Mì Thịt Nướng"),
        ("thêm 1 ly trà đào", 1, "Trà Đào"),
    ]
    for phrase, expected_qty, expected_dish in test_cases:
        res = voice_nlu_pipeline.parse_transcript(phrase)
        assert res.intent == "AddToCart", f"Failed intent for: {phrase}"
        assert len(res.items) == 1, f"Failed item count for: {phrase}"
        assert res.items[0].quantity == expected_qty, f"Failed quantity for: {phrase}"
        assert expected_dish.lower() in res.items[0].dish_name.lower(), f"Failed dish name for: {phrase}"


