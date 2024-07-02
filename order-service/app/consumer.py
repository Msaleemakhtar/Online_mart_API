import asyncio
import logging
from aiokafka import AIOKafkaConsumer
from app import settings
from app import user_pb2, inventory_pb2
from google.protobuf.json_format import MessageToDict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory caches
user_data = {}
inventory_cache = {}

async def consume_user_and_inventory_data():
    consumer = AIOKafkaConsumer(
        settings.KAFKA_USER_TOPIC, settings.KAFKA_INVENTORY_TOPIC,
        bootstrap_servers=settings.BOOTSTRAP_SERVER,
        group_id=settings.KAFKA_CONSUMER_GROUP_ID_FOR_ORDER,
        auto_offset_reset='earliest'
    )
    await consumer.start()

    try:
        async for msg in consumer:
            if msg.topic == settings.KAFKA_USER_TOPIC:
                logger.info(f"Received message from {settings.KAFKA_USER_TOPIC}")
                logger.info(f"Raw user message: {msg.value}")
                user_response = user_pb2.UserOutput()
                user_response.ParseFromString(msg.value)
                user_data[user_response.id] = MessageToDict(user_response)
                logger.info(f"Updated user_data: {user_data}")
            elif msg.topic == settings.KAFKA_INVENTORY_TOPIC:
                logger.info(f"Received message from {settings.KAFKA_INVENTORY_TOPIC}")
                logger.info(f"Raw inventory message: {msg.value}")
                inv_response = inventory_pb2.InventoryItem()
                inv_response.ParseFromString(msg.value)
                inventory_item = MessageToDict(inv_response)
                product_id = inventory_item['product_id']
                inventory_cache[product_id] = inventory_item
                logger.info(f"Updated inventory_cache: {inventory_cache}")
    except Exception as e:
        logger.error(f"Error consuming messages: {e}")
    finally:
        await consumer.stop()

