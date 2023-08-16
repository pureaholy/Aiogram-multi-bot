def start():
    return '<b>Добро пожаловать</b>'


def admin(users_count: int):
    return f"<b>Всего пользователей</b> - {users_count}\n\n" \
           f"<b>Отправка монет</b> - <code>/send_money user_id сумма</code>\n" \
           f"<b>Добавить админа</b> - <code>/add_admin user_id</code>"


def bots():
    return "<b>Здесь вы будете управлять своими ботами.</b>\n\n" \
           "1. <i>Добавлять|Удалять ботов</i>\n" \
           "2. <i>Изменять функции</i>"


def add_bot():
    return "<b>Создайте бота в <i>@botfather</i></b>\n\n" \
           "1. <i>Перейдите в <b>@botfather</b></i>\n" \
           "2. <i>Отправьте команду /newbot</i>\n" \
           "3. <i>Следуйте инструкциям</i>\n" \
           "4. <i>По окончанию бот выдаст вам токен бота, отправьте его мне</i>\n\n" \
           "<b>Пример токена:</b>\n<i>1937525622:AAFvrzkphMV0NPTGZ1amZAL3ezWrZtH2cmI</i>"


def bot_info(title, username, token):
    return f"<i>Настройки бота</i> - <b>{title}</b> | <b>@{username}</b>\n\n" \
           f"<code>{token}</code>"
