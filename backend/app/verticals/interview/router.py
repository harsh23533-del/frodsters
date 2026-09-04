from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.characters import list_characters
from app.core.db import get_db

router = APIRouter(tags=["interview"])


class InterviewState:
    INTRO = "intro"
    QUESTIONING = "questioning"
    WRAP_UP = "wrap_up"
    DONE = "done"


def next_state(current: str, questions_asked: int, max_questions: int = 5) -> str:
    if current == InterviewState.INTRO:
        return InterviewState.QUESTIONING
    if current == InterviewState.QUESTIONING and questions_asked >= max_questions:
        return InterviewState.WRAP_UP
    if current == InterviewState.WRAP_UP:
        return InterviewState.DONE
    return current


@router.get("/characters")
async def get_interview_characters(db: AsyncSession = Depends(get_db)):
    return await list_characters(db, "interview")
