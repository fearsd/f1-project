from pydantic import BaseModel

class TrackAddedEvent(BaseModel):
    name: str
    country: str
    length_km: float