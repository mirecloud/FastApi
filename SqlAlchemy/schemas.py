from datetime import datetime
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

 
class PostCreate(SQLModel):
    title: str
    content: str
    published: bool = True

class PostRead(SQLModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: "UserRead"  # Forward reference to UserRead
    votes: Optional[int] = 0  # To hold the count of votes

class UserRead(SQLModel):
    email: str
    #password: str   
    created_at: datetime
    id: int | None = None 

class UserCreate(SQLModel):
    email: EmailStr
    password: str  

class UserLogin(SQLModel):
    username: EmailStr
    password: str                          

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    email: str | None = None    

class Vote(SQLModel):   
    post_id: int
    dir: int    # 1 for upvote, 0 for remove vote
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    #user_id: int
    # user_id will be set in the route based on the current authenticated user

# Resolve forward references
