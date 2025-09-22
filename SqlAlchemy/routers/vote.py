from fastapi import HTTPException, APIRouter
from typing import List
from schemas import Vote as VoteSchemas
import database
from sqlmodel import select     
from fastapi.params import Depends
from sqlmodel import Session
import models
import auth2 as   auth

router = APIRouter(
    prefix="/votes",
    tags=["Votes"],
    responses={404: {"description": "Not found"}}  
)   

@router.post("/", status_code=201)
def vote(vote: VoteSchemas, session: database.Session = Depends(database.get_session), current_user: models.User = Depends(auth.get_current_user)):
    post = session.get(models.Post, vote.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    vote_record = session.get(models.Vote, (current_user.id, vote.post_id))
    
    if vote.dir == 1:
        if vote_record:
            raise HTTPException(status_code=409, detail="You have already voted on this post")
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        session.add(new_vote)
        session.commit()
        return {"message": "Vote added"}
    else:
        if not vote_record:
            raise HTTPException(status_code=404, detail="Vote does not exist")
        session.delete(vote_record)
        session.commit()
        return {"message": "Vote removed"}  

@router.get("/", response_model=List[VoteSchemas], status_code=200)
def get_votes(session: Session = Depends(database.get_session), current_user: models.User = Depends(auth.get_current_user)):
    votes = session.exec(select(models.Vote).where(models.Vote.user_id == current_user.id)).all()
    return votes    

@router.get("/{post_id}", response_model=VoteSchemas)
def get_vote(post_id: int, session: Session = Depends(database.get_session), current_user: models.User = Depends(auth.get_current_user)):
    vote = session.get(models.Vote, (current_user.id, post_id))
    if not vote:
        raise HTTPException(status_code=404, detail="Vote not found")
    return vote

@router.delete("/{post_id}", status_code=204)
def delete_vote(post_id: int, session: Session = Depends(database.get_session), current_user: models.User = Depends(auth.get_current_user)):
    vote = session.get(models.Vote, (current_user.id, post_id))
    if not vote:
        raise HTTPException(status_code=404, detail="Vote not found")
    session.delete(vote)
    session.commit()
    return {"message": "Vote removed"}
    