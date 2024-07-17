import asyncio
import logging
from typing import Annotated
from uuid import uuid4, UUID
from datetime import datetime
from aiokafka import AIOKafkaProducer
from contextlib import asynccontextmanager
from typing import AsyncGenerator, List, Optional
from fastapi import FastAPI, Depends, HTTPException,Path
from google.protobuf.timestamp_pb2 import Timestamp

from app import settings
from app import order_pb2
from sqlmodel import Session, select
from app.producer import get_kafka_producer, create_kafka_topic
from app.user_consumer import user_consume
from app.inv_consumer import inventory_consume
from app.db import create_db_and_tables , get_session
from app.models.order_model import (User, InventoryItem, Order, OrderItem,
                                OrderItemCreate, OrderCreate, OrderUpdate, OrderStatus)
from app.crud import get_users, get_inventory, create_order, get_orders, delete_order, update_order


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("LifeSpan Event..")
    await create_kafka_topic()
    create_db_and_tables()
    loop = asyncio.get_event_loop()
    user_consume_task = loop.create_task(user_consume())
    inv_consume_task = loop.create_task(inventory_consume())
    yield
   




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
        ],
    root_path="/order-service",
    root_path_in_servers=True
)

@app.get("/")
async def root():
    return {"Order-service"}

#Get all users
@app.get("/users/", response_model=List[User])
async def get_all_users(db: Annotated[Session, Depends(get_session)]):
    users = await get_users(db)
    return users

#Get all products
@app.get("/products/", response_model=List[InventoryItem])
async def get_all_inventory(db: Annotated[Session, Depends(get_session)]):
    products = await get_inventory(db)
    return products

#Get all orders
@app.get("/orders/", response_model=List[Order]) 
async def get_all_orders(db: Annotated[Session, Depends(get_session)]):
    orders = await get_orders(db)
    return orders

@app.post("/orders/", response_model=Order)
async def generate_orer(order_create: OrderCreate, db: Annotated[Session, Depends(get_session)],
                       producer:Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    return await create_order(order_create, db, producer)
  
  
# Delete order and send to kafka
@app.delete("/orders/{order_id}")
async def delete_order_by_id(order_id:str,  db: Annotated[Session, Depends(get_session)],
                       producer:Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    
    return await delete_order(order_id, db, producer)

#update order and send to kafka
@app.put("/orders/{order_id}")
async def update_order_by_id(order_id:str, order_update:OrderUpdate, db: Annotated[Session, Depends(get_session)],
                       producer:Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    return await update_order(order_id, order_update, db, producer)