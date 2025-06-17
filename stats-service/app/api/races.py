from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.race_events import RaceScheduledEvent, RaceFinishedEvent
from app.models.event_models import RaceEvent
from app.db.db import get_async_session
from app.services.event_dispatcher import dispatch_event
from app.services.rabbitmq import publish_event

router = APIRouter(prefix="/races", tags=["Races"])

@router.post("/schedule")
async def schedule_race(event: RaceScheduledEvent, session: AsyncSession = Depends(get_async_session)):
    event_dict = event.model_dump()
    event_dict["date"] = event.date.isoformat()
    db_event = RaceEvent(event_type="RaceScheduled", event_data=event_dict)
    session.add(db_event)
    await session.commit()

    await dispatch_event("RaceScheduled", event.model_dump(), session)
    return {"status": "race scheduled"}

@router.post("/finish")
async def finish_race(event: RaceFinishedEvent, session: AsyncSession = Depends(get_async_session)):
    db_event = RaceEvent(event_type="RaceFinished", event_data=event.model_dump())
    session.add(db_event)
    await session.commit()

    await dispatch_event("RaceFinished", event.model_dump(), session)
    await publish_event("race.RaceFinished", event.model_dump())
    return {"status": "race finished"}
