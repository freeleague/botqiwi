import telebot
from telebot import types


def sub_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn2 = types.KeyboardButton('Узнать баланс💰')
    btn3 = types.KeyboardButton('Добавить кошельки💳')
    btn4 = types.KeyboardButton('Сделать перевод💱')
    btn10 = types.KeyboardButton('Назад🔙')
    markup.add(btn2, btn3)
    markup.add(btn4, btn10)
    return markup

def admin_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    btn6 = types.KeyboardButton('Узнать баланс💰')
    btn7 = types.KeyboardButton('Добавить кошельки💳')
    btn8 = types.KeyboardButton('Сделать перевод💱')
    btn9 = types.KeyboardButton('Выдать подписку✔')
    btn12 = types.KeyboardButton('Забрать подписку✖')
    btn13 = types.KeyboardButton('Статистика бота📈')
    btn14 = types.KeyboardButton('Рассылка💬')
    btn11 = types.KeyboardButton('Назад🔙')
    markup.add(btn6, btn7)
    markup.add(btn8, btn9)
    markup.add(btn11, btn12)
    markup.add(btn13, btn14)
    return markup


