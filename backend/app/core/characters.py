from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Character


async def list_characters(db: AsyncSession, vertical: str):
    result = await db.execute(select(Character).where(Character.vertical == vertical))
    return result.scalars().all()


def build_prompt(character: Character, memory: list[str], history: list[dict]) -> list[dict]:
    system = character.system_prompt
    if memory:
        system += "\n\nThings you remember about this user:\n" + "\n".join(f"- {m}" for m in memory)
    return [{"role": "system", "content": system}, *history]
