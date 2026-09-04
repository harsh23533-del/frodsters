import uuid
from typing import Awaitable, Callable, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.characters import build_prompt
from app.core.db import get_db
from app.core.llm import complete
from app.core.memory import add_memory, get_relevant_memory
from app.core.rate_limit import rate_limit
from app.core.redis_client import redis_client
from app.models.models import Character, Message, Progress
from app.models.models import Session as ChatSession
from app.routers.auth import get_current_user

# A vertical can register a post-message hook: (db, user_id, vertical, transcript) -> dict
# The dict is merged into that user's progress.metric_json for the vertical.
PostMessageHook = Callable[[AsyncSession, str, str, str], Awaitable[Optional[dict]]]


def build_conversation_router(vertical: str, post_message_hook: PostMessageHook | None = None) -> APIRouter:
    router = APIRouter()

    @router.post("/sessions")
    async def start_session(
        character_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        user_id: str = Depends(get_current_user),
    ):
        await rate_limit(user_id, redis_client)
        character = await db.get(Character, character_id)
        if not character or character.vertical != vertical:
            raise HTTPException(404, "Character not found in this vertical")

        session = ChatSession(user_id=uuid.UUID(user_id), character_id=character_id)
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return {"session_id": session.id}

    @router.post("/sessions/{session_id}/messages")
    async def send_message(
        session_id: uuid.UUID,
        content: str,
        db: AsyncSession = Depends(get_db),
        user_id: str = Depends(get_current_user),
    ):
        await rate_limit(user_id, redis_client)

        session = await db.get(ChatSession, session_id)
        if not session or str(session.user_id) != user_id:
            raise HTTPException(404, "Session not found")
        character = await db.get(Character, session.character_id)

        db.add(Message(session_id=session_id, role="user", content=content))
        await db.commit()

        history_result = await db.execute(
            select(Message).where(Message.session_id == session_id).order_by(Message.created_at)
        )
        history = [{"role": m.role, "content": m.content} for m in history_result.scalars().all()]

        memory = await get_relevant_memory(db, session.user_id, session.character_id, content)
        prompt = build_prompt(character, memory, history)
        reply = await complete(prompt)

        db.add(Message(session_id=session_id, role="assistant", content=reply))
        await db.commit()

        if post_message_hook:
            metrics = await post_message_hook(db, user_id, vertical, content)
            if metrics:
                await _merge_progress(db, user_id, vertical, metrics)

        return {"reply": reply}

    @router.get("/sessions/{session_id}/messages")
    async def get_messages(
        session_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        user_id: str = Depends(get_current_user),
    ):
        session = await db.get(ChatSession, session_id)
        if not session or str(session.user_id) != user_id:
            raise HTTPException(404, "Session not found")
        result = await db.execute(
            select(Message).where(Message.session_id == session_id).order_by(Message.created_at)
        )
        return [{"role": m.role, "content": m.content} for m in result.scalars().all()]

    @router.get("/progress")
    async def get_progress(db: AsyncSession = Depends(get_db), user_id: str = Depends(get_current_user)):
        result = await db.execute(
            select(Progress).where(Progress.user_id == uuid.UUID(user_id), Progress.vertical == vertical)
        )
        progress = result.scalar_one_or_none()
        return progress.metric_json if progress else {}

    return router


async def _merge_progress(db: AsyncSession, user_id: str, vertical: str, metrics: dict):
    result = await db.execute(
        select(Progress).where(Progress.user_id == uuid.UUID(user_id), Progress.vertical == vertical)
    )
    progress = result.scalar_one_or_none()
    if progress is None:
        progress = Progress(user_id=uuid.UUID(user_id), vertical=vertical, metric_json=metrics)
        db.add(progress)
    else:
        progress.metric_json = {**progress.metric_json, **metrics}
    await db.commit()
