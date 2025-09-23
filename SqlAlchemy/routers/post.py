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
from sqlalchemy import func, select
from sqlalchemy.orm import column_property
from models import Vote

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    responses={404: {"description": "Not found"}}  
)

@router.get("/", response_model=List[PostRead])
def get_posts(session: Session = Depends(get_session)):
    query = (
        session.query(
            Post,
            func.count(Vote.post_id).label("votes")
        )
        .outerjoin(Vote, Vote.post_id == Post.id)
        .group_by(Post.id)
    )

    results = query.all()

    posts = [
        PostRead(
            id=post.id,
            title=post.title,
            content=post.content,
            published=post.published,
            created_at=post.created_at,
            owner_id=post.owner_id,
            owner=post.owner,
            votes=votes,
        )
        for post, votes in results
    ]

    return posts






@router.get("/", response_model=List[PostRead], status_code=200)
def get_posts(session: Session = Depends(get_session), current_user: User = Depends(auth.get_current_user)):
    posts = session.exec(select(Post)).all()
    
    return posts

@router.get("/{post_id}", response_model=PostRead)
def get_post(
    post_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(auth.get_current_user),
):
    # Vérifie si le post existe
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Vérifie si l'utilisateur est autorisé
    if current_user.id != post.owner_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this post")

    # Compte le nombre de votes pour ce post
    votes_count = session.query(func.count(Vote.post_id)).filter(Vote.post_id == post.id).scalar()

    # Retourne un PostRead enrichi
    return PostRead(
        id=post.id,
        title=post.title,
        content=post.content,
        published=post.published,
        created_at=post.created_at,
        owner_id=post.owner_id,
        owner=post.owner,
        votes=votes_count,
    )

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