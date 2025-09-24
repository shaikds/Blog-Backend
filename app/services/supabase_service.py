import os
import uuid
from typing import List

from fastapi import File, UploadFile
from supabase import create_client, Client

from app.models.Post import PostBase


class SupabaseService:
    def __init__(self):
        self.url: str = os.environ.get("DB_URL")
        self.key: str = os.environ.get("DB_KEY")
        self.supabase: Client = create_client(self.url, self.key)


    # async def upload_images(self, images: List[UploadFile]):
    #     # Get unique image id
    #     res: [str] = []
    #     for image in images:
    #         filename = f"{uuid.uuid4()}-{image.filename}"
    #         response = await self.supabase.storage.from_('blogs').upload(file=image.file, path=filename)
    #
    #         # Get the public URL after uploading
    #         public_url = self.supabase.storage.from_('blogs').get_public_url(path=filename)
    #         res.append(public_url)
    #
    #     return res

    # async def update_post(self, post: PostBase):
    #     response = await self.supabase.

    async def create_post(self, post:PostBase):
        response = await self.supabase.