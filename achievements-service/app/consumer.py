import aio_pika
import json
from db import get_async_session, init_db
from achievements import update_achievements

async def consume_events():
    await init_db()
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    channel = await connection.channel()

    exchange = await channel.declare_exchange("events", aio_pika.ExchangeType.TOPIC)
    queue = await channel.declare_queue("achievements_queue", durable=True)
    await queue.bind(exchange, routing_key="race.RaceFinished")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                payload = json.loads(message.body)
                results = payload["results"]

                async with get_async_session() as session: 
                    await update_achievements(session, results)