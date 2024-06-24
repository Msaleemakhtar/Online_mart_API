from aiokafka import AIOKafkaProducer
from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Query
from typing import AsyncGenerator, List, Optional
import asyncio
from app import product_pb2
import logging

from sqlmodel import Session
from app.db import create_db_and_tables , get_session
from app.crud import get_all_products, get_product_by_id, get_filtered_products, create_product_rating,get_ratings_for_product, update_product_rating, get_average_rating
from app.producer import get_kafka_producer, create_kafka_topic
from app.models.product_model import ProductUpdate, Product, ProductRating, ProductRatingCreate
from app.consumer import consume
from app import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("LifeSpan Event..")
    await create_kafka_topic()
    create_db_and_tables()
    loop = asyncio.get_event_loop()
    consume_task = loop.create_task(consume())
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





# Add product to Kafka
@app.post("/orders", tags=["Kafka_Operations"])
async def create_product(product: ProductUpdate, producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    product_message = product_pb2.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        expiry=product.expiry,
        brand=product.brand,
        weight=product.weight,
        category_id=product.category_id,
        sku=product.sku,
        stock_quantity=product.stock_quantity,
        reorder_level=product.reorder_level,
        meta_title=product.meta_title,
        meta_description=product.meta_description,
        meta_keywords=product.meta_keywords,
        operation=product_pb2.OperationType.CREATE
    )

    await producer.send_and_wait(settings.KAFKA_PRODUCT_TOPIC, product_message.SerializeToString())
    return {"message": "order created successfully"}

# Update order in Kafka
@app.put("/orders/{order_id}", tags=["Kafka_Operations"])
async def update_product(product_id: int, product: ProductUpdate, producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    product_message = product_pb2.Product(
        id=product_id,  # Include the ID for update
        name=product.name,
        description=product.description,
        price=product.price,
        expiry=product.expiry,
        brand=product.brand,
        weight=product.weight,
        category_id=product.category_id,
        sku=product.sku,
        stock_quantity=product.stock_quantity,
        reorder_level=product.reorder_level,
        meta_title=product.meta_title,
        meta_description=product.meta_description,
        meta_keywords=product.meta_keywords,
        operation=product_pb2.OperationType.UPDATE
    )

    await producer.send_and_wait(settings.KAFKA_PRODUCT_TOPIC, product_message.SerializeToString())
    return {"message": "Order updated successfully"}

# Delete order from Kafka
@app.delete("/orders/{order_id}", tags=["Kafka_Operations"])
async def delete_product(product_id: int, producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    product_message = product_pb2.Product(
        id=product_id,  # Ensure ID is set for deletion
        operation=product_pb2.OperationType.DELETE
    )

    await producer.send_and_wait(settings.KAFKA_PRODUCT_TOPIC, product_message.SerializeToString())
    return {"message": "Product deleted successfully"}



# Get all orders from database
@app.get("/all_orders", response_model=List[Product], tags=["Database_Operations"])
def get_products(session: Annotated[Session, Depends(get_session)]):
    return get_all_products(session)

# Get all orders from database
@app.get("/orders/{order_id}", response_model=Product, tags=["Database_Operations"])
def get_single_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
    """ Get a single product by ID"""
    try:
        return get_product_by_id(product_id=product_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
