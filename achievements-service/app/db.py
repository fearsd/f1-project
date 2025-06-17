import os
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from contextlib import asynccontextmanager

engine = create_async_engine(os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db"))
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

@asynccontextmanager
async def get_async_session():
    async with async_session_maker() as session:
        yield session

async def init_db():
    import models
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)