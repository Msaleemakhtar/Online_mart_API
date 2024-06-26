from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from app import user_pb2, product_pb2, order_pb2
from app.models.order_model import Order, OrderItem
from sqlmodel import Session, select
from app.db import get_session
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def consume_and_process_orders():
    consumer = AIOKafkaConsumer(
        settings.KAFKA_PRODUCT_TOPIC, settings.KAFKA_USER_TOPIC,settings.KAFKA_ORDER_TOPIC,
        bootstrap_servers=settings.BOOTSTRAP_SERVER,
        group_id=settings.KAFKA_CONSUMER_GROUP_ID_FOR_ORDER
    )
    producer = AIOKafkaProducer(bootstrap_servers=settings.bootstrap_servers)
    await consumer.start()
    await producer.start()
    user_data = {}
    product_data = {}
    try:
        async for msg in consumer:
            if msg.topic == "user-data-topic":
                user_response = user_pb2.UserResponse()
                user_response.ParseFromString(msg.value)
                user_data[user_response.user_id] = user_response
            
            elif msg.topic == "product-data-topic":
                product_response = product_pb2.ProductResponse()
                product_response.ParseFromString(msg.value)
                product_data[product_response.product_id] = product_response
            
            elif msg.topic == "order-topic":
                order_operation = order_pb2.OrderOperation()
                order_operation.ParseFromString(msg.value)
                
                with Session(get_db()) as session:
                    if order_operation.operation == order_pb2.OperationType.CREATE:
                        # Handle Order Creation
                        new_order = Order(
                            id=UUID(order_operation.order.id),
                            user_id=order_operation.order.user_id,
                            total_price=order_operation.order.total_price,
                            status=order_operation.order.status,
                            created_at=order_operation.order.created_at
                        )
                        session.add(new_order)
                        session.commit()
                        logger.info(f"Order created: {new_order.id}")

                    elif order_operation.operation == order_pb2.OperationType.UPDATE:
                        # Handle Order Update
                        order = session.get(Order, UUID(order_operation.order.id))
                        if order:
                            order.user_id = order_operation.order.user_id
                            order.total_price = order_operation.order.total_price
                            order.status = order_operation.order.status
                            order.updated_at = datetime.utcnow()
                            session.add(order)
                            session.commit()
                            logger.info(f"Order updated: {order.id}")
                        else:
                            logger.warning(f"Order not found: {order_operation.order.id}")

                    elif order_operation.operation == order_pb2.OperationType.DELETE:
                        # Handle Order Deletion
                        order = session.get(Order, UUID(order_operation.order.id))
                        if order:
                            session.delete(order)
                            session.commit()
                            logger.info(f"Order deleted: {order.id}")
                        else:
                            logger.warning(f"Order not found: {order_operation.order.id}")

    finally:
        await consumer.stop()
        await producer.stop()
