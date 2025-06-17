from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.team_events import TeamCreatedEvent
from app.models.event_models import TeamEvent
from app.db.db import get_async_session
from app.services.event_dispatcher import dispatch_event
from app.services.rabbitmq import publish_event

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.post("/create")
async def create_team(event: TeamCreatedEvent, session: AsyncSession = Depends(get_async_session)):
    db_event = TeamEvent(event_type="TeamCreated", event_data=event.model_dump())
    session.add(db_event)
    await session.commit()

    await dispatch_event("TeamCreated", event.model_dump(), session)
    await publish_event("team.TeamCreated", event.model_dump())
    return {"status": "team created"}
