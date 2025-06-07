import json
from aiokafka import AIOKafkaProducer

from dotenv import load_dotenv
import os

load_dotenv()

KAFKA_TOPIC = "company.blog_count.increase"
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

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
