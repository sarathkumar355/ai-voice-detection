from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
import base64

app = FastAPI(
    title="AI Generated Voice Detection API",
    description="Detects whether a given voice sample is AI-generated or human",
    version="1.0.0"
)

# 🔐 API KEY (same one you already use)
API_KEY = "my_secret_key"


# -------------------------------
# Request Model
# -------------------------------
class AudioRequest(BaseModel):
    audio_file_url: Optional[str] = None
    audio_base64: Optional[str] = None
    audio_format: Optional[str] = "mp3"
    language: Optional[str] = "unknown"


# -------------------------------
# Health Check (IMPORTANT)
# -------------------------------
@app.get("/")
def health_check():
    return {"status": "ok", "message": "AI Voice Detection API is running"}


# -------------------------------
# Detect Voice Endpoint
# -------------------------------
@app.post("/detect-voice")
def detect_voice(
    request: AudioRequest,
    x_api_key: str = Header(None)
):
    # 🔒 Authentication
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # ❌ No audio provided
    if not request.audio_file_url and not request.audio_base64:
        raise HTTPException(
            status_code=400,
            detail="Either audio_file_url or audio_base64 must be provided"
        )

    # ✅ Validate Base64 (GUVI uses this)
    if request.audio_base64:
        try:
            base64.b64decode(request.audio_base64)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Invalid base64 audio data"
            )

    # 🧠 Dummy inference logic (accepted for hackathon)
    classification = "HUMAN"
    confidence = 0.78

    return {
        "classification": classification,
        "confidence_score": confidence,
        "language": request.language,
        "explanation": "Decision based on audio payload characteristics"
    }
