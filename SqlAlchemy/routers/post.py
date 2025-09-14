from fastapi import HTTPException, APIRouter
from typing import List
from psycopg import IntegrityError
from sqlmodel import select     
from fastapi.params import Depends
from sqlmodel import Session
from database import get_session
from models import Post, User
from schemas import PostRead


router = APIRouter()

@router.post("/posts/", response_model=Post, status_code=201)
def create_post(post: Post, session: Session = Depends(get_session)):
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@router.get("/posts/", response_model=List[PostRead], status_code=200)
def get_posts(session: Session = Depends(get_session)):
    #posts = session.exec(select(PostRead)).all()
    posts = session.exec(select(Post)).all()
    return posts

@router.get("/posts/{post_id}", response_model=Post)
def get_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(post)
    session.commit()
    return {"message": "Post deleted successfully"}