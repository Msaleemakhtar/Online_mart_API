from fastapi import HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer

from uuid import UUID
from datetime import datetime, timedelta, timezone
from typing import Any, Union
 
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core import settings


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# create  a custom credentials exception
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    headers={"WWW-Authenticate": "Bearer"},
    detail={"error": "access_token", "error_description":"The access token expired" }
)


# get the id of current user
async def get_current_user_id(token: str | None = Security(Oauth2_scheme)):
  
    try:
        if not token:
            raise credentials_exception
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[str(ALGORITHM)])
        user_id: UUID = UUID(payload.get("id"))
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
           
        )


# verify the refresh token  
async def validate_refresh_token(refresh_token: str)->Union[str, None]:
    try:
        payload:dict[str, Any]  = jwt.decode(refresh_token, str(SECRET_KEY), algorithms=[str(ALGORITHM)]) 
        user_id:Union[str, None] = payload.get("id")
        if not user_id:
            return None
        return user_id
    except JWTError:
        return None
    


# create refresh token
def create_refresh_token(data:dict, expires_delta:Union[timedelta, None]= None):
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















