from schemas.events import DriverCreatedEvent
from config import logging
from metrics import EVENTS_PROCESSED

async def handle_event(event_type: str, data: dict):
    if event_type == "DriverCreated":
        payload = DriverCreatedEvent(**data)
        logging.info(f"[Notification] Новый гонщик: {payload.name} ({payload.nationality})")
    elif event_type == "DriverJoinedTeam":
        logging.info(f"[Notification] Гонщик присоединился к команде")
    elif event_type == "DriverLeftTeam":
        logging.info(f"[Notification] Гонщик покинул команду")
    elif event_type == "TeamCreated":
        logging.info(f"[Notification] Новая команда создана: {data}")
    elif event_type == "RaceScheduled":
        logging.info(f"[Notification] Гонка запланирована: {data}")
    elif event_type == "TrackAdded":
        logging.info(f"[Notification] Трек добавлен: {data}")
    elif event_type == "RaceFinished":
        logging.info(f"[Notification] Гонка завершена: {data}")
    else:
        logging.info(f"[Notification] Неизвестное событие: {event_type}")
    
    EVENTS_PROCESSED.inc()
