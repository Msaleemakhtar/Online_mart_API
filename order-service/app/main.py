import asyncio
import logging
from app import order_pb2
from typing import Annotated
from uuid import uuid4, UUID
from aiokafka import AIOKafkaProducer
from contextlib import asynccontextmanager
from typing import AsyncGenerator, List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query

from app import settings
from sqlmodel import Session
from app.models.order_model import Order, OrderItem, OrderItemCreate, OrderCreate, OrderUpdate, OrderStatus
from app.consumer import consume_and_process_orders
from app.db import create_db_and_tables , get_session
from app.producer import get_kafka_producer, create_kafka_topic
#from app.crud import get_all_products, get_product_by_id
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp




def timestamp_from_datetime(dt: datetime) -> Timestamp:
    """Helper function to convert datetime to Timestamp object."""
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("LifeSpan Event..")
    await create_kafka_topic()
    create_db_and_tables()
    loop = asyncio.get_event_loop()
    consume_task = loop.create_task(consume_and_process_orders())
    try:
        yield
    finally:
        consume_task.cancel()
        try:
            await consume_task
        except asyncio.CancelledError:
            logger.warning("Consume task was cancelled during shutdown.")
        except Exception as e:
            logger.error(f"Unexpected error during shutdown: {e}")





description = f"""
Order Microservice API allows you to manage orders and their ratings effectively. 
With this microservice, you can:
- Create, update, retrieve, and delete orders.
- Used protobuf for serialization and deserialization of data.

Utilize Kafka for asynchronous creation, updating, and deletion of products.
"""


app = FastAPI(lifespan=lifespan,
    title="Product-service",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Muhammad Saleem Akhtar",
        "email": "saleemakhtar864@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT",
    },
     servers=[
        {
            "url": "http://127.0.0.1:8009", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ]
)

@app.get("/")
async def root():
    return {"Order-service"}




@app.post("/orders/", response_model=Order)
async def create_order(order_create: OrderCreate, db: Annotated[Session , Depends(get_session)], producer: AIOKafkaProducer = Depends(get_kafka_producer)):

    try:
        # Create the order in the database
        order = Order(user_id=order_create.user_id, status=OrderStatus.PENDING)
        db.add(order)
        db.commit()
        db.refresh(order)

        # Create order items and associate with the order
        order_items = []
        for item in order_create.items:
            order_item = OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity)
            db.add(order_item)
            order_items.append(order_item)

        # Commit all order items
        db.commit()

        # Refresh order items to get IDs
        for order_item in order_items:
            db.refresh(order_item)

        # Update the order with its items
        order.items = order_items

        # Prepare protobuf message
        order_message = order_pb2.OrderOperation(
            operation=order_pb2.OperationType.CREATE,
            order=order_pb2.Order(
                id=str(order.id),
                user_id=order.user_id,
                total_price=float(order.total_price),
                status=order_pb2.OrderStatus.PENDING,
                created_at=timestamp_from_datetime(order.created_at),
                updated_at=timestamp_from_datetime(order.updated_at),
                items=[
                    order_pb2.OrderItem(
                        id=str(item.id),
                        order_id=str(order.id),
                        product_id=item.product_id,
                        quantity=item.quantity,
                        created_at=timestamp_from_datetime(item.created_at),
                        updated_at=timestamp_from_datetime(item.updated_at)
                    ) for item in order_items
                ]
            )
        )

        # Serialize the protobuf message
        order_message_serialized = order_message.SerializeToString()

        # Send protobuf message to Kafka
        await producer.send_and_wait(settings.KAFKA_ORDER_TOPIC, order_message_serialized)

        return order

    except Exception as e:
        # Handle exceptions (rollback, logging, etc.)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    finally:
        # Always close the session to release resources
        db.close()






# @app.put("/orders/", response_model=Order)
# async def update_order(order_update: OrderUpdate, db:Annotated[Session, Depends(get_session)], producer: AIOKafkaProducer = Depends(get_kafka_producer)):
#     order = db.get(Order, order_update.id)
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
    
#     if order_update.user_id:
#         order.user_id = order_update.user_id
#     if order_update.status:
#         order.status = order_update.status
#     order.updated_at = datetime.now()
#     db.commit()
#     db.refresh(order)
    
#     if order_update.items:
#         for item in order_update.items:
#             order_item = db.exec(select(OrderItem).where(OrderItem.order_id == order.id, OrderItem.product_id == item.product_id)).first()
#             if order_item:
#                 order_item.quantity = item.quantity
#                 order_item.updated_at = datetime.now()
#             else:
#                 order_item = OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity)
#                 db.add(order_item)
#             db.commit()
#             db.refresh(order_item)
    
#     order_message = order_pb2.OrderOperation(
#         operation=order_pb2.OperationType.UPDATE,
#         order=order_pb2.Order(
#             id=str(order.id),
#             user_id=order.user_id,
#             total_price=order.total_price,
#             status=order_pb2.OrderStatus.Value(order.status.upper()),
#             created_at=order.created_at.isoformat(),
#             updated_at=order.updated_at.isoformat(),
#             items=[order_pb2.OrderItem(
#                 id=str(item.id),
#                 order_id=str(order.id),
#                 product_id=item.product_id,
#                 quantity=item.quantity,
#                 created_at=item.created_at.isoformat(),
#                 updated_at=item.updated_at.isoformat()
#             ) for item in order.items]
#         )
#     )
#     await producer.send_and_wait(settings.KAFKA_ORDER_TOPIC, order_message.SerializeToString())
#     return order

# @app.delete("/orders/{order_id}", response_model=dict)
# async def delete_order(order_id: UUID, db:Annotated[Session, Depends(get_session)], producer: AIOKafkaProducer = Depends(get_kafka_producer)):
#     order = db.get(Order, order_id)
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
    
#     db.delete(order)
#     db.commit()
    
#     order_message = order_pb2.OrderOperation(
#         operation=order_pb2.OperationType.DELETE,
#         order=order_pb2.Order(
#             id=str(order.id),
#             user_id=order.user_id,
#             total_price=order.total_price,
#             status=order_pb2.OrderStatus.Value(order.status.upper()),
#             created_at=order.created_at.isoformat(),
#             updated_at=order.updated_at.isoformat(),
#             items=[order_pb2.OrderItem(
#                 id=str(item.id),
#                 order_id=str(order.id),
#                 product_id=item.product_id,
#                 quantity=item.quantity,
#                 created_at=item.created_at.isoformat(),
#                 updated_at=item.updated_at.isoformat()
#             ) for item in order.items]
#         )
#     )
#     await producer.send_and_wait(settings.KAFKA_ORDER_TOPIC, order_message.SerializeToString())
#     return {"message": "Order deleted successfully"}