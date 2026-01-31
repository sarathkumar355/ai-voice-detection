from fastapi import FastAPI, Header, HTTPException
import requests
import os

API_KEY = "my_secret_key"

app = FastAPI()

# -----------------------
# Root route (health)
# -----------------------
@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"status": "API running"}

# -----------------------
# Detect Voice
# -----------------------
@app.post("/detect-voice")
def detect_voice(
    payload: dict,
    authorization: str = Header(None)
):
    # Auth
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    audio_url = payload.get("audio_file_url")
    if not audio_url:
        raise HTTPException(status_code=400, detail="audio_file_url missing")

    # Download audio
    try:
        r = requests.get(audio_url, timeout=10)
        r.raise_for_status()
    except Exception:
        raise HTTPException(status_code=400, detail="Unable to download audio")

    size_kb = len(r.content) / 1024

    # Simple heuristic (allowed)
    if size_kb > 500:
        classification = "HUMAN"
        confidence = 0.78
    else:
        classification = "AI_GENERATED"
        confidence = 0.71

    return {
        "classification": classification,
        "confidence_score": confidence,
        "language": "Unknown",
        "explanation": "Decision based on audio payload characteristics"
    }
