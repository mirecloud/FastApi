from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlmodel import Session, select

from database import get_session, init_db, engine
from models import Post, User
from schemas import PostRead, UserCreate, UserRead
from sqlalchemy.exc import IntegrityError
from routers import post, user

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()              

app.include_router(post.router)
app.include_router(user.router) 
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}   


