def save_to_csv(user_id, name, age):
    import os
    os.makedirs('/tmp/data', exist_ok=True)  # Создаем папку, если её нет
    with open('/tmp/data/responses.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, name, age])


import csv
import telebot
from telebot.apihelper import send_message
from telebot import types
from telebot.types import (ReplyKeyboardMarkup, KeyboardButton,
                          ReplyKeyboardRemove, InlineKeyboardMarkup,
                          InlineKeyboardButton)

bot = telebot.TeleBot('7376838326:AAFcVYOPhlhZFLsrU6I-7jAWSDZ0MPamyKo')


# Функция сохранения в CSV
def save_to_csv(user_id, name, age):
    with open('responses.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, name, age])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("📝 Заполнить анкету")
    markup.add(btn)
    bot.send_message(message.chat.id, "Привет! Нажми кнопку ниже.", reply_markup=markup)


@bot.message_handler(func=lambda m: m.text == "📝 Заполнить анкету")
def start_form(message):
    bot.send_message(message.chat.id, "Как тебя зовут?", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, ask_age)


def ask_age(message):
    name = message.text
    bot.send_message(message.chat.id, "Сколько тебе лет?")
    bot.register_next_step_handler(message, lambda m: save_data(m, name))


def save_data(message, name):
    age = message.text
    save_to_csv(message.from_user.id, name, age)

    # Создаем кнопку-ссылку на канал
    markup = InlineKeyboardMarkup()
    btn_channel = InlineKeyboardButton("🔥 Присоединиться к чату", url="https://t.me/vgostyah_u_yanin")
    markup.add(btn_channel)

    # Финальное сообщение
    bot.send_message(
        message.chat.id,
        f"Спасибо, {name}, что прошли анкетирование! 🎉\n\n"
        "А теперь добро пожаловать в наш уютный чатец! 👇",
        reply_markup=markup
    )

    
if __name__ == "__main__":
    (bot.polling(non_stop=True))
