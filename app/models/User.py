import uuid

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base schema for user data."""
    username: str
    email: EmailStr

class UserRegister(UserBase):
    """Schema for a new user registration request (client -> server)."""
    password: str

class UserLogin(BaseModel):
    """Schema for a user login request (client -> server)."""
    username: str
    password: str

class UserResponse(UserBase):
    """Schema for the user data sent back to the client (excludes password/hash)."""
    id: uuid.UUID

    class Config:
        from_attributes = True

class UserInDB(UserBase):
    """Schema for a user object as stored internally (includes the hashed password)."""
    id: uuid.UUID
    hashed_password: str
    username: str
    email: EmailStr

    class Config:
        from_attributes = True

