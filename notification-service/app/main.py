import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.users_consumer import consume_users
from app.orders_consumer import consume_orders

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("LifeSpan Event..")
    loop = asyncio.get_event_loop()
    loop.create_task(consume_orders())
    loop.create_task(consume_users())
    yield

description = """
Notification Microservice API allows you to manage notifications effectively. 
With this microservice:
- Used protobuf for serialization and deserialization of data.
- Utilize Kafka for asynchronous creation, updating, and deletion of notifications.
"""

app = FastAPI(
    lifespan=lifespan,
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
            "url": "http://127.0.0.1:8010",  # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
    ],
    root_path="/notification-service",
    root_path_in_servers=True
)

@app.get("/")
async def root():
    return {"message": "Notification-service"}


