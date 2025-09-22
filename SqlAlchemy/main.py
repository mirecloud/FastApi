from fastapi import FastAPI, Depends, HTTPException
from database import get_session, init_db, engine
from sqlalchemy.exc import IntegrityError
from routers import post, user, auth, vote

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()              

app.include_router(post.router)
app.include_router(user.router) 
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}
    