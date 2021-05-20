import pickle
from app.database.models import User, Class, State

class CRUD:
    def __init__(self):
        try:
            self._users = self.load()
        except FileNotFoundError:
            self._users: dict[int, User] = {}


    def load(self) -> dict[int, User]:
        with open('data.pkl', 'rb') as f:
            return pickle.load(f)

    def save(self) -> None:
        with open('data.pkl', 'wb') as f:
            pickle.dump(self._users, f)

    def get_user(self, user_id: int) -> User:
        print(self._users)
        return self._users[user_id]

    def add_user(self, user: User) -> User:
        self._users[user.id] = user
        return user

    def exists_user(self, user_id: int) -> bool:
        return user_id in self._users

    def get_or_create_user(self, user_id: int) -> User:
        if user_id in self._users:
            return self.get_user(user_id)
        return self.add_user(User(user_id))

    def add_user_to_class(self, user_id: int, teacher_id: int, class_id: int) -> None:
        self.get_user(teacher_id).classes[class_id].add_user(user_id)
