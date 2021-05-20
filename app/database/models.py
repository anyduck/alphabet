import enum
from app.quiz.quiz import Quiz

class State(enum.Enum):
    MENU = enum.auto()
    QUIZ = enum.auto()
    CREATE_CLASS = enum.auto()


class User:
    def __init__(self, id_, class_code=None):
        self.id = id_
        self.classes: dict[int, Class] = {}
        self.state = State.MENU
        self.quiz: Quiz = None
        self.quiz_results: list[int] = []

    def add_quiz_result(self, result: int):
        self.quiz_results.append(result)

class Class:
    def __init__(self, id_, name):
        self.id = id_
        self.name = name
        self.users: list[int] = []

    def add_user(self, user_id):
        self.users.append(user_id)

    def del_user(self, user_id):
        self.users.remove(user_id)
