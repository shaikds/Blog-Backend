import os
import uuid
from datetime import timedelta, datetime
from typing import Optional

from docutils.nodes import status
from fastapi import HTTPException, Depends
import jwt
from passlib.context import CryptContext

from app.models.User import UserInDB
from app.repository.users_repo import UsersRepo
from app.routers.users_router import get_user_repository

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "2l3jP4oY8qN5tD7sF6aK1hG9rZ0xWcQeBnVm4uI7yT3pA8sD2fG0hJ5kL9zX1c"
)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plaintext, hashed):
    return pwd_context.verify(plaintext, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode=data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt

def decode_access_token(token:str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

        return payload
    except jwt.exception.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Signature has expired")
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


async def get_current_user(
        token: str = Depends(oauth2_scheme),  # Automatically extracts the token string
        repo: UsersRepo = Depends(get_user_repository)
) -> UserInDB:
    """
    The dependency that authenticates the user based on the JWT token.
    1. Decodes the token.
    2. Uses the user ID (sub) to fetch the complete UserInDB object from the repository.
    3. Raises 401 if token is invalid, expired, or user is not found.
    """
    # 1. Decode and Validate
    payload = decode_access_token(token)

    # 2. Extract ID and Fetch from DB
    user_id = uuid.UUID(payload.get("sub"))
    user = repo.get_user_by_id(user_id)

    # 3. Final check for user existence
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # 4. Return the fully authenticated user object
    return user
