import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.characters import list_characters
from app.core.conversation import build_conversation_router
from app.core.db import get_db
from app.models.models import Progress

router = APIRouter(tags=["kids"])


def next_difficulty(progress: dict, topic: str) -> str:
    topic_progress = progress.get(topic, {})
    if topic_progress.get("correct_streak", 0) >= 3:
        return "harder"
    if topic_progress.get("wrong_streak", 0) >= 2:
        return "easier"
    return "same"


async def _difficulty_hook(db: AsyncSession, user_id: str, vertical: str, transcript: str) -> dict | None:
    """Post-message hook: recompute difficulty for the default topic bucket.
    A real implementation would classify `transcript` into a topic first."""
    result = await db.execute(
        select(Progress).where(Progress.user_id == uuid.UUID(user_id), Progress.vertical == vertical)
    )
    progress = result.scalar_one_or_none()
    current = progress.metric_json if progress else {}
    return {"last_difficulty": next_difficulty(current, "general")}


@router.get("/characters")
async def get_kids_characters(db: AsyncSession = Depends(get_db)):
    return await list_characters(db, "kids")


router.include_router(build_conversation_router("kids", post_message_hook=_difficulty_hook))
