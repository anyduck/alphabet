from aiohttp import web
from app.web.games import routes

app = web.Application()
app.add_routes(routes)