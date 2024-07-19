from typing import Optional, Annotated
from sqlmodel import Session
from fastapi import Depends, HTTPException, FastAPI, Form, status
from fastapi.security import  OAuth2PasswordRequestForm
from aiokafka import AIOKafkaProducer

from uuid import UUID
from contextlib import asynccontextmanager
from app import user_pb2
import logging

from app.core import settings
from app.service import user_login_for_access_token, user_signup, get_gpt_token, create_access_token, get_current_user
from app.models import UserRegister, GptToken, UserOutput, LoginResponse, UserRead
from app.core.config_db import get_db, create_db_and_tables
from app.core.utils import get_current_user_id
from app.producer import get_kafka_producer, create_kafka_topic


from app.service import user_signup



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("LifeSpan Event..")
    await create_kafka_topic()
    create_db_and_tables()
    yield
    
    
    
    
description = f"""
User Microservice API allows you to manage users.
With this microservice, you can:
- Create, update, retrieve, and delete users.
- Used protobuf for serialization and deserialization of data.

Utilize Kafka for asynchronous creation, updating, and deletion of user.
"""


app = FastAPI(lifespan=lifespan,
    title="user-service",
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
            "url": "http://127.0.0.1:8006", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ],
    root_path="/user-service",
    root_path_in_servers=True

)




# signup users in db 
@app.post("/api/oauth/signup", response_model=UserOutput, tags=["OAuth2 Authentication"])
async def signup(user_data:UserRegister, db:Annotated[Session, Depends(get_db)],
                 producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    
    user = await user_signup(user_data, db)
    
     #Step 1: Serialize user data
    user_message = user_pb2.User(
        id=str(user.id),
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        email_verified=user.email_verified
    )
    user_operation_message = user_pb2.UserOperation(
        operation=user_pb2.OperationType.CREATE,
        user=user_message
    )
    serialized_data = user_operation_message.SerializeToString()

    # Step 2: Send serialized data to Kafka
    await producer.send_and_wait(settings.KAFKA_USER_TOPIC, serialized_data)
    return user

 





# # signup users in db and send to kafka
# @app.post("/api/oauth/signup-user", response_model=UserOutput, tags=["Kafka_Operation"])
# async def signup_user(user: Annotated[str, Depends(get_current_user)],
#                 producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    
#     #Step 1: Serialize user data
#     user_message = user_pb2.User(
#         id=str(user.id),
#         username=user.username,
#         full_name=user.full_name,
#         email=user.email,
#         email_verified=user.email_verified
#     )
#     user_operation_message = user_pb2.UserOperation(
#         operation=user_pb2.OperationType.CREATE,
#         user=user_message
#     )
#     serialized_data = user_operation_message.SerializeToString()

#     # Step 2: Send serialized data to Kafka
#     await producer.send_and_wait(settings.KAFKA_USER_TOPIC, serialized_data)
#     return user



# After sign up , using username and password to get access/refresh tokens
@app.post("/api/oauth/login",response_model=LoginResponse, tags=["OAuth2 Authentication"])
async def login_authorization(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
    try:
        return await user_login_for_access_token(form_data, db)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    

@app.post("/api/oauth/token", response_model=GptToken, tags=["OAuth2 Authentication"])
async def token_manager_outh_flow(
    grant_type:str = Form(...),
    refresh_token:Optional[str] = Form(None),
    code:Optional[str]=Form(None)):

    return await get_gpt_token(grant_type, refresh_token, code)



# Get the temp_code from user_id to implement Oauth for custom GPT
@app.get("/api/oauth/get_temp_code", tags=["OAuth2 Authentication"])
async def get_temp_code(user_id: UUID):
    code = create_access_token(data={"id":user_id})
    return {"code":code}



# This end point will take token and return user_id
@app.get("/api/user/user_id", tags=["User"])
async def get_user_by_id(user_id: Annotated[UUID, Depends(get_current_user_id)]):
    return user_id

@app.get("/api/user/me", tags=["User"])
async def read_users(current_user: Annotated[str, Depends(get_current_user)]):
    return current_user