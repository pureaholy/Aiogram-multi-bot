import asyncio
from datetime import datetime

from aiogram import Bot
from aiogram.enums import UpdateType
from aiogram.exceptions import TelegramUnauthorizedError

from database import db
from handlers import register_all_handlers
from handlers.user import register_user_handlers
from middlewares import register_all_middlewares
from misc.loader import dp, start_bot, dp_new_bots
from misc.polling_manager import PollingManager
from misc.utils import set_bot_commands


async def bot_start():
    register_all_middlewares(dp=dp)
    register_all_handlers(dp=dp)
    await set_bot_commands(bot=start_bot)

    register_user_handlers(dp=dp_new_bots)

    polling_manager = PollingManager()
    bots = [Bot(new_bot.token) for new_bot in db.get_all_bots()]

    for bot in bots:
        try:
            await bot.delete_webhook()
            await bot.get_updates(offset=-1)
            polling_manager.start_bot_polling(dp=dp_new_bots, bot=bot, polling_manager=polling_manager)
            bot_info = await bot.me()
            print(f'{bot_info.first_name} | {bot_info.username} | is Started...')
        except TelegramUnauthorizedError:
            bot_info = db.get_bot_by_bot_id(bot.id)
            await start_bot.send_message(chat_id=bot_info.user_id,
                                         text=f'Бот - {bot_info.title} был удален из списка ботов')
            db.remove_bot_by_bot_id(user_id=bot_info.user_id, bot_id=bot.id)

    bot_info = await start_bot.me()
    print(f'Hi {bot_info.username}. Bot started OK!\n «««  {datetime.now().replace(microsecond=0)}  »»»')

    await dp.start_polling(start_bot, dp_for_new_bot=dp_new_bots, polling_manager=polling_manager,
                           allowed_updates=[UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY])


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(bot_start())
    except KeyboardInterrupt:
        quit(0)
