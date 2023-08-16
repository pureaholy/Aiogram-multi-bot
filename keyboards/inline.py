from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.databases import User, Bots
from config import sub_list
from misc.types import CallbackData
from misc.utils import can_delete_admin


def start():
    result = InlineKeyboardBuilder()
    result.row(InlineKeyboardButton(text="⚙️ Управлять ботами", callback_data=CallbackData.Start.bots()))
    return result.as_markup()


def bots(ls: list[list[Bots]], page_num=0):
    result = InlineKeyboardBuilder()
    len_ls = len(ls)
    count = page_num if len_ls != 1 else 0
    for i in ls[count]:
        result.row(InlineKeyboardButton(text=i.title, callback_data=CallbackData.Bots.select(i.bot_id)))
    if len_ls != 1:
        move_back = len_ls - 1 if page_num == 0 else page_num - 1
        move_next = 0 if page_num == len_ls - 1 else page_num + 1
        result.row(InlineKeyboardButton(text="⬅", callback_data=CallbackData.Bots.move(move_back)))
        result.add(InlineKeyboardButton(text=f"{page_num + 1}/{len_ls}", callback_data=f"None"))
        result.add(InlineKeyboardButton(text="➡", callback_data=CallbackData.Bots.move(move_next)))
    result.row(InlineKeyboardButton(text="Добавить бота", callback_data=CallbackData.Bots.new()))
    return result.as_markup()


def admin():
    result = InlineKeyboardBuilder()
    result.row(InlineKeyboardButton(text="📤 Рассылка", callback_data=CallbackData.Admin.ross()))
    result.add(InlineKeyboardButton(text="👑 Админы", callback_data=CallbackData.Admin.get_admins()))
    result.row(InlineKeyboardButton(text="👥 Получить базу данных", callback_data=CallbackData.Admin.get_db()))

    return result.as_markup()


def admin_list(ls: list[list[User]], owner_id: int, page_num=0):
    result = InlineKeyboardBuilder()
    len_ls = len(ls)
    count = page_num if len_ls != 1 else 0
    for i in ls[count]:
        callback_data = CallbackData.Admin.remove_admin(i.id)
        text_admin = f"{i.first_name} {i.last_name if i.last_name is not None else ''}"
        result.row(InlineKeyboardButton(text=text_admin, callback_data='None'))
        if can_delete_admin(owner_id=owner_id, user_id=i.user_id, is_admin=i.is_admin):
            result.add(InlineKeyboardButton(text="🗑 Удалить", callback_data=callback_data))
    if len(ls) != 1:
        move_back = len_ls - 1 if page_num == 0 else page_num - 1
        move_next = 0 if page_num == len_ls - 1 else page_num + 1

        callback_data_back = CallbackData.Admin.move_admins(move_back)
        callback_data_next = CallbackData.Admin.move_admins(move_next)

        result.row(InlineKeyboardButton(text=f"⬅", callback_data=callback_data_back))
        result.add(InlineKeyboardButton(text=f"{page_num + 1}/{len_ls}", callback_data=f"None"))
        result.add(InlineKeyboardButton(text=f"➡", callback_data=callback_data_next))

    result.row(InlineKeyboardButton(text="◀️ Назад", callback_data=CallbackData.Admin.main()))
    return result.as_markup()


def back_to_admin():
    result = InlineKeyboardBuilder()
    result.row(InlineKeyboardButton(text="◀️ Назад", callback_data=CallbackData.Admin.main()))
    return result.as_markup()


def confirm_ross():
    result = InlineKeyboardBuilder()
    confirm = InlineKeyboardButton(text="✅ Подтвердить", callback_data=CallbackData.Admin.confirm_ross())
    cancel = InlineKeyboardButton(text="❌ Отменить", callback_data=CallbackData.Admin.main())
    result.row(confirm).add(cancel)
    return result.as_markup()


def subscribe_chats(chat_list):
    result = InlineKeyboardBuilder()
    for chat_id in chat_list:
        link = sub_list[chat_id]['link']
        name = sub_list[chat_id]['name']
        result.row(InlineKeyboardButton(text=name, url=link))
    result.row(InlineKeyboardButton(text="☑️ Проверить", callback_data="check_subs"))
    return result.as_markup()


def back(to, main_menu: bool = False, cancel: bool = False):
    text = "◀️ Назад"
    if cancel is True:
        text = "❌ Отменить"
    if main_menu is True:
        text = "🔙 В главное меню"
    result = InlineKeyboardBuilder()
    result.add(InlineKeyboardButton(text=text, callback_data=to))
    return result.as_markup()


def bot_setting(bot_id):
    result = InlineKeyboardBuilder()
    result.row(InlineKeyboardButton(text='🔙 В главное меню', callback_data=CallbackData.Back.main_menu()))
    result.add(InlineKeyboardButton(text='✂️ Удалить бота', callback_data=CallbackData.Bots.remove(bot_id)))
    return result.as_markup()
