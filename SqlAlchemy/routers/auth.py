from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import schemas
import database, utils 
from database import get_session
import models
from sqlmodel import Session
import auth2    


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    # Authentication logic would go here
    user = session.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user or not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = auth2.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}   