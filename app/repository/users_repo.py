import uuid
from typing import Dict, Optional

from app.models.User import UserInDB, UserRegister
from app.services.auth.security import get_password_hash

users_db: Dict[uuid.UUID, UserInDB] = {}


class UsersRepo:

    def __init__(self):
        self.db = users_db

    def create_user(self, user_in: UserRegister) -> UserInDB:
        """ Creates a new user in the database """
        hashed_password = get_password_hash(user_in.password)

        new_id = uuid.uuid4()
        user_db_instance = UserInDB(
            id=new_id,
            username=user_in.username,
            email=user_in.email,
            hashed_password=hashed_password
        )

        self.db[new_id] = user_db_instance
        return user_db_instance

    def get_user_by_username(self, username: str) -> Optional[UserInDB]:
        """ Get a user by username """
        try:
            user_found = next(
                user for user in self.db.values() if user.username == username
            )
            return user_found
        except StopIteration:
            return None

    def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """ Get a user by email value"""
        try:
            user_found = next(
                user for user in self.db.values() if user.email == email
            )
            return user_found
        except StopIteration:
            return None

    def get_user_by_id(self, user_id: uuid.UUID) -> Optional[UserInDB]:
        return self.db.get(user_id)
