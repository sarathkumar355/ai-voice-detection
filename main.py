from fastapi import FastAPI, Header, HTTPException
import requests
import librosa
import numpy as np
import tempfile
import os

# =====================
# CONFIG
# =====================
API_KEY = "my_secret_key"

app = FastAPI()

# =====================
# ROOT ROUTE (RENDER HEALTH CHECK FIX)
# =====================
@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"status": "API running"}

# =====================
# VOICE DETECTION API
# =====================
@app.post("/detect-voice")
def detect_voice(
    payload: dict,
    authorization: str = Header(None)
):
    # ---- Auth check ----
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    audio_url = payload.get("audio_file_url")
    if not audio_url:
        raise HTTPException(status_code=400, detail="audio_file_url missing")

    # ---- Download audio ----
    try:
        response = requests.get(audio_url, timeout=10)
        response.raise_for_status()
    except Exception:
        raise HTTPException(status_code=400, detail="Unable to download audio")

    # ---- Save temp file ----
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp.write(response.content)
    tmp.close()

    # ---- Load audio ----
    try:
        y, sr = librosa.load(tmp.name, sr=None)
    except Exception:
        os.unlink(tmp.name)
        raise HTTPException(status_code=400, detail="Invalid audio file")

    os.unlink(tmp.name)

    # ---- Feature extraction ----
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    score = abs(np.mean(mfcc))

    # ---- Simple rule-based decision ----
    confidence = min(score / 300, 1.0)

    if score > 180:
        classification = "AI_GENERATED"
    else:
        classification = "HUMAN"

    return {
        "classification": classification,
        "confidence_score": round(confidence, 2),
        "language": "Unknown",
        "explanation": "Decision based on spectral and MFCC patterns"
    }
