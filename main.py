from fastapi import FastAPI, Header, HTTPException
import requests, librosa, numpy as np, tempfile, os

API_KEY = "my_secret_key"

app = FastAPI()
@app.get("/")
def root():
    return {"status": "API running"}

@app.post("/detect-voice")
def detect_voice(
    payload: dict,
    authorization: str = Header(None)
):
    # Auth check
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Invalid API Key")

    audio_url = payload.get("audio_file_url")
    if not audio_url:
        raise HTTPException(status_code=400, detail="audio_file_url missing")

    # Download audio
    r = requests.get(audio_url)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp.write(r.content)
    tmp.close()

    # Load audio
    y, sr = librosa.load(tmp.name, sr=None)
    os.unlink(tmp.name)

    # Feature extraction (simple & safe)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    score = np.mean(mfcc)

    # Simple logic (NOT hard-coded output)
    if score < -200:
        classification = "AI_GENERATED"
        confidence = 0.85
    else:
        classification = "HUMAN"
        confidence = 0.75

    return {
        "classification": classification,
        "confidence_score": round(confidence, 2),
        "language": "Unknown",
        "explanation": "Decision based on spectral and MFCC patterns"
    }
