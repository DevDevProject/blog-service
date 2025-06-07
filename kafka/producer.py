import json
from aiokafka import AIOKafkaProducer
import asyncio

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "company.blog_count.increase"

producer = None

async def init_producer():
    global producer
    if producer is None:
        producer = AIOKafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        await producer.start()

async def send_company_update(company_name: str):
    await init_producer()
    message = {
        "company_name": company_name,
        "action": "increase_blog_count"
    }
    await producer.send_and_wait(KAFKA_TOPIC, message)
