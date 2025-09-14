from datetime import datetime
from sqlmodel import SQLModel, Field

class Post(SQLModel, table=True):

    __tablename__ = "Posts"

    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    published: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class User(SQLModel, table=True):

    __tablename__ = "Users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)       

 
