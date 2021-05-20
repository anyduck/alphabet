import random
from typing import Optional

ALPHABET = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'


class Question:
    def __init__(self, qestion_length):
        self._question = self._init_question(qestion_length)
        self._answer = self._answers = None

    def __repr__(self) -> str:
        return f'Question{self.question}'

    @property
    def answers(self) -> str:
        return self._answers

    def _init_question(self, n: int) -> str:
        start = random.randrange(0, len(ALPHABET) - n)
        return ALPHABET[start:start + n]

    def _init_answers(self, n: int) -> tuple[str, str]:
        raise NotImplementedError

    def answer(self, letter: str) -> Optional[bool]:
        raise NotImplementedError
