from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from app.config.bot import MESSAGES
from app.quiz.base import Question
from app.database.models import Class


class TestKeyboard(InlineKeyboardMarkup):
    def __init__(self):
        keyboard = [
            [InlineKeyboardButton('class_name', callback_data='get_in')],
        ]
        super().__init__(row_width=len(keyboard), inline_keyboard=keyboard)


class MenuKeyboard(ReplyKeyboardMarkup):
    def __init__(self):
        keyboard = [
            [KeyboardButton(MESSAGES['start_game'])],
            [KeyboardButton(MESSAGES['start_quiz'])],
            [KeyboardButton(MESSAGES['class_menu'])],
        ]
        super().__init__(row_width=len(keyboard), keyboard=keyboard)


class QuizKeyboard(ReplyKeyboardMarkup):
    def __init__(self, question: Question):
        half = len(question._answers) // 2
        keyboard = [
            [KeyboardButton(answer) for answer in question._answers[half:]],
            [KeyboardButton(answer) for answer in question._answers[:half]],
        ]
        super().__init__(row_width=len(keyboard), keyboard=keyboard)


class ClassesMenuKeyboard(InlineKeyboardMarkup):
    def __init__(self, classes: list[Class]):
        keyboard = [
            [InlineKeyboardButton(class_.name, callback_data=f'list_class:{class_.id}')]
            for class_ in classes
        ] + [
            [InlineKeyboardButton(MESSAGES['create_class'], callback_data='create_class')]
        ]
        super().__init__(row_width=len(keyboard), inline_keyboard=keyboard)


class ClassMenuKeyboard(InlineKeyboardMarkup):
    def __init__(self):
        keyboard = [
            [InlineKeyboardButton(MESSAGES['back'], callback_data='back')]
        ]
        super().__init__(row_width=len(keyboard), inline_keyboard=keyboard)