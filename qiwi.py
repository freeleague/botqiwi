import telebot
from SimpleQIWI import *
from qiwi_keyboard import *
from qiwi_config import *
import sqlite3


@bot.message_handler(commands=['start'])
def start_message(message):
    inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
    inline = types.InlineKeyboardButton(text=f"Купить доступ", callback_data=f'BUY_')
    inline_keyboard.add(inline)
    bot.send_message(message.chat.id,
                     '💵Привет,чтобы пользоваться ботом, необходимо оплатить доступ', reply_markup=inline_keyboard)
    user_id = message.from_user.id
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS user(user_id INTEGER, access TEXT);""")
        cur.execute("SELECT * FROM user WHERE `user_id` = '{}'".format(user_id))
        row = cur.fetchall()
        if len(row) == 0:
            cur.execute("INSERT INTO `user` (`user_id`, `access`) VALUES(?,?)", (user_id, 'False',))
    chat_id = message.from_user.id
    with sqlite3.connect('users.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE `user_id` = '{}'".format(user_id))
        row = cur.fetchall()
        if row[0][0] == user_id and row[0][1] == 'True':
            bot.send_message(message.from_user.id, 'У вас есть доступ!', reply_markup=sub_keyboard())
    if chat_id in admin:
        bot.send_message(chat_id, 'Вы *админ*', parse_mode="Markdown",
                         reply_markup=admin_keyboard())


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if 'BUY_' in call.data:
        deposit(call, amount)
    elif 'STATUS-' in call.data:
        regex = call.data.split('-')
        user_status_pay(call, regex[1], regex[2])
    elif 'many_' in call.data:
        user_id = call.message.chat.id
        message = call.message
        bot.send_message(user_id, 'Введите номер кошелька и количество в виде: номер:сумма')
        bot.register_next_step_handler(message, pay_many)
    elif 'one_' in call.data:
        user_id = call.message.chat.id
        message = call.message
        bot.send_message(user_id, 'Введите номер кошелька с которого отправляем')
        bot.register_next_step_handler(message, one_number)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    try:
        chat_id = message.from_user.id
        if message.text == 'Добавить кошельки💳':
            bot.send_message(message.from_user.id, 'Напишите кошелек в виде: номер:токен', parse_mode="Markdown")
            bot.register_next_step_handler(message, add_qiwi)
        elif message.text == 'Узнать баланс💰':
            user_id = message.from_user.id
            with sqlite3.connect('users.db') as conn:
                cur = conn.cursor()
                cur.execute("SELECT `qiwi` FROM qiwi WHERE `user_id` = '{}'".format(user_id))
                row = cur.fetchall()
                for rows in row:
                    qiwi1 = str(rows[0])
                    qiwi = qiwi1.split(':')
                    phone = qiwi[0]
                    token = qiwi[1]
                    api = QApi(token=token, phone=phone)
                    bot.send_message(user_id, '💰Баланс кошелька ' + str(phone) + ' : ' + str(api.balance[0]) + '₽')
        elif message.text == 'Сделать перевод💱':
            inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
            inline = types.InlineKeyboardButton(text=f"Cо всех", callback_data=f'many_')
            inline1 = types.InlineKeyboardButton(text="С одного", callback_data='one_')
            inline_keyboard.add(inline, inline1)
            bot.send_message(message.from_user.id, 'Выберите', reply_markup=inline_keyboard)
        elif message.text == 'Выдать подписку✔' and chat_id in admin:
            bot.send_message(message.from_user.id, 'Введите id пользователя')
            bot.register_next_step_handler(message, give_sub)
        elif message.text == 'Забрать подписку✖' and chat_id in admin:
            bot.send_message(message.from_user.id, 'Введите id пользователя')
            bot.register_next_step_handler(message, remove_sub)
        elif message.text == 'Статистика бота📈' and chat_id in admin:
            user_id = message.from_user.id
            with sqlite3.connect('users.db') as conn:
                cur = conn.cursor()
                cur.execute("SELECT `access` FROM `user` WHERE `access` = '{}'".format('True'))
                row = cur.fetchall()
                bot.send_message(user_id, 'Кол-во пользователей купивших подписку: ' + str(len(row)))
        elif message.text == 'Рассылка💬' and chat_id in admin:
            message = bot.send_message(chat_id, '💁🏻‍♀️ Введите *сообщение* для рассылки', parse_mode="Markdown")
            bot.register_next_step_handler(message, add_message)
    except Exception as e:
        bot.send_message(message.from_user.id,
                         "Упс... что-то пошло не так, проверьте правильность заданных данных. Помощь: @faulmit")
        print(e)




bot.polling()

