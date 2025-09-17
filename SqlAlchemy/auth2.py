from jose import JWTError, jwt
from datetime import datetime, timedelta
from schemas import UserLogin
import models, database, utils
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from database import get_session    
from sqlmodel import select

SECRET_KEY = "qwertyuiop[]asdfghjkl;'zxcvbnm,./1234567890-="
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30        

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt  
   
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    return token_data   
     
def get_current_user(token: str = Depends(database.oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)
    user = session.exec(select(models.User).where(models.User.email == token.email)).first()
    if user is None:
        raise credentials_exception
    return user     