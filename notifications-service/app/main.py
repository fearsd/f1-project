import asyncio
import threading
from consumer import start_consuming
from prometheus_client import start_http_server

def start_metrics_server():
    start_http_server(8000)

async def main():
    threading.Thread(target=start_metrics_server, daemon=True).start()
    await start_consuming()

if __name__ == "__main__":
    asyncio.run(main())
