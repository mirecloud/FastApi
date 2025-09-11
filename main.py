from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/posts")
def get_posts():
    return {"Hello": "Tis is your post data"}


@app.post("/posts")
#def create_posts(payload: dict = Body(...) ):
def create_posts(post: Post):

    #print(payload)
    print(post)
    print(post.dict())
    #return {"new_post": f"title {payload['title']}  content: {payload['content']}"}
    return {"data": post}