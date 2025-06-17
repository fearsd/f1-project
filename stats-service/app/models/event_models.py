from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.db.db import Base

class BaseEvent(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    event_data: Mapped[JSONB] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )


class DriverEvent(BaseEvent):
    __tablename__ = "driver_events"


class TeamEvent(BaseEvent):
    __tablename__ = "team_events"


class RaceEvent(BaseEvent):
    __tablename__ = "race_events"


class TrackEvent(BaseEvent):
    __tablename__ = "track_events"
