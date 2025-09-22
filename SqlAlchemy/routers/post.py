from fastapi import HTTPException, APIRouter
from typing import List
from psycopg import IntegrityError
from sqlmodel import select     
from fastapi.params import Depends
from sqlmodel import Session
from database import get_session
from models import Post, User
from schemas import PostRead , PostCreate
import auth2 as   auth

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    responses={404: {"description": "Not found"}}  
)

@router.post("/", response_model=PostRead, status_code=201)
def create_post(
    post_in: PostCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(auth.get_current_user),
):
    # Build the Post directly from input + owner_id
    post = Post(**post_in.model_dump(), owner_id=current_user.id)

    session.add(post)
    session.commit()
    session.refresh(post)
    return post






@router.get("/", response_model=List[PostRead], status_code=200)
def get_posts(session: Session = Depends(get_session), current_user: User = Depends(auth.get_current_user)):
    posts = session.exec(select(Post)).all()
    
    return posts

@router.get("/{post_id}", response_model=PostRead)
def get_post(post_id: int, session: Session = Depends(get_session), current_user: User = Depends(auth.get_current_user)):
    post = session.get(Post, post_id)
    if current_user.id != post.owner_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this post")
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, session: Session = Depends(get_session), current_user: User = Depends(auth.get_current_user)):
    post = session.get(Post, post_id)
    if current_user.id != post.owner_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this post")
        
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    session.delete(post)
    session.commit()
    return {"message": "Post deleted successfully"}