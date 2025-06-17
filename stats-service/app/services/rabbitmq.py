import json
import aio_pika
from typing import Any


RABBITMQ_URL = "amqp://guest:guest@rabbitmq/"

async def publish_event(routing_key: str, event_data: dict[str, Any]) -> None:
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()

        exchange = await channel.declare_exchange("events", aio_pika.ExchangeType.TOPIC)

        message = aio_pika.Message(
            body=json.dumps(event_data).encode(),
            content_type="application/json",
            headers={"event_type": routing_key.split(".")[-1]},
        )

        await exchange.publish(
            message,
            routing_key=routing_key
        )
