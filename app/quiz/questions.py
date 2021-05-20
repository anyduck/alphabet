import random
from typing import Optional

from app.config.bot import MESSAGES
from app.quiz.base import Question, ALPHABET


class SequenceQuestion(Question):
    def __init__(self):
        self._question = self._init_question(4)
        self._answer, self._answers = self._init_answers(4)

    def __repr__(self) -> str:
        return f'Вкажіть послідовність літер:'

    def _init_answers(self, n: int) -> tuple[str, str]:
        answers = list(self._question)
        random.shuffle(answers)

        return self._question[0], ''.join(answers)

    def answer(self, letter: str) -> Optional[bool]:
        if not letter.isalpha() or letter not in self._answers:
            return None
        if not letter == self._answer:
            return False

        self._answers = self._answers.replace(letter, MESSAGES['correct'])
        self._question = self._question.replace(letter, '')
        try:
            self._answer = self._question[0]
        except IndexError:
            return True
        return None


class SelectQuestion(Question):
    def __init__(self):
        self._question = self._init_question(random.randrange(3, 6))
        self._answer, self._answers = self._init_answers(4)

    def __repr__(self) -> str:
        return f'Оберіть пропущену літеру: <b>{self._question}</b>'

    def _init_answers(self, n: int) -> tuple[str, str]:
        answer = random.choice(self._question)
        answers = random.sample(ALPHABET.replace(self._question, ''), n)
        answers[-1] = answer
        self._question = self._question.replace(answer, '_')

        random.shuffle(answers)

        return answer, ''.join(answers)

    def answer(self, letter: str) -> Optional[bool]:
        return letter == self._answer