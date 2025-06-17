from pydantic import BaseModel

class TeamCreatedEvent(BaseModel):
    name: str
    country: str