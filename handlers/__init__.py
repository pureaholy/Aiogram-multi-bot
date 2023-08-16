from aiogram import Dispatcher

from handlers.error import register_all_error_handlers
from handlers.main import register_all_main_handlers
from handlers.admin import register_all_admin_handlers
from handlers.other import register_other_handlers


def register_all_handlers(dp: Dispatcher) -> None:
    handlers = (
        register_all_main_handlers,
        register_all_admin_handlers,
        register_all_error_handlers,
        register_other_handlers
    )
    for handler in handlers:
        handler(dp)
