from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from app.models.read_models import (
    Driver, Team, Race, RaceResult,
    DriverStanding, TeamStanding, TeamHistory, Track
)
from app.schemas.driver_events import (
    DriverCreatedEvent, DriverJoinedTeamEvent, DriverLeftTeamEvent
)
from app.schemas.race_events import (
    RaceScheduledEvent, RaceFinishedEvent, RaceResultData
)
from app.schemas.track_events import TrackAddedEvent
from app.schemas.team_events import TeamCreatedEvent
from datetime import datetime


EventHandler = dict[str, callable]
event_handlers: EventHandler = {}

def register_event(event_type: str):
    def decorator(fn):
        event_handlers[event_type] = fn
        return fn
    return decorator


@register_event("DriverCreated")
async def handle_driver_created(session: AsyncSession, data: dict):
    payload = DriverCreatedEvent(**data)
    driver = Driver(
        name=payload.name,
        nationality=payload.nationality,
        date_of_birth=payload.date_of_birth
    )
    session.add(driver)
    await session.commit()


@register_event("TeamCreated")
async def handle_team_created(session: AsyncSession, data: dict):
    payload = TeamCreatedEvent(**data)
    team = Team(
        name=payload.name,
        country=payload.country
    )
    session.add(team)
    await session.commit()


@register_event("DriverJoinedTeam")
async def handle_driver_joined_team(session: AsyncSession, data: dict):
    payload = DriverJoinedTeamEvent(**data)
    driver = await session.get(Driver, payload.driver_id)
    if driver:
        driver.team_id = payload.team_id
        driver.joined_at = payload.joined_at
        driver.left_at = None
        session.add(driver)

        history = TeamHistory(
            driver_id=payload.driver_id,
            team_id=payload.team_id,
            joined_at=payload.joined_at
        )
        session.add(history)
        await session.commit()


@register_event("DriverLeftTeam")
async def handle_driver_left_team(session: AsyncSession, data: dict):
    payload = DriverLeftTeamEvent(**data)
    driver = await session.get(Driver, payload.driver_id)
    if driver and driver.team_id == payload.team_id:
        driver.left_at = payload.left_at
        driver.team_id = None
        session.add(driver)

        result = await session.execute(
            select(TeamHistory)
            .where(TeamHistory.driver_id == payload.driver_id)
            .where(TeamHistory.team_id == payload.team_id)
            .where(TeamHistory.left_at == None)
        )
        history = result.scalar_one_or_none()
        if history:
            history.left_at = payload.left_at
            session.add(history)
        await session.commit()


@register_event("RaceScheduled")
async def handle_race_scheduled(session: AsyncSession, data: dict):
    payload = RaceScheduledEvent(**data)
    race = Race(
        name=payload.name,
        track_id=payload.track_id,
        date=payload.date, 
        season=payload.season
    )
    session.add(race)
    await session.commit()


@register_event("RaceFinished")
async def handle_race_finished(session: AsyncSession, data: dict):
    payload = RaceFinishedEvent(**data)

    # Получаем дату гонки по её ID
    result = await session.execute(
        select(Race).where(Race.id == payload.race_id)
    )
    race = result.scalar_one_or_none()

    if not race:
        raise ValueError(f"Race with id {payload.race_id} not found")

    season = race.season

    for result in payload.results:
        race_result = RaceResult(
            race_id=payload.race_id,
            driver_id=result.driver_id,
            team_id=result.team_id,
            position=result.position,
            points=result.points
        )
        session.add(race_result)

        driver_standing = await session.get(
            DriverStanding, {"driver_id": result.driver_id, "season": season}
        )
        if not driver_standing:
            driver_standing = DriverStanding(driver_id=result.driver_id, season=season, points=0)
            session.add(driver_standing)
        driver_standing.points += result.points

        team_standing = await session.get(
            TeamStanding, {"team_id": result.team_id, "season": season}
        )
        if not team_standing:
            team_standing = TeamStanding(team_id=result.team_id, season=season, points=0)
            session.add(team_standing)
        team_standing.points += result.points

    await session.commit()


@register_event("TrackAdded")
async def handle_track_added(session: AsyncSession, data: dict):
    payload = TrackAddedEvent(**data)
    track = Track(
        name=payload.name,
        country=payload.country,
        length_km=payload.length_km
    )
    session.add(track)
    await session.commit()


async def dispatch_event(event_type: str, event_data: dict, session: AsyncSession):
    handler = event_handlers.get(event_type)
    if handler:
        await handler(session, event_data)
    else:
        raise ValueError(f"No handler registered for event type: {event_type}")
