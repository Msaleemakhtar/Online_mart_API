from app import settings
from aiokafka import AIOKafkaConsumer
from app.gmail import send_email
from app import user_pb2
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)







async def consume_users():
    while True:
        try:
            consumer = AIOKafkaConsumer(
                settings.KAFKA_USER_TOPIC,
                bootstrap_servers=settings.BOOTSTRAP_SERVER,
                group_id=settings.KAFKA_CONSUMER_GROUP_ID_FOR_NOTIFICATION,
                auto_offset_reset='latest'
            )
            await consumer.start()
            try:
                async for msg in consumer:
                    user_operation = user_pb2.UserOperation()
                    user_operation.ParseFromString(msg.value)
                    user = user_operation.user
                    logger.info(f"Received user: {user.email}")
                    await handle_user_event(user)
            finally:
                await consumer.stop()
        except Exception as e:
            logger.error(f"Error consuming users: {e}")
            await asyncio.sleep(5)  # wait before restarting the consumer

# async def consume_users():
#     consumer = AIOKafkaConsumer(
#         settings.KAFKA_USER_TOPIC,
#         bootstrap_servers=settings.BOOTSTRAP_SERVER,
#         group_id=settings.KAFKA_CONSUMER_GROUP_ID_FOR_NOTIFICATION,
#         auto_offset_reset='latest')
#     await consumer.start()
#     try:
#         async for msg in consumer:
#             user_operation = user_pb2.UserOperation()
#             user_operation.ParseFromString(msg.value)
#             user = user_operation.user
#             logger.info(f"Received user: {user.email}")
#             handle_user_event(user)
#     finally:
#         await consumer.stop()


def handle_user_event(user):
    subject = "🎉 Welcome to Online Mart! Your Journey Begins Now 🚀"
    
    body = (
        "Dear {name},\n\n"
        "We're thrilled to welcome you to Online Mart, your one-stop destination for all things shopping! 🛒\n\n"
        "As a token of our appreciation for joining us, we're offering you an exclusive welcome offer. Check your inbox for special deals and updates tailored just for you.\n\n"
        "Start exploring our wide range of products and enjoy a seamless shopping experience. If you have any questions or need assistance, our support team is here to help!\n\n"
        "Thank you for choosing Online Mart. We can't wait to see you make the most of your new account!\n\n"
        "Best regards,\n"
        "The Online Mart Team\n\n"
        "P.S. Stay tuned for exciting updates and offers!"
    ).format(name=user.full_name)
    
    send_email(
        subject=subject,
        recipient=str(user.email),
        body=body
    )

