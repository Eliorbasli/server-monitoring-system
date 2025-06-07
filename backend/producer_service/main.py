import asyncio
from producer_service.kafka import init_kafka, close_kafka
from producer_service.worker import fetch_and_send
from producer_service.config import settings
from app.db.base import init_models

init_models()

async def main():
    await init_kafka()
    try:
        while True:
            await fetch_and_send()
            await asyncio.sleep(settings.POLL_INTERVAL)
    finally:
        await close_kafka()

if __name__ == "__main__":
    asyncio.run(main())
