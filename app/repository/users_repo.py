import datetime
import uuid
from typing import Dict

from app.models import User

users: Dict[uuid.UUID, User] = {}


def create_mock_data():
    """Initializes the in-memory database with mock data for testing."""
    for i in range(15):
        post_id = uuid.uuid4()
        creation_time = datetime.datetime.now() - datetime.timedelta(seconds=i * 15)

        users[post_id] = users(

            id: uuid.UUID,

        )

    class UsersRepo:
    """Handles all data access operations for Posts."""

    def __init__(self):
        # In a real app, this would initialize DB connection, e.g., self.db = get_db_session()
        self.users_db = users
