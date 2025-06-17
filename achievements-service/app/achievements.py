from models import DriverAchievement
from sqlalchemy.ext.asyncio import AsyncSession
from metrics import EVENTS_PROCESSED

async def update_achievements(session: AsyncSession, race_results: list[dict]):
    for result in race_results:
        driver_id = result["driver_id"]
        position = result["position"]

        achievement = await session.get(DriverAchievement, driver_id)
        if not achievement:
            achievement = DriverAchievement(driver_id=driver_id, total_races=0, total_wins=0, podiums=0, best_finish=None)

        achievement.total_races += 1
        if position == 1:
            achievement.total_wins += 1
        if position <= 3:
            achievement.podiums += 1
        if achievement.best_finish is None or position < achievement.best_finish:
            achievement.best_finish = position

        session.add(achievement)
    await session.commit()
    EVENTS_PROCESSED.inc()
