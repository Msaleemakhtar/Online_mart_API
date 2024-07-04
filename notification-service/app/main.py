import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.kafka_consumer import consume_users, consume_orders




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("LifeSpan Event..")
    #create_db_and_tables()
    loop = asyncio.get_event_loop()
    order_task= loop.create_task(consume_orders())
    user_task = loop.create_task(consume_users())
    yield
   




description = f"""
Notification Microservice API allows you to manage notification effectively. 
With this microservice, you can:
- Create, update, retrieve, and delete notification.
- Used protobuf for serialization and deserialization of data.

Utilize Kafka for asynchronous creation, updating, and deletion of notification.
"""


app = FastAPI(lifespan=lifespan,
    title="Notification-service",
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
            "url": "http://127.0.0.1:8010", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ]
)

@app.get("/")
async def root():
    return {"Notification -service"}

