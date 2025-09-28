import uuid
from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models.Token import Token
from app.models.User import UserRegister, UserResponse, UserInDB
from app.repository.users_repo import UsersRepo
from app.services.auth.security import *

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def get_user_repository() -> UsersRepo:
     return UsersRepo()
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
        user_data: UserRegister,
        repo: UsersRepo = Depends(get_user_repository)
):
    """ Register a new user"""
    if repo.get_user_by_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken"
        )

    if repo.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email address already registered"
        )

    new_user_db = repo.create_user(user_data)
    return new_user_db

@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        repo: UsersRepo = Depends(get_user_repository)
):
    user = repo.get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(401, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
async def read_user_me(
        current_user: UserInDB = Depends(get_current_user)
):
    return current_user