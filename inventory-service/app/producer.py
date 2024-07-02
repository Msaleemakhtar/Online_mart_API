import asyncio
from aiokafka import AIOKafkaProducer
from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from aiokafka.errors import TopicAlreadyExistsError, KafkaConnectionError
from app import settings

MAX_RETRIES = 5
RETRIES_INTERVAL = 10

async def create_kafka_topic():
    admin_client = AIOKafkaAdminClient(bootstrap_servers=settings.BOOTSTRAP_SERVER)
    retries = 0
    while retries < MAX_RETRIES:
        try:
            await admin_client.start()
            topic_list = [NewTopic(name=settings.KAFKA_INVENTORY_TOPIC, num_partitions=1, replication_factor=1)]
            try:
                await admin_client.create_topics(topic_list, validate_only=False)
                print("Topic created successfully")
            except TopicAlreadyExistsError:
                print("Topic already exists")
            finally:
                await admin_client.close()
                return
        except KafkaConnectionError:
            print(f"Failed to connect to Kafka. Retrying in {RETRIES_INTERVAL} seconds...")
            await asyncio.sleep(RETRIES_INTERVAL)
            retries += 1
    raise Exception("Failed to create Kafka topic after multiple retries")


async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers=settings.BOOTSTRAP_SERVER)
    await producer.start()
   
    try:
        yield producer
    finally:
        await producer.stop()
   
