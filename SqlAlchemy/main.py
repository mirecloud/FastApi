from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlmodel import Session, select

from database import get_session, init_db, engine
from models import Post, User
from schemas import PostRead, UserCreate, UserRead
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()              

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/posts/", response_model=Post, status_code=201)
def create_post(post: Post, session: Session = Depends(get_session)):
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@app.get("/posts/", response_model=List[PostRead], status_code=200)
def get_posts(session: Session = Depends(get_session)):
    #posts = session.exec(select(PostRead)).all()
    posts = session.exec(select(Post)).all()
    return posts

@app.get("/posts/{post_id}", response_model=Post)
def get_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(post)
    session.commit()
    return {"message": "Post deleted successfully"}

@app.post("/create_users/", response_model=UserRead, status_code=201)
def create_users(user: UserCreate, session: Session = Depends(get_session)):
    user.password = pwd_context.hash(user.password)
    try:
        user = User(**user.dict())
        session.add(user)
        session.commit()
        session.refresh(user)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    return user    

@app.get("/users/", response_model=List[UserRead], status_code=200)
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user 