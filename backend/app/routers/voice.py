import httpx
from fastapi import APIRouter, UploadFile
from fastapi.responses import StreamingResponse

from app.core.config import settings

router = APIRouter(prefix="/api/voice", tags=["voice"])


@router.post("/transcribe")
async def transcribe(audio: UploadFile):
    audio_bytes = await audio.read()
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {settings.openrouter_api_key}"},
            files={"file": (audio.filename, audio_bytes)},
            data={"model": "whisper-1"},
            timeout=60,
        )
        resp.raise_for_status()
        return {"text": resp.json()["text"]}


@router.post("/synthesize")
async def synthesize(text: str, voice_id: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers={"xi-api-key": settings.elevenlabs_api_key},
            json={"text": text},
            timeout=60,
        )
        resp.raise_for_status()
        audio_bytes = resp.content
    return StreamingResponse(iter([audio_bytes]), media_type="audio/mpeg")
