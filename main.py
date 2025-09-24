import datetime
import os
import time
import uuid
from typing import List
from supabase import create_client, Client
from fastapi import *

from app.models.Post import PostCreate, Post
from app.services.supabase_service import SupabaseService

app = FastAPI()
posts = {}
supabaseService = SupabaseService()
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


    # post creation
    postModel = Post(**post_json)

    await supabase.create_post(postModel)

    return imagesLinkList

@app.put("/posts/{id}/", status_code = 200)
async def update_post(id: uuid.UUID, title: str, content: str, images: List[File(...)]):

    post_model = posts.get(id, None)
    post_model.title = title
    post_model.content = content
    post_model.images = images
    post_model.updated_at = datetime.datetime.now() ## INITs updated_at field

    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)



@app.get("/posts/", status_code = 200)
async def get_posts():
    return posts

@app.get("/posts/{id}", status_code = 200)
async def get_post(id: uuid.UUID):
    try:
        return posts[id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Resource Not Found")