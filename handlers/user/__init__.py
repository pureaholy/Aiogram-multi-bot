from aiogram import Dispatcher

from handlers.user.main import register_main_handlers


def register_user_handlers(dp: Dispatcher):
    handlers = (
        register_main_handlers,
    )
    for handler in handlers:
        handler(dp)
