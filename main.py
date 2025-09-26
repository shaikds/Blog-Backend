import datetime
import os
import time
import uuid
from typing import List
from supabase import create_client, Client
from fastapi import *

from app.models.Post import PostCreate, Post, PostBase, PostUpdate
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
    posts[post.id] = postModel
    return {
        "result": "success",
        "data": postModel
    }


    # await supabase.create_post(postModel)

    # return imagesLinkList

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
async def get_posts(limit: int|None = None, cursor: str | None  = None ):
    sortedPosts = sorted(posts.values(), key=lambda post: post.created_at, reverse=True)
    res = []
    if limit is not None:
        res = sortedPosts[:limit]
        rest = sortedPosts[limit:]
        if len(res) > 0:
            # create cursor for next


    return {
        "result": "success",
        "data": res,
        "cursor":
    }

@app.get("/posts/{id}", status_code = 200)
async def get_post(id: uuid.UUID):
    try:
        return posts[id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Resource Not Found")

@app.patch("/posts/{id}/", status_code = 200)
async def update_post(id: uuid.UUID, post: PostUpdate):
    try:
        postModel = posts.get(id, None)
        if not postModel:
            raise KeyError

        # Update the post
        if post.images is not None:
            postModel.images = post.images
        if post.title is not None:
            postModel.title = post.title
        if post.content is not None:
            postModel.content = post.content
        postModel.updated_at = datetime.datetime.now()

        return {
            "result": "success",
            "data": postModel
        }
    except KeyError:
        raise HTTPException(status_code=404, detail="Resource Not Found")

@app.delete("/posts/{id}/", status_code = 204)
async def delete_post(id: uuid.UUID):
    if id not in posts:
        raise HTTPException(status_code=404, detail="Resource Not Found")
    del posts[id]
    return None

