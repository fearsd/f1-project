# app/utils/cache.py
import functools
import hashlib
import json
import logging
from functools import wraps
from typing import Callable, Awaitable
from fastapi import Request
import redis.asyncio as redis
from starlette.responses import JSONResponse
from datetime import date, datetime

logger = logging.getLogger("custom_cache")
logger.setLevel(logging.INFO)

def cache_response(redis_getter: Callable[[], any], expire: int = 60):
    def decorator(func: Callable[..., Awaitable]):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            redis = await redis_getter()
            if redis is None:
                raise RuntimeError("Redis client is not initialized")

            key = f"cache:{func.__name__}"

            cached = await redis.get(key)
            if cached:
                print(f"Cache HIT for {key}")
                data = json.loads(cached)
                return JSONResponse(content=data)
            else:
                print(f"Cache MISS for {key}")
                response = await func(*args, **kwargs)

                def serialize(obj):
                    if hasattr(obj, "__dict__"):
                        return {
                            k: serialize(v)
                            for k, v in vars(obj).items()
                            if not k.startswith("_")
                        }
                    elif isinstance(obj, list):
                        return [serialize(item) for item in obj]
                    elif isinstance(obj, (datetime, date)):
                        return obj.isoformat()
                    else:
                        return obj

                if isinstance(response, list):
                    to_cache = json.dumps([serialize(item) for item in response])
                else:
                    to_cache = json.dumps(serialize(response))

                await redis.set(key, to_cache, ex=expire)
                return JSONResponse(content=json.loads(to_cache))
        return wrapper
    return decorator
