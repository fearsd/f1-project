from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.driver_events import (
    DriverCreatedEvent,
    DriverJoinedTeamEvent,
    DriverLeftTeamEvent,
)
from app.models.event_models import DriverEvent
from app.db.db import get_async_session
from app.services.event_dispatcher import dispatch_event
from app.services.rabbitmq import publish_event

router = APIRouter(prefix="/drivers", tags=["Drivers"])

@router.post("/create")
async def create_driver(event: DriverCreatedEvent, session: AsyncSession = Depends(get_async_session)):
    event_dict = event.model_dump()
    event_dict["date_of_birth"] = event.date_of_birth.isoformat()
    db_event = DriverEvent(event_type="DriverCreated", event_data=event_dict)
    session.add(db_event)
    await session.commit()

    await dispatch_event("DriverCreated", event.model_dump(), session)
    await publish_event("notifications.DriverCreated", event_dict)

    return {"status": "driver created"}

@router.post("/join")
async def driver_joins_team(event: DriverJoinedTeamEvent, session: AsyncSession = Depends(get_async_session)):
    event_dict = event.model_dump()
    event_dict["joined_at"] = event.joined_at.isoformat()
    db_event = DriverEvent(event_type="DriverJoinedTeam", event_data=event_dict)
    session.add(db_event)
    await session.commit()

    await dispatch_event("DriverJoinedTeam", event.model_dump(), session)
    return {"status": "driver joined team"}

@router.post("/leave")
async def driver_leaves_team(event: DriverLeftTeamEvent, session: AsyncSession = Depends(get_async_session)):
    event_dict = event.model_dump()
    event_dict["left_at"] = event.left_at.isoformat()
    db_event = DriverEvent(event_type="DriverLeftTeam", event_data=event_dict)
    session.add(db_event)
    await session.commit()

    await dispatch_event("DriverLeftTeam", event.model_dump(), session)
    return {"status": "driver left team"}
