from fastapi import FastAPI
from app.api import drivers, teams, races, tracks
from app.db.db import init_db

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis
from app.api.query import router as query_router
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI(
    title="F1 Stats Service",
    version="1.0.0",
    description="Сервис команд для отправки событий в Event Store + CQRS",
)
instrumentator = Instrumentator().instrument(app)

@app.on_event("startup")
async def on_startup():
    redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)
    FastAPICache.init(RedisBackend(redis_client), prefix="f1-cache")
    instrumentator.expose(app)
    await init_db()

app.include_router(drivers.router)
app.include_router(teams.router)
app.include_router(races.router)
app.include_router(tracks.router)
app.include_router(query_router)
