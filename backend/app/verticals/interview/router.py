import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.characters import list_characters
from app.core.conversation import build_conversation_router
from app.core.db import get_db
from app.models.models import Progress

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


async def _state_hook(db: AsyncSession, user_id: str, vertical: str, transcript: str) -> dict | None:
    result = await db.execute(
        select(Progress).where(Progress.user_id == uuid.UUID(user_id), Progress.vertical == vertical)
    )
    progress = result.scalar_one_or_none()
    current = progress.metric_json if progress else {}
    state = current.get("state", InterviewState.INTRO)
    asked = current.get("questions_asked", 0) + 1
    new_state = next_state(state, asked)
    return {"state": new_state, "questions_asked": asked}


@router.get("/characters")
async def get_interview_characters(db: AsyncSession = Depends(get_db)):
    return await list_characters(db, "interview")


router.include_router(build_conversation_router("interview", post_message_hook=_state_hook))
