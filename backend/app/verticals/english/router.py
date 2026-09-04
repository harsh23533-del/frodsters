import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.characters import list_characters
from app.core.conversation import build_conversation_router
from app.core.db import get_db
from app.core.llm import complete

router = APIRouter(tags=["english"])


async def score_utterance(transcript: str) -> dict:
    prompt = (
        "Analyse this spoken English for grammar and fluency. "
        'Return JSON: {"errors": [...], "fluency_score": 0-100}\n'
        f"Text: {transcript}"
    )
    raw = await complete([{"role": "user", "content": prompt}], response_format="json")
    return json.loads(raw)


async def _scoring_hook(db, user_id: str, vertical: str, transcript: str) -> dict | None:
    scored = await score_utterance(transcript)
    return {"fluency_score": scored.get("fluency_score"), "last_errors": scored.get("errors", [])}


@router.get("/characters")
async def get_english_characters(db: AsyncSession = Depends(get_db)):
    return await list_characters(db, "english")


router.include_router(build_conversation_router("english", post_message_hook=_scoring_hook))
