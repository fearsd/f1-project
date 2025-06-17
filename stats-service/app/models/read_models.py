from sqlalchemy import String, Integer, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy.ext.declarative import declarative_base
from datetime import date, datetime

# Base = declarative_base()

from app.db.db import Base

class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    nationality: Mapped[str]
    date_of_birth: Mapped[date] = mapped_column(Date)
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"), nullable=True)
    joined_at: Mapped[date | None]
    left_at: Mapped[date | None]


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    country: Mapped[str]


class Race(Base):
    __tablename__ = "races"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    track_id: Mapped[int] = mapped_column(ForeignKey("tracks.id"))
    date: Mapped[date]
    season: Mapped[int]


class Track(Base):
    __tablename__ = "tracks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    country: Mapped[str]
    length_km: Mapped[float]


class RaceResult(Base):
    __tablename__ = "race_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    race_id: Mapped[int] = mapped_column(ForeignKey("races.id"))
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    position: Mapped[int]
    points: Mapped[int]


class DriverStanding(Base):
    __tablename__ = "driver_standings"

    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"), primary_key=True)
    season: Mapped[int] = mapped_column(primary_key=True)
    points: Mapped[int]


class TeamStanding(Base):
    __tablename__ = "team_standings"

    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), primary_key=True)
    season: Mapped[int] = mapped_column(primary_key=True)
    points: Mapped[int]



class TeamHistory(Base):
    __tablename__ = "team_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    joined_at: Mapped[date]
    left_at: Mapped[date | None]