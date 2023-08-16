from aiogram import Dispatcher, types
import keyboards
import texts


async def check_subs(callback: types.CallbackQuery):
    text = texts.start()
    reply_markup = keyboards.inline.start()

    await callback.message.delete()
    await callback.message.answer(text=text, reply_markup=reply_markup)


async def other_callback(callback: types.CallbackQuery):
    await callback.answer(text="Скоро...")


def register_other_handlers(dp: Dispatcher):
    dp.callback_query.register(check_subs, lambda c: c.data == "check_subs")
    dp.callback_query.register(other_callback)
