import uuid
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from app.models.Post import Post, PostCreate, PostUpdate
from app.repository.posts_repo import PostRepository

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

# For Unit tests. If we won't use it like this, it will hard to test this class functionality,
# without the actual REPO connection to DB.
def get_repository() -> PostRepository:
    return PostRepository()

# CREATE POST
@router.post("/", response_model=Post, status_code=201)
async def create_post_route(
        post: PostCreate,
        repo: PostRepository = Depends(get_repository)  # הזרקת תלות
):
    # קוראים למתודה של האובייקט המוזרק
    new_post = repo.create_new_post(post)
    return new_post


# READ POSTS with CURSOR PAGINATION
@router.get("/", status_code=200)
async def get_posts_route(
        limit: Optional[int] = 10,
        cursor: Optional[str] = None,
        repo: PostRepository = Depends(get_repository)  # dependency injection
):
    # 1. Get all sorted posts from the repository
    sorted_posts = repo.get_all_posts()
    nextPageIdx = 0

    if cursor is not None:
        try:
            # A. Find the Post object whose ID matches the cursor (efficient search)
            # We explicitly cast post.id to str for comparison with the cursor string
            postToFind = next(post for post in sorted_posts if str(post.id) == cursor)

            # B. Find the index and start from the *next* post
            nextPageIdx = sorted_posts.index(postToFind) + 1

        except (StopIteration, ValueError):
            # StopIteration: next() failed to find a match.
            # ValueError: sorted_posts.index() failed.
            raise HTTPException(status_code=404, detail="Cursor not found or post was deleted.")

    # 2. Slice the list (Pagination)
    endIndex = nextPageIdx + limit
    res = sorted_posts[nextPageIdx:endIndex]

    # 3. Determine the next cursor
    next_cursor = None

    # Check if we returned exactly the limit, AND if there are more posts available
    if limit is not None and len(res) == limit and endIndex < len(sorted_posts):
        next_cursor = str(res[-1].id)

    return {
        "result": "success",
        "data": res,
        "limit": limit,
        "cursor": next_cursor
    }


# READ SINGLE POST
@router.get("/{id}", response_model=Post, status_code=200)
async def get_post_route(id: uuid.UUID, repo: PostRepository = Depends(get_repository)):
    post_model = repo.get_post_by_id(id)
    if not post_model:
        raise HTTPException(status_code=404, detail="Resource Not Found")
    return post_model


# UPDATE POST (PATCH)
@router.patch("/{id}", status_code=200)
async def update_post_route(id: uuid.UUID, post: PostUpdate, repo: PostRepository = Depends(get_repository)):
    updated_post = repo.update_existing_post(id, post)
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Resource Not Found")

    return updated_post


# DELETE POST
@router.delete("/{id}", status_code=204)
async def delete_post_route(id: uuid.UUID, repo: PostRepository = Depends(get_repository)):
    if not repo.delete_post_by_id(id):
        raise HTTPException(status_code=404, detail="Resource Not Found")
    return None
