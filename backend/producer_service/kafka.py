from aiokafka import AIOKafkaProducer
import asyncio
from config import settings

producer: AIOKafkaProducer | None = None

async def init_kafka():
    global producer
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
    )
    await producer.start()
    print("✅ Kafka producer started")

async def close_kafka():
    if producer:
        await producer.stop()
        print("🛑 Kafka producer stopped")

async def send_to_kafka(message: bytes):
    if not producer:
        raise RuntimeError("Kafka producer is not initialized")
    await producer.send_and_wait(settings.KAFKA_TOPIC, message)
    print(f"📤 Message sent to Kafka: {message}")
