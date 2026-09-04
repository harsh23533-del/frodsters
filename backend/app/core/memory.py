import uuid

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.models import MemoryFact

EMBED_MODEL = "text-embedding-3-small"


async def embed_text(text: str) -> list[float]:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.openai.com/v1/embeddings",
            headers={"Authorization": f"Bearer {settings.openrouter_api_key}"},
            json={"model": EMBED_MODEL, "input": text},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["data"][0]["embedding"]


async def add_memory(db: AsyncSession, user_id: uuid.UUID, character_id: uuid.UUID, fact_text: str):
    vec = await embed_text(fact_text)
    fact = MemoryFact(user_id=user_id, character_id=character_id, fact_text=fact_text, embedding=vec)
    db.add(fact)
    await db.commit()
    return fact


async def get_relevant_memory(db: AsyncSession, user_id: uuid.UUID, character_id: uuid.UUID, query: str, k: int = 5):
    query_vec = await embed_text(query)
    result = await db.execute(
        select(MemoryFact)
        .where(MemoryFact.user_id == user_id, MemoryFact.character_id == character_id)
        .order_by(MemoryFact.embedding.cosine_distance(query_vec))
        .limit(k)
    )
    return [m.fact_text for m in result.scalars().all()]
