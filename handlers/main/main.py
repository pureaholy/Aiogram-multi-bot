import re

from aiogram import Dispatcher, types, Bot, F
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.token import TokenValidationError

import config
import keyboards
import texts
from database import databases, db
from misc.polling_manager import PollingManager
from misc.states import AddBot
from misc.types import CallbackData
from misc.utils import pagination


async def start_command(message: types.Message, state: FSMContext):
    await state.clear()
    text = texts.start()
    reply_markup = keyboards.inline.start()
    await message.answer(text=text, reply_markup=reply_markup)


async def start_callback(callback: types.CallbackQuery, user_info: databases.User):
    callback_data = CallbackData.extract(data=callback.data)
    await callback.message.delete()
    if callback_data.data == CallbackData.Start.bots():
        pag = pagination(user_info.bots, 2)
        await callback.message.answer(texts.bots(), reply_markup=keyboards.inline.bots(ls=pag))


async def back(callback: types.CallbackQuery, state: FSMContext):
    callback_data = CallbackData.extract(data=callback.data)
    await state.clear()
    await callback.message.delete()
    if callback_data.data == CallbackData.Back.main_menu():
        text = texts.start()
        reply_markup = keyboards.inline.start()
        await callback.message.answer(text=text, reply_markup=reply_markup)


async def bots(callback: types.CallbackQuery, state: FSMContext,
               user_info: databases.User, polling_manager: PollingManager):
    callback_data = CallbackData.extract(data=callback.data)
    if callback_data.data == CallbackData.Bots.new():
        reply_markup = keyboards.inline.back(to=CallbackData.Back.main_menu(), main_menu=True)
        await callback.message.edit_text(texts.add_bot(),
                                         reply_markup=reply_markup)
        await state.set_state(AddBot.token)

    elif callback_data.data == CallbackData.Bots.move():
        pag = pagination(user_info.bots, 2)
        await callback.message.edit_reply_markup(
            reply_markup=keyboards.inline.bots(ls=pag, page_num=callback_data.args[0]))

    elif callback_data.data == CallbackData.Bots.select():
        bot_id = int(callback_data.args[0])
        info = db.get_bot_by_bot_id(bot_id=bot_id)

        text = texts.bot_info(title=info.title, username=info.username, token=info.token)
        reply_markup = keyboards.inline.bot_setting(bot_id=bot_id)
        await callback.message.edit_text(text=text, reply_markup=reply_markup)

    elif callback_data.data == CallbackData.Bots.remove():
        bot_id = int(callback_data.args[0])
        bot_info = db.get_bot_by_bot_id(bot_id)
        try:
            bot_info.delete()
            polling_manager.stop_bot_polling(bot_id)
            await callback.answer('Бот удален!')
            user_info = db.get_user_by_user_id(user_id=callback.from_user.id)

            pag = pagination(user_info.bots, 2)
            reply_markup = keyboards.inline.bots(ls=pag)
            await callback.message.edit_text(texts.bots(), reply_markup=reply_markup)
        except (ValueError, KeyError) as err:
            await callback.answer('Ошибка остановки бота')


async def get_token(message: types.Message, dp_for_new_bot: Dispatcher, polling_manager: PollingManager,
                    state: FSMContext):
    if re.match(config.RegEx.token, message.text):
        bot = Bot(message.text)
        try:
            if bot.id in polling_manager.polling_tasks:
                await message.answer("Бот уже был зарегистрирован в системе!")
                return

            await bot.delete_webhook()
            await bot.get_updates(offset=-1)

            polling_manager.start_bot_polling(
                dp=dp_for_new_bot,
                bot=bot,
                polling_manager=polling_manager
            )
            bot_user = await bot.me()
            db.add_bot(user_id=message.from_user.id, token=message.text,
                       title=bot_user.first_name, username=bot_user.username, bot_id=bot_user.id)
            await message.answer(
                texts.bot_info(title=bot_user.first_name, username=bot_user.username, token=message.text),
                reply_markup=keyboards.inline.bot_setting(bot_id=bot.id))
            await state.clear()

        except (TokenValidationError, TelegramUnauthorizedError) as err:
            await message.answer('Отправьте токен бота')
    else:
        reply_markup = keyboards.inline.back(to=CallbackData.Back.main_menu(), main_menu=True)
        await message.reply('<b>❗️ Ошибка, проверьте правильность токена</b>', reply_markup=reply_markup)
        await state.clear()


def register_main_handlers(dp: Dispatcher):
    dp.message.register(start_command, Command("start"))
    dp.callback_query.register(start_callback, lambda c: c.data.split("~")[0] == CallbackData.Start())
    dp.callback_query.register(back, lambda c: c.data.split("~")[0] == CallbackData.Back())

    dp.callback_query.register(bots, lambda c: c.data.split("~")[0] == CallbackData.Bots())
    dp.message.register(get_token, F.text, AddBot.token)
