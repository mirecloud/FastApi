from fastapi import FastAPI, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
import time


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
     

while True:
    try:
        conn = psycopg.connect(
            "dbname=Fastapi user=admin password=admin host=192.168.52.1 port=5432"
        )
        cursor = conn.cursor()
        print("✅ Database connection was successful")
        break
    except Exception as error:
        print("❌ Connecting to database failed")
        print("Error:", error)
        time.sleep(2)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM public.\"Posts\"")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}      
    #return {"Hello": "Tis is your post data"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
#def create_posts(payload: dict = Body(...) ):
def create_posts(post: Post):

    #print(payload)
    cursor.execute(
        "INSERT INTO public.\"Posts\" (title, content, published) VALUES (%s, %s, %s) RETURNING *",
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    conn.commit()
    print(new_post)
     
    #return {"new_post": f"title {payload['title']}  content: {payload['content']}"}
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM public.\"Posts\" WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    print(post)
    return {"post_detail": post}
    #return {"post_detail": f"Here is your post with id: {id}"} 

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):   
    cursor.execute("DELETE FROM public.\"Posts\" WHERE id = %s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        return {"message": f"post with id: {id} was not found"}
    return {"message": f"post with id: {id} was successfully deleted"}
    #return {"message": f"post with id: {id} was successfully deleted"}             

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        "UPDATE public.\"Posts\" SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
        (post.title, post.content, post.published, str(id)),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        return {"message": f"post with id: {id} was not found"}
    return {"data": updated_post}
    #return {"data": f"post with id: {id} was updated"}     