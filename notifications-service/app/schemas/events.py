from pydantic import BaseModel
from datetime import date

class DriverCreatedEvent(BaseModel):
    name: str
    nationality: str
    date_of_birth: date
