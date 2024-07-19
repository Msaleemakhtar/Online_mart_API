from app import settings
from aiokafka import AIOKafkaConsumer
from app.gmail import send_email
from app import order_pb2
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




async def consume_orders():
    while True:
        try:
            consumer = AIOKafkaConsumer(
                settings.KAFKA_ORDER_TOPIC,
                bootstrap_servers=settings.BOOTSTRAP_SERVER,
                group_id=settings.KAFKA_CONSUMER_GROUP_ID_FOR_NOTIFICATION,
                auto_offset_reset='latest'
            )
            await consumer.start()
            try:
                async for msg in consumer:
                    order_operation = order_pb2.OrderOperation()
                    order_operation.ParseFromString(msg.value)
                    await handle_order_event(order_operation)
            finally:
                await consumer.stop()
        except Exception as e:
            logger.error(f"Error consuming orders: {e}")
            await asyncio.sleep(5)  # wait before restarting the consumer

# async def consume_orders():
#     consumer = AIOKafkaConsumer(
#         settings.KAFKA_ORDER_TOPIC,
#         bootstrap_servers=settings.BOOTSTRAP_SERVER,
#         group_id=settings.KAFKA_CONSUMER_GROUP_ID_FOR_NOTIFICATION,
#         auto_offset_reset='latest')
#     await consumer.start()
#     try:
#         async for msg in consumer:
#             order_operation = order_pb2.OrderOperation()
#             order_operation.ParseFromString(msg.value)
#             handle_order_event(order_operation)
#     finally:
#         await consumer.stop()


# def handle_order_event(order_operation):
#     if order_operation.operation == order_pb2.OperationType.CREATE:
#         send_email(
#             subject="Order Created",
#             recipient=order_operation.order.user_email,
#             body=f"Your order {order_operation.order.id} has been created."
#         )
#     elif order_operation.operation == order_pb2.OperationType.UPDATE:
#         send_email(
#             subject="Order Updated",
#             recipient=order_operation.order.user_email,
#             body=f"Your order {order_operation.order.id} has been updated."
#         )
#     elif order_operation.operation == order_pb2.OperationType.DELETE:
#         send_email(
#             subject="Order Deleted",
#             recipient=order_operation.order.user_email,
#             body=f"Your order {order_operation.order.id} has been deleted."
#         )
def handle_order_event(order_operation):
    order_id = order_operation.order.id
    user_email = order_operation.order.user_email

    if order_operation.operation == order_pb2.OperationType.CREATE:
        subject = "🎉 Your Order Has Been Successfully Created! 🛒"
        body = (
            f"Hello there!\n\n"
            f"Great news! Your order #{order_id} has been successfully created. 🎉\n\n"
            f"We're excited to start processing your order and will keep you updated on its progress.\n\n"
            f"Here's a summary of your order:\n"
            f"Order ID: {order_id}\n"
            f"Status: Created\n\n"
            f"Thank you for shopping with us! If you have any questions or need assistance, feel free to reach out.\n\n"
            f"Best regards,\n"
            f"The Online Mart Team\n\n"
            f"P.S. Stay tuned for more updates!"
        )

    elif order_operation.operation == order_pb2.OperationType.UPDATE:
        subject = "🔄 Your Order Has Been Updated! 🚀"
        body = (
            f"Hello!\n\n"
            f"Your order #{order_id} has been updated. We wanted to keep you in the loop about the changes made to your order.\n\n"
            f"Here's a summary of the update:\n"
            f"Order ID: {order_id}\n"
            f"Status: Updated\n\n"
            f"Thank you for your patience and for choosing Online Mart. If you need any further assistance, we're here to help.\n\n"
            f"Best regards,\n"
            f"The Online Mart Team\n\n"
            f"P.S. Keep an eye out for more updates!"
        )

    elif order_operation.operation == order_pb2.OperationType.DELETE:
        subject = "❌ Your Order Has Been Deleted 🚫"
        body = (
            f"Dear Customer,\n\n"
            f"We're sorry to inform you that your order #{order_id} has been deleted. 😔\n\n"
            f"If this was done in error or if you have any questions, please contact our support team immediately.\n\n"
            f"Thank you for your understanding.\n\n"
            f"Best regards,\n"
            f"The Online Mart Team\n\n"
            f"P.S. We're here if you need us!"
        )

    send_email(
        subject=subject,
        recipient=user_email,
        body=body
    )

