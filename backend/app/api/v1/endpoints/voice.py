import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.domain.services.voice_pipeline import voice_nlu_pipeline

router = APIRouter()
logger = logging.getLogger("voice_stream")

@router.websocket("/stream")
async def voice_stream_websocket(websocket: WebSocket):
    """
    Bi-directional WebSocket for real-time voice interaction.
    Accepts:
      - Binary PCM audio chunks (16kHz 16-bit Mono)
      - Text / JSON messages: {"transcript": "...", "confidence": 0.95}
    Returns:
      - JSON NLU parsing result, intent, detected food items, and TTS response.
    """
    await websocket.accept()
    logger.info("Client connected to voice stream WebSocket.")
    try:
        while True:
            # We receive either text or bytes
            message = await websocket.receive()
            if "text" in message:
                data_str = message["text"]
                try:
                    payload = json.loads(data_str)
                    transcript = payload.get("transcript", "")
                    confidence = float(payload.get("confidence", 0.95))
                except json.JSONDecodeError:
                    transcript = data_str
                    confidence = 0.95

                nlu_result = voice_nlu_pipeline.parse_transcript(transcript, confidence=confidence)
                await websocket.send_json({
                    "event_type": "NLU_RECOGNIZED",
                    "nlu_result": nlu_result.model_dump()
                })

            elif "bytes" in message:
                # Binary audio chunk received (PCM 16kHz)
                # In mock/adapter mode, we acknowledge chunk reception with amplitude calculation
                raw_bytes = message["bytes"]
                chunk_len = len(raw_bytes)
                await websocket.send_json({
                    "event_type": "CHUNK_RECEIVED",
                    "chunk_bytes": chunk_len,
                    "status": "LISTENING"
                })

    except WebSocketDisconnect:
        logger.info("Voice stream WebSocket disconnected gracefully.")
    except Exception as e:
        logger.error(f"Error in voice stream WebSocket: {e}")
        try:
            await websocket.send_json({
                "event_type": "ERROR",
                "error_message": str(e)
            })
        except Exception:
            pass

@router.post("/parse")
async def parse_voice_text(payload: dict):
    """
    HTTP REST endpoint for voice NLU parsing.
    Acts as a reliable fallback when WebSockets are blocked or unavailable.
    """
    transcript = payload.get("transcript", "")
    confidence = float(payload.get("confidence", 0.95))
    nlu_result = voice_nlu_pipeline.parse_transcript(transcript, confidence=confidence)
    return {
        "event_type": "NLU_RECOGNIZED",
        "nlu_result": nlu_result.model_dump()
    }


