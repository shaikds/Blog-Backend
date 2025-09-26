import datetime
import uuid
from typing import Optional, List
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    images: List[str] | None = None

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    images: List[str] | None = None

class Post(PostBase):
    id: uuid.UUID
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime = None