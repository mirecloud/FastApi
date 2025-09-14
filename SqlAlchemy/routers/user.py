
from fastapi import Depends, HTTPException,APIRouter
from typing import List
from psycopg import IntegrityError
from sqlmodel import Session, select
from database import get_session
from models import User
from schemas import UserCreate, UserRead

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},  
)

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/create_users/", response_model=UserRead, status_code=201)
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

@router.get("/", response_model=List[UserRead], status_code=200)
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user 