from app.config.bot import API_TOKEN


import logging
import asyncio
import hashlib

import urllib.parse

from aiohttp import web
from aiogram import Bot, Dispatcher, types
	
from aiogram.dispatcher.filters import Text

from app.config.bot import API_TOKEN, MESSAGES, WEB_HOST
from app.web import app
from app.bot.keyboards import QuizKeyboard, MenuKeyboard
from app.classes.quiz import Quiz


logging.basicConfig(level=logging.INFO)


bot = Bot(API_TOKEN)
dp = Dispatcher(bot)

Bot.set_current(bot)

import enum
class State(enum.Enum):
    MENU = enum.auto()
    QUIZ = enum.auto()
    CREATE_CLASS = enum.auto()



class User:
    def __init__(self, id_, class_code=None):
        self.id = id_
        self.class_list: dict[int, Class] = {}
        self.state = State.MENU
        self.quiz: Quiz = None
        self.results: list[int] = []

    def add_to_class(self, class_code: str):
        teacher_id, class_id = class_code.split(':')
        USERS[teacher_id].class_list[class_id].add_user(self.id)

    def add_quiz_result(self, result: int):
        self.list.results(result)

class Class:
    def __init__(self, id_, name):
        self.id = id_
        self.name = name
        self.list: list[int] = []

    def add_user(self, user_id):
        self.list.append(user_id)

    def del_user(self, user_id):
        self.list.remove(user_id)


USERS: dict[int, User] = {}

##############################################################################
# Обробники повідомлень
##############################################################################

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    user_id = message.from_user.id
    if user_id not in USERS:
        USERS[user_id] = User(user_id)
    user = USERS[user_id]
    if (class_code := message.get_args()):
        user.add_to_class(class_code)
    user.state = State.MENU

    await message.answer(MESSAGES['start'], reply_markup=MenuKeyboard())

@dp.message_handler(Text(MESSAGES['start_game']))
async def start_game_message(message: types.Message):
    await bot.send_game(message.chat.id, 'alphabet_battle')

@dp.message_handler(Text(MESSAGES['start_quiz']))
async def start_quiz_message(message: types.Message):
    user_id = message.from_user.id
    user = USERS[message.from_user.id]
    user.state = State.QUIZ
    user.quiz = Quiz()
    await message.answer(user.quiz.quesiton, parse_mode='HTML', reply_markup=QuizKeyboard(user.quiz.quesiton))

@dp.message_handler(lambda message: USERS[message.from_user.id].state == State.QUIZ)
async def answer_quiz_message(message: types.Message):
    user = USERS[message.from_user.id]
    answer = user.quiz.answer(message.text)

    if answer:
        await message.answer(MESSAGES['correct'])
    elif not answer:
        await message.answer(MESSAGES['wrong'])

    if user.quiz.is_ended:
        user.add_quiz_result(user.quiz.result)
        user.quiz = None
        user.state = State.MENU
        await message.answer(MESSAGES['quiz_result'].format(result=user.quiz.result), reply_markup=MenuKeyboard())
    else:
        await message.answer(user.quiz.quesiton, parse_mode='HTML', reply_markup=QuizKeyboard(user.quiz.quesiton))



@dp.callback_query_handler(lambda query: query.game_short_name is not None)
async def start_games_query(query: types.CallbackQuery):
    urlargs = urllib.parse.urlencode({
        'userd_id' :query.from_user.id,
        'inline_message_id': query.inline_message_id,
    })
    await query.answer(url=f'{WEB_HOST}/{query.game_short_name}?{urlargs}')

@dp.inline_handler()
async def list_games_query(inline_query: types.InlineQuery):
    text = inline_query.query or 'echo'
    alphabet_battle = types.InlineQueryResultGame(
        id=hashlib.md5(text.encode()).hexdigest(),
        game_short_name='alphabet_battle'
    )
    await inline_query.answer([alphabet_battle], cache_time=300)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dp.skip_updates())
    loop.create_task(dp.start_polling())
    web.run_app(app=app, host='0.0.0.0', port=8000)
