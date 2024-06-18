from typing import Optional, Annotated
from sqlmodel import Session

from fastapi import Depends, HTTPException, FastAPI, Form
from fastapi.security import OAuth2PasswordRequestForm

from uuid import UUID
from contextlib import asynccontextmanager



from app.service import user_login_for_access_token, user_signup, get_gpt_token, create_access_token, get_current_user
from app.models import UserRegister, GptToken, UserOutput, LoginResponse, UserRead
from app.core.config_db import get_db, create_db_and_tables
from app.core.utils import get_current_user_id




@asynccontextmanager
async def create_table(app:FastAPI):
    create_db_and_tables()
    yield

app:FastAPI = FastAPI(
    lifespan=create_table,
      title="OAuth Server",
    description="Multi-User Todo-App OAuth_Microservice",
    version="1.0.0",
    contact={
        "name": "Muhammad Saleem Akhtar",
        "email": "saleemakhtar864@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    },
    docs_url="/api/docs"
)


# signup users 
@app.post("/api/oauth/signup", response_model=UserOutput, tags=["OAuth2 Authentication"])
async def signup(user_data:UserRegister, db:Annotated[Session, Depends(get_db)]):
    
    return await user_signup(user_data, db)

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
@app.get("/api/user/me", tags=["User"])
async def get_user_by_id(user_id: Annotated[UUID, Depends(get_current_user_id)]):
    return user_id

@app.get("/api/user/me")
async def read_users(current_user: Annotated[str, Depends(get_current_user)]):
    return current_user