from pydantic import BaseModel
from datetime import date
from typing import List

class RaceScheduledEvent(BaseModel):
    # race_id: int
    name: str
    track_id: int
    date: date
    season: int


class RaceResultData(BaseModel):
    driver_id: int
    team_id: int
    position: int
    points: int


class RaceFinishedEvent(BaseModel):
    race_id: int
    results: List[RaceResultData]
