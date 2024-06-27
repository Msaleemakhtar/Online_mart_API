import asyncio
import logging
from app import order_pb2
from typing import Annotated
from uuid import uuid4, UUID
from aiokafka import AIOKafkaProducer
from contextlib import asynccontextmanager
from typing import AsyncGenerator, List, Optional
from fastapi import FastAPI, Depends, HTTPException

from app import settings
from sqlmodel import Session
from app.models.order_model import Order, OrderItem, OrderItemCreate, OrderCreate, OrderUpdate, OrderStatus
from app.product_consumer import product_consume
from app.user_consumer import user_consume
from app.db import create_db_and_tables , get_session
from app.producer import get_kafka_producer, create_kafka_topic
#from app.crud import get_all_products, get_product_by_id
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("LifeSpan Event..")
    await create_kafka_topic()
    create_db_and_tables()
    loop = asyncio.get_event_loop()
    product_consume_task = loop.create_task(product_consume())
    user_consume_task = loop.create_task(user_consume())
    try:
        yield
    finally:
        product_consume_task.cancel()
        user_consume_task.cancel()
        try:
            await product_consume_task
            await user_consume_task
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
    title="Order-service",
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
async def create_order(order_create: OrderCreate, db: Annotated[Session, Depends(get_session)],
                       producer: AIOKafkaProducer = Depends(get_kafka_producer)):
    
  
    try:
  
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
               
                items=[
                    order_pb2.OrderItem(
                        id=str(item.id),
                        order_id=str(order.id),
                        product_id=item.product_id,
                        quantity=item.quantity,
                        
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