import aio_pika
import asyncio
import json
from handlers import handle_event
from config import settings, logging

async def start_consuming():
    connection = await aio_pika.connect_robust(settings.rabbitmq_url)
    channel = await connection.channel()
    exchange = await channel.declare_exchange("events", aio_pika.ExchangeType.TOPIC)

    queue = await channel.declare_queue("notifications", durable=True)
    await queue.bind(exchange, routing_key="#")
    print("Notifications consumer started, waiting for messages...")
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                try:
                    payload = json.loads(message.body)
                    event_type = message.routing_key.split(".")[-1]
                    await handle_event(event_type, payload)
                except Exception as e:
                    logging.exception("Failed to handle message")
