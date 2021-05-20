import random
from typing import Optional

from app.quiz.base import Question
from app.quiz.questions import SelectQuestion, SequenceQuestion


class Quiz:
    def __init__(self):
        self._length = 20
        self._current_question = 0
        self._questions: list[Question] = [
            SelectQuestion() if random.random() < .5 else SequenceQuestion()
            for _ in range(self._length)
        ]
        self._result = 0

    def answer(self, letter: str) -> Optional[bool]:
        answer = self._questions[self._current_question].answer(letter)
        if answer is not None:
            self._current_question += 1
            self._result += bool(answer)
        return answer

    @property
    def quesiton(self) -> Question:
        return self._questions[self._current_question]

    @property
    def result(self) -> int:
        return int(self._result / self._length * 100)

    @property
    def is_ended(self) -> bool:
        return self._current_question >= self._length
