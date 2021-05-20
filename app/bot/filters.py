from aiogram import types
from app.database import crud
from app.database.models import State

def StateFilter(state: State):
    def wrapper(message: types.Message) -> bool:
        return crud.get_user(message.from_user.id).state == state
    return wrapper

def CallbackFilter(data: str):
    def wrapper(query: types.CallbackQuery) -> bool:
        return query.data == data
    return wrapper
