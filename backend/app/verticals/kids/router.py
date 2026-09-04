from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.characters import list_characters
from app.core.db import get_db

router = APIRouter(tags=["kids"])


def next_difficulty(progress: dict, topic: str) -> str:
    topic_progress = progress.get(topic, {})
    if topic_progress.get("correct_streak", 0) >= 3:
        return "harder"
    if topic_progress.get("wrong_streak", 0) >= 2:
        return "easier"
    return "same"


@router.get("/characters")
async def get_kids_characters(db: AsyncSession = Depends(get_db)):
    return await list_characters(db, "kids")
