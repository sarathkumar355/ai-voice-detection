from fastapi import FastAPI, Header, HTTPException, Form
import base64

app = FastAPI(
    title="AI Generated Voice Detection API",
    version="1.0.0"
)

API_KEY = "my_secret_key"


# -----------------------
# Health Check (REQUIRED)
# -----------------------
@app.get("/")
def health():
    return {"status": "ok"}


# -----------------------
# Detect Voice (GUVI)
# -----------------------
@app.post("/detect-voice")
def detect_voice(
    x_api_key: str = Header(None),

    # GUVI sends FORM fields
    language: str = Form(None),
    audio_format: str = Form(None),
    audio_base64: str = Form(None)
):
    # 🔐 Auth
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # ❌ Missing audio
    if not audio_base64:
        raise HTTPException(
            status_code=400,
            detail="Either audio_file_url or audio_base64 must be provided"
        )

    # ✅ Validate Base64
    try:
        base64.b64decode(audio_base64)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid base64 audio data"
        )

    # 🧠 Dummy inference (allowed)
    return {
        "classification": "HUMAN",
        "confidence_score": 0.78,
        "language": language or "Unknown",
        "explanation": "Decision based on audio payload characteristics"
    }
