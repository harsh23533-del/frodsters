from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.characters import list_characters
from app.core.db import get_db

router = APIRouter(tags=["english"])


async def score_utterance(transcript: str) -> dict:
    """Placeholder: wire this to an LLM call that returns
    {"errors": [...], "fluency_score": 0-100} once OPENROUTER_API_KEY is set."""
    return {"errors": [], "fluency_score": None, "transcript": transcript}


@router.get("/characters")
async def get_english_characters(db: AsyncSession = Depends(get_db)):
    return await list_characters(db, "english")
