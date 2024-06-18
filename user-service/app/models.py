
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Union



class Token(SQLModel):
    """
    Represents a basic token with fields for an access token and token type.
    """
    access_token: str
    token_type: str



class GptToken(Token):
    """
    Represents a GPT (Generative Pre-trained Transformer) token, which extends the basic Token model.
    Adds fields for expiration time and refresh token.
    """
    expires_in: int
    refresh_token: str



class TokenData(SQLModel):
    """
    Represents token-related data, particularly associated with a user (identified by username).
    """
    username: str | None = None




class UserRead(SQLModel):
    """
    Represents user data that can be read.
    """
    username: str = Field(unique=True, index=True)
    full_name:str = Field()
    email: str = Field(unique=True, index=True)
    email_verified: Union[bool, None] = None




class User(UserRead, table=True):
    """
    Represents a generic user model with fields for ID, hashed password, email verification status,
    and timestamps for creation and update.
    """
    id:UUID | None = Field(default_factory=uuid4, primary_key=True, index=True)
    hashed_password: str = Field(index=True)
    email_verified: bool = Field(default=False)
    updated_at: datetime | None = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})
    created_at: datetime = Field(default_factory=datetime.now)



class UserRegister(UserRead):
    """
    Represents user registration data, including all user data plus the password.
    """
    password: str 



class UserInDb(UserRead):
    """
    Represents user data stored in the database, including fields for ID and hashed password.
    """
    id:UUID
    hashed_password: str
    


class UserOutput(UserRead):
    """
    Represents user data that is outputted, including only the user's ID.
    """
    id:UUID



  
class LoginResponse(Token):
    """
    Represents the response returned after a user logs in.
    Includes token-related data, information about the logged-in user, and expiration time for the login session.
    """
    user: UserOutput
    expires_in: int
    refresh_token: str
