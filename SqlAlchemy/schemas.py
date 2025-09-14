from datetime import datetime
from pydantic import EmailStr
from sqlmodel import SQLModel 

class PostRead(SQLModel):
    title: str
    content: str
    published: bool

class UserRead(SQLModel):
    email: str
    #password: str   
    created_at: datetime
    id: int | None = None 

class UserCreate(SQLModel):
    email: EmailStr
    password: str                         