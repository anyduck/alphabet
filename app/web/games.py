from aiohttp import web
from aiogram import types, Bot

routes = web.RouteTableDef()

#TODO: import bot

@routes.post('/api/{gmame_short_name}/set_score')
async def set_score(request: web.BaseRequest):
    """ Встановлює новий максимальний бал в грі для користувача. """

    await Bot.get_current().set_game_score(
        request.query['user_id'],
        request.query['score'],
        inline_message_id=request.query['inline_message_id']
    )
    return web.json_response({'status': 'success'})

@routes.get('/api/{gmame_short_name}/get_high_scores')
async def get_high_scores(request: web.BaseRequest):
    """ Повертає таблицю лідерів в грі. """

    scores: list[types.GameHighScore] = await Bot.get_current().get_game_high_scores(
        request.query['user_id'],
        inline_message_id=request.query['inline_message_id']
    )
    return web.json_response([score.to_python() for score in scores])
