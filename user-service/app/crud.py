from sqlmodel import Session, select
from typing import Union

from app.core.utils import get_password_hash
from app.models import User,UserRegister 


class InvalidUserException(Exception):
    def __init__(self, status_code:int, detail:str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


def db_get_user(db:Session, username:Union[str, None] = None):
    
    try:
        if not username:
            raise InvalidUserException(status_code=400, detail="Username is required")
    
        user_query = select(User).where(User.username == username)
        user = db.exec(user_query).first()

        if not user:
            raise InvalidUserException(status_code=400, detail="Username not found")

        return user

    except Exception as e:
        raise InvalidUserException(status_code=400, detail=str(e))
   



async def db_signup_users(db:Session, user_data:UserRegister):

   # If useralready exist in database
    existing_user_email_query = select(User).where(User.email == user_data.email)
    existing_user_email = db.exec(existing_user_email_query).first()
    if existing_user_email:
        raise InvalidUserException(status_code=400, detail="User Email already exists")
    
    existing_user_username_query = select(User).where(User.username == user_data.username)
    existing_user_username = db.exec(existing_user_username_query).first()
    if existing_user_username:
        raise InvalidUserException(status_code=400, detail="User name already exists")
    

    hashed_password = get_password_hash(user_data.password)
    # If user is not in database , add new user
    new_user = User(
        username = user_data.username,
        email = user_data.email,
        full_name = user_data.full_name,
        hashed_password = hashed_password 
    )

    # add user in db
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
