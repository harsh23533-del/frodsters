from fastapi import HTTPException
from redis.asyncio import Redis


async def rate_limit(user_id: str, redis: Redis, limit: int = 30, window: int = 60):
    key = f"rl:{user_id}"
    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, window)
    if count > limit:
        raise HTTPException(429, "Too many requests")
