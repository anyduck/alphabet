import enum
from app.quiz.quiz import Quiz

class State(enum.Enum):
    MENU = enum.auto()
    QUIZ = enum.auto()
    CREATE_CLASS = enum.auto()


class Class:
    def __init__(self, id_, name):
        self.id = id_
        self.name = name
        self.users: list[int] = []

    def __repr__(self) -> str:
        return f'CLass{self.id, self.name, self.users}'

    def add_user(self, user_id):
        self.users.append(user_id)

    def del_user(self, user_id):
        self.users.remove(user_id)


class User:
    def __init__(self, id_, name):
        self.id = id_
        self.name = name
        self.classes: dict[int, Class] = {}
        self.state = State.MENU
        self.quiz: Quiz = None
        self.quiz_results: list[int] = []

    def __repr__(self) -> str:
        return f'User{self.id, self.name, self.classes}'

    def add_quiz_result(self, result: int):
        self.quiz_results.append(result)

    def add_class(self, class_: Class):
        self.classes[class_.id] = class_