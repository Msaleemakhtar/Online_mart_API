from aiokafka import AIOKafkaConsumer
import logging
import asyncio
from fastapi import HTTPException


from app import settings
from app import order_pb2
from app.models.order_model import  OrderCreate
from app import user_pb2, product_pb2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory caches
user_data = {}
product_data = {}

# Background task to consume and update caches
async def consume_user_and_product_data():
    consumer = AIOKafkaConsumer(
        "user", "product",
        bootstrap_servers=settings.BOOTSTRAP_SERVER,
        group_id=settings.KAFKA_CONSUMER_GROUP_ID_FOR_ORDER,
       auto_offset_reset='earliest'
    )
    await consumer.start()
 
    try:
        async for msg in consumer:
            if msg.topic == "user":
                logger.info(f"Received message from {settings.KAFKA_USER_TOPIC}")
                user_response = user_pb2.UserOutput()
                user_response.ParseFromString(msg.value)
                user_data[user_response.id] = user_response
                logger.info(f"Updated user_data: {user_response}")
                #user_data_event.set()  # Signal that user data is available
                print(user_response.id)

            elif msg.topic == "product":
                logger.info(f"Received message from {settings.KAFKA_PRODUCT_TOPIC}")
                product_response = product_pb2.Product()
                product_response.ParseFromString(msg.value)
                product_data[product_response.id] = product_response
                logger.info(f"product_data: {product_response}")
                #product_data_event.set()  # Signal that product data is available
    except Exception as e:
        logger.error(f"Error consuming messages: {e}")
    finally:
        await consumer.stop()

print("user data: ", user_data)
print("product data: ", product_data)

