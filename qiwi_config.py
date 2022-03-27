import telebot
from telebot import types

from SimpleQIWI import *
import json, os

import threading, random

from qiwi_keyboard import *

import sqlite3

import string

import datetime
from datetime import timedelta

from time import sleep

bot = telebot.TeleBot('5097135417:AAEcUEm_benBpN4zJsainD3gSKCbXSRPcbk')  # токен бота

admin = [1623380569] # айди одменов

amount = 60  # цена доступа

phone = '+79688066555' # твой номер телефона qiwi

token = 'b1b3d2e1b8e4364555847dba67ff347c' # твой токен кошелька киви

in_deposit = []

one_qiwi = []

def get_usersId_banker():
    try:
        array = []

        with sqlite3.connect("users.db") as con:
            cur = con.cursor()
            rows = cur.execute("SELECT * FROM user").fetchall()

            for row in rows:
                array.append(row[0])

        return array
    except Exception as e:
        print(e)


def add_message(message):
    try:
        if (message.text != 'Назад🔙'):
            rows = get_usersId_banker()
            for row in rows:
                bot.send_message(row, message.text)
    except:
        pass


def remove_sub(message):
    try:
        if message.text == 'Назад🔙':
            bot.send_message(message.from_user.id, 'Вы вернулись назад')
        else:
            user_id = message.text
            with sqlite3.connect('users.db') as conn:
                cur = conn.cursor()
                cur.execute("UPDATE `user` SET `access` = 'False' WHERE `user_id` = ?", (user_id,))
                bot.send_message(message.from_user.id, 'Подписка забрана!')
    except Exception as e:
        bot.send_message(message.from_user.id,
                         "Упс... что-то пошло не так, проверьте правильность заданных данных. Помощь: @faulmit")
        print(e)


def give_sub(message):
    try:
        if message.text == 'Назад🔙':
            bot.send_message(message.from_user.id, 'Вы вернулись назад')
        else:
            user_id = message.text
            with sqlite3.connect('users.db') as conn:
                cur = conn.cursor()
                cur.execute("UPDATE `user` SET `access` = 'True' WHERE `user_id` = ?", (user_id,))
                bot.send_message(message.from_user.id, 'Подписка выдана!')
    except Exception as e:
        bot.send_message(message.from_user.id,
                         "Упс... что-то пошло не так, проверьте правильность заданных данных. Помощь: @faulmit")
        print(e)

def pay_many(message):
    try:
        if message.text == 'Назад🔙':
            bot.send_message(message.from_user.id, 'Вы вернулись назад')
        else:
            user_id = message.from_user.id
            with sqlite3.connect('users.db') as conn:
                cur = conn.cursor()
                cur.execute("SELECT `qiwi` FROM qiwi WHERE `user_id` = '{}'".format(user_id))
                row = cur.fetchall()
                pay = str(message.text)
                split = pay.split(':')
                phone1 = split[0]
                amount1 = int(split[1])
                for rows in row:
                    qiwi1 = str(rows[0])
                    qiwi = qiwi1.split(':')
                    phone = qiwi[0]
                    token = qiwi[1]
                    print(phone, token)
                    api = QApi(token=token, phone=phone)
                    api.pay(account=phone1, amount=amount1, comment='')
    except Exception as e:
        bot.send_message(message.from_user.id, "Упс... что-то пошло не так, проверьте правильность заданных данных. Помощь: @faulmit")
        print(e)


def one_number(message):
    try:
        if message.text == 'Назад🔙':
            bot.send_message(message.from_user.id, 'Вы вернулись назад')
        else:
            one_qiwi.append(str(message.text))
            bot.send_message(message.chat.id, 'Введите номер кошелька и количество в виде: номер:сумма')
            bot.register_next_step_handler(message, pay_one)
    except Exception as e:
        bot.send_message(message.from_user.id,
                         "Упс... что-то пошло не так, проверьте правильность заданных данных. Помощь: @faulmit")
        print(e)

def pay_one(message):
    try:
        if message.text == 'Назад🔙':
            bot.send_message(message.from_user.id, 'Вы вернулись назад')
        else:
            user_id = message.from_user.id
            with sqlite3.connect('users.db') as conn:
                cur = conn.cursor()
                cur.execute("SELECT `qiwi` FROM qiwi WHERE `user_id` = '{}'".format(user_id))
                row = cur.fetchall()
                pay = str(message.text)
                split = pay.split(':')
                phone1 = split[0]
                amount1 = int(split[1])

                for rows in row:
                    qiwi1 = str(rows[0])
                    qiwi = qiwi1.split(':')
                    phone = qiwi[0]
                    if phone == one_qiwi[0]:
                        phone2 = one_qiwi[0]
                        token1 = qiwi[1]
                        api = QApi(token=token1, phone=phone2)
                        api.pay(account=phone1, amount=amount1, comment='')
                        one_qiwi.clear()
                        bot.send_message(user_id, 'Перевод успешно совершен')
                        break
    except Exception as e:
        bot.send_message(message.from_user.id,
                         "Упс... что-то пошло не так, проверьте правильность заданных данных. Помощь: @faulmit")
        print(e)

def add_qiwi(message):
    try:
        if message.text == 'Назад🔙':
            bot.send_message(message.from_user.id, 'Вы вернулись назад')
        else:
            msg = message.text
            user_id = message.from_user.id
            split = msg.split(':')
            number = split[0]
            tok = split[1]
            api = QApi(token=tok, phone=number)
            print(api.balance)
            with sqlite3.connect('users.db') as conn:
                cur = conn.cursor()
                cur.execute("""CREATE TABLE IF NOT EXISTS qiwi(user_id INTEGER, qiwi TEXT);""".format(user_id))
                cur.execute("INSERT INTO `qiwi`(`user_id`, `qiwi`) VALUES (?,?)",(int(user_id), str(message.text),))


            bot.send_message(message.from_user.id, 'Добавлен кошелек' + '\n' + 'Номер телефона: ' + str(number) + '\n' + 'Токен: ' + str(tok))
    except Exception as e:
        bot.send_message(message.from_user.id,
                         "Упс... что-то пошло не так, проверьте правильность заданных данных. Помощь: @faulmit")
        print(e)




def bill_create(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def deposit(call, amount):
    try:
        chat_id = call.message.chat.id

        billId = str(f'{bill_create(6)}_{random.randint(10000, 999999)}')

        inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
        inline_1 = types.InlineKeyboardButton(text="Проверить оплату",
                                              callback_data=f'STATUS-{billId}-{amount}')
        inline_keyboard.add(inline_1)
        message = bot.send_message(call.message.chat.id,
                                   f'💁🏻‍♀️ *Переведите* {str(amount)} ₽ на QIWI\nСчет действителен *10* минут\n\nНомер: `+{phone}`\nКомментарий: `{billId}`\n\n_Нажмите на реквизиты и комментарий чтобы их скопировать_',
                                   parse_mode="Markdown",
                                   reply_markup=inline_keyboard)


    except Exception as e:
        print(e)


def user_status_pay(call, billId, amount):
    chat_id = call.message.chat.id
    api = QApi(phone=phone, token=token)
    payments = api.payments['data']
    for info_payment in payments:
        if info_payment['comment'] == billId:
            if str(amount) == str(info_payment['sum']['amount']):
                bot.send_message(chat_id, '✅Вы купили доступ!✅', reply_markup=sub_keyboard())
                with sqlite3.connect('users.db') as conn:
                    cur = conn.cursor()
                    cur.execute("UPDATE `user` SET `access` = 'True' WHERE `user_id` = ?", (chat_id,))
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="💁🏻‍♀️ Платеж не найден")
