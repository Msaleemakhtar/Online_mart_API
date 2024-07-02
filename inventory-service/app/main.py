
from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlmodel import Session, select
from datetime import datetime

from app.inventory_pb2 import InventoryOperation, InventoryItem as InventoryItemProto, OperationType as InventoryOperationType
from app.producer import get_kafka_producer, create_kafka_topic
from aiokafka import AIOKafkaProducer
from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Query
from typing import AsyncGenerator, List, Optional
import asyncio
import logging
from app import settings
from app.db import create_db_and_tables , get_session
from app.crud import get_all_inventory_items, get_inventory_by_id, convert_inventory_item_to_proto
from app.models.inventory_model import InventoryItem
from app.consumer import consume

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("LifeSpan Event..")
    create_db_and_tables()
    await create_kafka_topic()
    loop = asyncio.get_event_loop()
    consume_task = loop.create_task(consume())
    yield
    # finally:
    #     consume_task.cancel()
    #     try:
    #         await consume_task
    #     except asyncio.CancelledError:
    #         logger.warning("Consume task was cancelled during shutdown.")
    #     except Exception as e:
    #         logger.error(f"Unexpected error during shutdown: {e}")





description = f"""
Microservice API allows you to manage Inventory.

Used protobuf for serialization and deserialization of data.

Utilize Kafka for asynchronous creation, updating, and deletion of Inventory.
"""


app = FastAPI(lifespan=lifespan,
    title="Inventory-service",
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
            "url": "http://127.0.0.1:8008", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ]
)

@app.get("/")
async def root():
    return {"Inventory-service"}


# add product to inventory
@app.post("/inventory_items/", response_model=InventoryItem)
async def create_inventory_item(item: InventoryItem, db:Annotated[ Session,Depends(get_session)], producer:Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    db.add(item)
    db.commit()
    db.refresh(item)
    
    # Produce inventory operation to Kafka
    inventory_operation = InventoryOperation(
        operation=InventoryOperationType.CREATE,
        inventory_item=convert_inventory_item_to_proto(item)
    )
    # Send protobuf message to Kafka
    await producer.send_and_wait(settings.KAFKA_INVENTORY_TOPIC, inventory_operation.SerializeToString())
    
    return item


#Update inventory
@app.put("/inventory_items/{item_id}", response_model=InventoryItem)
async def update_inventory_item(item_id: int, item: InventoryItem, db:Annotated[Session, Depends(get_session)], producer:Annotated[ AIOKafkaProducer, Depends(get_kafka_producer)]):
    existing_item = db.exec(select(InventoryItem).where(InventoryItem.id == item_id)).first()
    if not existing_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    if existing_item:
        if item.product_id:
            existing_item.product_id = item.product_id
        if item.stock_quantity:
            existing_item.stock_quantity = item.stock_quantity
        if item.reorder_level:
            existing_item.reorder_level = item.reorder_level 
        
    existing_item.updated_at = datetime.now()
    db.commit()
    db.refresh(existing_item)
    
    # Produce inventory operation to Kafka
    inventory_operation = InventoryOperation(
        operation=InventoryOperationType.UPDATE,
        inventory_item=convert_inventory_item_to_proto(existing_item)
    )
    # Send protobuf message to Kafka
    await producer.send_and_wait(settings.KAFKA_INVENTORY_TOPIC, inventory_operation.SerializeToString())
    
    return existing_item



#delete product from inventory
@app.delete("/inventory_items/{item_id}", response_model=InventoryItem)
async def delete_inventory_item(item_id: int, db:Annotated[ Session, Depends(get_session)], producer: AIOKafkaProducer = Depends(get_kafka_producer)):
    existing_item = db.exec(select(InventoryItem).where(InventoryItem.id == item_id)).first()
    if not existing_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    db.delete(existing_item)
    db.commit()
    
    # Produce inventory operation to Kafka
    inventory_operation = InventoryOperation(
        operation=InventoryOperationType.DELETE,
        inventory_item=convert_inventory_item_to_proto(existing_item)
    )
    # Send protobuf message to Kafka
    await producer.send_and_wait(settings.KAFKA_INVENTORY_TOPIC, inventory_operation.SerializeToString())
    
    return existing_item





@app.get("/all_inventory", response_model=List[InventoryItem], tags=["Database_Operations"])
def get_products(session: Annotated[Session, Depends(get_session)]):
    return get_all_inventory_items(session)


@app.get("/inventory/{product_id}", response_model=InventoryItem, tags=["Database_Operations"])
def get_single_product(product_id: int, session: Annotated[Session, Depends(get_session)]):
   
    try:
        return get_inventory_by_id(product_id=product_id, session=session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


