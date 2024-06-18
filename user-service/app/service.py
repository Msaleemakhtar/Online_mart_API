from sqlmodel import Session
from fastapi import Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from datetime import datetime, timedelta, timezone
from typing import Optional, Union, Annotated
from uuid import UUID
from jose import jwt, JWTError


from app.core import settings
from app.core.config_db import get_db
from app.core.utils import verify_password, create_refresh_token, credentials_exception, get_current_user_id, validate_refresh_token
from app.models import UserRegister, TokenData
from app.crud import db_get_user, db_signup_users, InvalidUserException


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = float(str(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
REFRESH_TOKEN_EXPIRE_MINUTES = float(str(settings.REFRESH_TOKEN_EXPIRE_MINUTES))



Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(db, username:str, password:str):
    try:
        user = db_get_user(db, username)
        if not user:
            raise False
        if not verify_password(password, user.hashed_password):
            raise False
        return user
    except InvalidUserException:
        raise


# create access token
def create_access_token(data:dict, expires_delta:Union[timedelta, None] = None):
   
   
    to_encode = data.copy()
    
    # If the Id present in date , convert it to string from uuid
    if 'id' in to_encode and isinstance(to_encode['id'], UUID):
        to_encode['id'] = str(to_encode['id'])

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=7)

    to_encode.update({"exp": expire})


    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=str(ALGORITHM))

    return encoded_jwt




async def get_current_user(token: Annotated[str, Depends(Oauth2_scheme)], db:Annotated[Session, Depends(get_db)]):
    print("tken", token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"})
    
    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[str(ALGORITHM)])
        username: Union[str, None] = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception
    
    user = db_get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user



async def user_login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], db:Annotated[Session, Depends(get_db)]):
    
   try:
        user = authenticate_user(db, form_data.username, form_data.password)
       
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
       
        refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
   

        access_token = create_access_token(
            data={"sub": user.username, "id": user.id}, expires_delta=access_token_expires)
        
   

        refresh_token = create_refresh_token(
        data={"sub": user.username, "id": user.id}, expires_delta=refresh_token_expires)


        return {"access_token": access_token, "token_type": "bearer", "user":user, "expires_in":int(access_token_expires.total_seconds()),  "refresh_token": refresh_token}
   except InvalidUserException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
   
   except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
   


async def user_signup(user_data:UserRegister, db:Annotated[Session, Depends(get_db)]):
    try:
        return await db_signup_users(db, user_data)
    except InvalidUserException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


async def get_gpt_token(grant_type:str = Form(...), refresh_token:Optional[str] = Form(None), code:Optional[str]=Form(None)):
   
   
    if grant_type == "refresh_token":
        if not refresh_token:
            raise credentials_exception
        user_id = await validate_refresh_token(refresh_token)
        if not user_id:
            raise credentials_exception
        
    elif grant_type == "authorization_code":
        user_id = await get_current_user_id(code)
        if not user_id:
            raise credentials_exception
        
    expires_access_token = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expires_refresh_token = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"id": user_id}, expires_delta=expires_access_token)
    
    rotate_fresh_token = create_refresh_token(
        data={"id": user_id}, expires_delta=expires_refresh_token)
    
    return {
        "access_token": access_token, 
        "refresh_token": rotate_fresh_token,
        "token_type": "bearer", 
        "expires_in":int(expires_access_token.total_seconds())
        }