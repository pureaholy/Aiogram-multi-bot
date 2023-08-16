from aiogram.fsm.state import StatesGroup, State


class Admin(StatesGroup):
    ross = State()


class AddBot(StatesGroup):
    token = State()
