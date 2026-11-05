from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field

class ExtractedItem(BaseModel):
    dish_name: str
    quantity: int = 1
    note: Optional[str] = None
    unit_price: Optional[int] = None

class VoiceNLUResult(BaseModel):
    intent: str  # SearchDish, AddToCart, RemoveFromCart, ModifyQuantity, ConfirmOrder, Unknown
    raw_transcript: str
    confidence_score: float
    items: List[ExtractedItem] = Field(default_factory=list)
    target_item: Optional[str] = None
    new_quantity: Optional[int] = None
    tts_response: str
    action_payload: Optional[Dict[str, Any]] = None

class VoiceEventMessage(BaseModel):
    event_type: str  # LISTENING, TRANSCRIPT_PARTIAL, NLU_RECOGNIZED, REPROMPT, ERROR
    session_id: Optional[str] = None
    transcript: Optional[str] = None
    confidence_score: Optional[float] = None
    nlu_result: Optional[VoiceNLUResult] = None
    error_message: Optional[str] = None

