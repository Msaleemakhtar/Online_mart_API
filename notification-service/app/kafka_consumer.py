from app import settings
from aiokafka import AIOKafkaConsumer
from app.gmail import send_email
from app import order_pb2, user_pb2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def consume_orders():
    consumer = AIOKafkaConsumer(
        settings.KAFKA_ORDER_TOPIC,
        bootstrap_servers=settings.BOOTSTRAP_SERVER,
        group_id=settings.KAFKA_CONSUMER_GROUP_ID_FOR_NOTIFICATION
    )
    await consumer.start()
    try:
        async for msg in consumer:
            order_operation = order_pb2.OrderOperation()
            order_operation.ParseFromString(msg.value)
            handle_order_event(order_operation)
    finally:
        await consumer.stop()

async def consume_users():
    consumer = AIOKafkaConsumer(
        settings.KAFKA_USER_TOPIC,
        bootstrap_servers=settings.BOOTSTRAP_SERVER,
        group_id=settings.KAFKA_CONSUMER_GROUP_ID_FOR_NOTIFICATION
    )
    await consumer.start()
    try:
        async for msg in consumer:
            user_operation = user_pb2.UserOperation()
            user_operation.ParseFromString(msg.value)
            user = user_operation.user
            logger.info(f"Received user: {user.email}")
            handle_user_event(user)
    finally:
        await consumer.stop()

def handle_order_event(order_operation):
    if order_operation.operation == order_pb2.OperationType.CREATE:
        send_email(
            subject="Order Created",
            recipient="saleemakhtar864@gmail.com",
            body=f"Your order {order_operation.order.id} has been created."
        )
    elif order_operation.operation == order_pb2.OperationType.UPDATE:
        send_email(
            subject="Order Updated",
            recipient="saleemakhtar864@gmail.com",
            body=f"Your order {order_operation.order.id} has been updated."
        )
    elif order_operation.operation == order_pb2.OperationType.DELETE:
        send_email(
            subject="Order Deleted",
            recipient="saleemakhtar864@gmail.com",
            body=f"Your order {order_operation.order.id} has been deleted."
        )

def handle_user_event(user):
    send_email(
        subject="Welcome!",
        recipient=str(user.email),
        body="Welcome to Online Mart API"
    )

