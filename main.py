import logging
import asyncio
import hashlib
import urllib.parse

from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text

from app.config.bot import API_TOKEN, MESSAGES, WEB_HOST
from app.bot.keyboards import QuizKeyboard, MenuKeyboard
from app.bot.filters import StateFilter
from app.database.models import User, Class, State
from app.web import app
from app.quiz.quiz import Quiz
from app.database import crud


logging.basicConfig(level=logging.INFO)


bot = Bot(API_TOKEN)
dp = Dispatcher(bot)

Bot.set_current(bot)



##############################################################################
# Обробники повідомлень
##############################################################################

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    user = crud.get_or_create_user(message.from_user.id)

    if (class_code := message.get_args()):
        teacher_id, class_id = class_code.split(':')
        crud.add_user_to_class(user.id, teacher_id, class_id)
    user.state = State.MENU

    await message.answer(MESSAGES['start'], reply_markup=MenuKeyboard())


@dp.message_handler(Text(MESSAGES['start_game']))
async def start_game_message(message: types.Message):
    await bot.send_game(message.chat.id, 'alphabet_battle')


@dp.message_handler(Text(MESSAGES['start_quiz']))
async def start_quiz_message(message: types.Message):
    user = crud.get_user(message.from_user.id)
    user.state = State.QUIZ
    user.quiz = Quiz()
    await message.answer(
        f'{user.quiz.get_progress()} {user.quiz.quesiton}',
        parse_mode='HTML',
        reply_markup=QuizKeyboard(user.quiz.quesiton)
    )


@dp.message_handler(StateFilter(State.QUIZ))
async def answer_quiz_message(message: types.Message):
    user = crud.get_user(message.from_user.id)
    answer = user.quiz.answer(message.text)

    text = f"{user.quiz.get_progress()} {MESSAGES['correct' if answer or answer is None else 'wrong']}"

    if user.quiz.is_ended():
        user.add_quiz_result(user.quiz.result)
        user.state = State.MENU
        await message.answer(
            f"{text} {MESSAGES['quiz_result'].format(result=user.quiz.result)}",
            reply_markup=MenuKeyboard()
        )
    else:
        await message.answer(
            text if answer is None else f'{text} {user.quiz.quesiton}',
            parse_mode='HTML',
            reply_markup=QuizKeyboard(user.quiz.quesiton)
        )






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
