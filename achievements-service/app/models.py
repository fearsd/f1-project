from sqlalchemy import Column, Integer
from db import Base

class DriverAchievement(Base):
    __tablename__ = "driver_achievements"

    driver_id = Column(Integer, primary_key=True)
    total_races = Column(Integer, default=0, nullable=False)
    total_wins = Column(Integer, default=0, nullable=False)
    podiums = Column(Integer, default=0, nullable=False)
    best_finish = Column(Integer, default=0, nullable=False)