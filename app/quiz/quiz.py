import random
from typing import Optional

from app.quiz.base import Question
from app.quiz.questions import SelectQuestion, SequenceQuestion


class Quiz:
    def __init__(self):
        self._length = 10
        self._current = 0
        self._questions: list[Question] = [
            SelectQuestion() if random.random() < .5 else SequenceQuestion()
            for _ in range(self._length)
        ]
        self._result = 0

    def answer(self, letter: str) -> Optional[bool]:
        answer = self._questions[self._current].answer(letter)
        if answer is not None:
            self._current += 1
            self._result += bool(answer)
        return answer

    @property
    def quesiton(self) -> Question:
        return self._questions[self._current]

    @property
    def result(self) -> int:
        return int(self._result / self._length * 100)

    def is_ended(self) -> bool:
        return self._current >= self._length

    def get_progress(self) -> int:
        return f'{self._current}/{self._length}'
