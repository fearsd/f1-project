from pydantic import BaseModel
from datetime import date
from typing import Optional


class DriverCreatedEvent(BaseModel):
    # driver_id: int
    name: str
    nationality: Optional[str] = None
    date_of_birth: date


class DriverJoinedTeamEvent(BaseModel):
    driver_id: int
    team_id: int
    season: int
    joined_at: date


class DriverLeftTeamEvent(BaseModel):
    driver_id: int
    team_id: int
    season: int
    left_at: date
