from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.track_events import TrackAddedEvent
from app.models.event_models import TrackEvent
from app.db.db import get_async_session
from app.services.event_dispatcher import dispatch_event
from app.services.rabbitmq import publish_event

router = APIRouter(prefix="/tracks", tags=["Tracks"])

@router.post("/add")
async def add_track(event: TrackAddedEvent, session: AsyncSession = Depends(get_async_session)):
    db_event = TrackEvent(event_type="TrackAdded", event_data=event.model_dump())
    session.add(db_event)
    await session.commit()

    await dispatch_event("TrackAdded", event.model_dump(), session)
    await publish_event("track.TrackAdded", event.model_dump())

    return {"status": "track added"}
