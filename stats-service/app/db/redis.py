from redis import asyncio as redis

_redis: redis.Redis | None = None

async def get_redis() -> redis.Redis:
    global _redis
    if _redis is None:
        _redis = redis.from_url("redis://redis", decode_responses=True)
    return _redis
