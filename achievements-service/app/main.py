import asyncio
import threading
from consumer import consume_events
from prometheus_client import start_http_server
from db import init_db

def start_metrics_server():
    start_http_server(8000)

async def main():
    threading.Thread(target=start_metrics_server, daemon=True).start()
    await init_db()
    await consume_events()

if __name__ == "__main__":
    asyncio.run(main())
