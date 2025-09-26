import uuid
import datetime
from typing import Dict, List, Optional
from app.models.post import Post, PostCreate, PostUpdate

# Mock In-Memory Database
posts: Dict[uuid.UUID, Post] = {}


# Initialization logic remains outside the class for simplicity
def create_mock_data():
    """Initializes the in-memory database with mock data for testing."""
    for i in range(15):
        post_id = uuid.uuid4()
        creation_time = datetime.datetime.now() - datetime.timedelta(seconds=i * 15)

        posts[post_id] = Post(
            id=post_id,
            title=f"Post Title {i + 1} ({15 - i} minutes ago)",
            content=f"Content for post number {i + 1}.",
            images=[],
            created_at=creation_time,
            updated_at=None
        )


create_mock_data()


# --- Repository Class ---

class PostRepository:
    """Handles all data access operations for Posts."""

    def __init__(self):
        # In a real app, this would initialize DB connection, e.g., self.db = get_db_session()
        self.posts_db = posts

    def get_all_posts(self) -> List[Post]:
        """Retrieves all posts from the 'database' sorted by creation date."""
        return sorted(self.posts_db.values(), key=lambda post: post.created_at, reverse=True)

    def get_post_by_id(self, post_id: uuid.UUID) -> Optional[Post]:
        """Retrieves a single post by its UUID."""
        return self.posts_db.get(post_id)

    def create_new_post(self, post_data: PostCreate) -> Post:
        """Creates a new post object and adds it to the database."""
        new_id = uuid.uuid4()
        now = datetime.datetime.now()
        new_post = Post(
            id=new_id,
            created_at=now,
            updated_at=None,
            **post_data.dict()
        )
        self.posts_db[new_id] = new_post
        return new_post

    def update_existing_post(self, post_id: uuid.UUID, update_data: PostUpdate) -> Optional[Post]:
        """Updates an existing post by ID with provided data."""
        post_model = self.posts_db.get(post_id)
        if not post_model:
            return None

        update_dict = update_data.dict(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(post_model, key, value)

        post_model.updated_at = datetime.datetime.now()
        return post_model

    def delete_post_by_id(self, post_id: uuid.UUID) -> bool:
        """Deletes a post by ID and returns True if successful."""
        if post_id in self.posts_db:
            del self.posts_db[post_id]
            return True
        return False
