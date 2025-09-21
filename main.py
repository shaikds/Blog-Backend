import datetime
import time
import uuid
from typing import List

import supabase
from fastapi import *

from app.models.Post import PostCreate, Post

app = FastAPI()
posts = {}
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    total_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(total_time)
    print(f"Request to {request.url.path} took {total_time:.4f} seconds")
    return response

@app.post("/posts/", status_code = 201)
async def create_post(post: PostCreate):
    post_json = post.dict()
    post_json["id"] = uuid.uuid4()
    post_json["created_at"] =  datetime.datetime.now()
    post_json["updated_at"] = None

    postModel = Post(**post_json)
    posts[postModel.id] = postModel

    return postModel

@app.put("/posts/{id}/", status_code = 200)
async def update_post(id: uuid.UUID, title: str, content: str, images: List[File(...)]):

    post_model = posts.get(id, None)
    post_model.title = title
    post_model.content = content
    post_model.images = images
    post_model.updated_at = datetime.datetime.now() ## INITs updated_at field

    db_storage = supabase.Client.storage
    supabase = supabase.Client(db_storage)



@app.get("/posts/", status_code = 200)
async def get_posts():
    return posts

@app.get("/posts/{id}", status_code = 200)
async def get_post(id: uuid.UUID):
    try:
        return posts[id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Resource Not Found")