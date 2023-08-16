from aiogram import Dispatcher, types, Bot
from aiogram.exceptions import TelegramUnauthorizedError
from database import db
from misc.loader import start_bot
from misc.polling_manager import PollingManager


async def start(message: types.Message, bot: Bot, polling_manager: PollingManager):
    try:
        await message.copy_to(chat_id=message.from_user.id)
    except TelegramUnauthorizedError:
        polling_manager.stop_bot_polling(int(bot.id))
        bot_info = db.get_bot_by_bot_id(bot.id)
        db.remove_bot_by_bot_id(user_id=bot_info.bot_id, bot_id=bot.id)
        await start_bot.send_message(chat_id=bot_info.user_id,
                                     text=f'Бот - {bot_info.title} был удален из списка ботов')


def register_main_handlers(dp: Dispatcher):
    dp.message.register(start)
