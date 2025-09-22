from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Post(SQLModel, table=True):
    __tablename__ = "Posts"

    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    published: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # 👇 important: owner_id must be defined
    owner_id: int = Field(foreign_key="Users.id", nullable=False)

    owner: "User" = Relationship(back_populates="posts")


class User(SQLModel, table=True):
    __tablename__ = "Users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    posts: list[Post] = Relationship(back_populates="owner")

class Vote(SQLModel, table=True):
    __tablename__ = "Votes"

    user_id: int = Field(foreign_key="Users.id", primary_key=True)
    post_id: int = Field(foreign_key="Posts.id", primary_key=True)  
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)   
    