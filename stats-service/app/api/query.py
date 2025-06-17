from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_async_session
from app.models.read_models import DriverStanding, TeamStanding, Race, Track
from sqlalchemy.future import select
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/query", tags=["Query"])

@router.get("/standings/drivers")
@cache(expire=60)
async def get_driver_standings(season: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        select(DriverStanding).where(DriverStanding.season == season).order_by(DriverStanding.points.desc())
    )
    return result.scalars().all()

@router.get("/standings/teams")
@cache(expire=60)
async def get_team_standings(season: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        select(TeamStanding).where(TeamStanding.season == season).order_by(TeamStanding.points.desc())
    )
    return result.scalars().all()

@router.get("/races")
@cache(expire=60)
async def get_races(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Race))
    return result.scalars().all()

@router.get("/tracks")
@cache(expire=300)
async def get_tracks(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Track))
    return result.scalars().all()
