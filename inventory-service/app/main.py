from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Query
from typing import AsyncGenerator, List, Optional
import asyncio
import logging

from sqlmodel import Session
from app.db import create_db_and_tables , get_session
from app.crud import get_all_inventory_items, get_inventory_by_id
from app.models.inventory_model import InventoryItem
from app.consumer import consume

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("LifeSpan Event..")
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
    
