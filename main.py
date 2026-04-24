import telebot
from telebot import types
from flask import Flask
from threading import Thread
import os
import time

# --- НАСТРОЙКИ ---
TOKEN = '8682627312:AAFo_FhHzHjTkvfN94c-CD0zq0glHR3_mFc'
ADMIN_ID = 6863105636 
MY_USERNAME = 'MuichiroHGP'

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# --- СЕРВЕР ДЛЯ RENDER ---
@server.route("/")
def webhook():
    return "Бот работает!", 200

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server.run(host="0.0.0.0", port=port)

# --- ЛОГИКА БОТА ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💰 Прайс та послуги", "📝 Замовити розробку", "👨‍💻 Написати майстру")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привіт! Я допоможу вам з розробкою бота.", reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "💰 Прайс та послуги":
        text = "1️⃣ Бот-візитка — 800 грн\n2️⃣ Бот-анкета — 1 500 грн\n3️⃣ Бот-магазин — від 4 000 грн"
        bot.send_message(message.chat.id, text)
    elif message.text == "👨+💻 Написати майстру":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("Написати особисто 💬", url=f"https://t.me{MY_USERNAME}")
        markup.add(btn)
        bot.send_message(message.chat.id, "Тисніть на кнопку:", reply_markup=markup)
    elif message.text == "📝 Замовити розробку":
        bot.send_message(message.chat.id, "Який тип бота вас цікавить?")
        bot.register_next_step_handler(message, get_bot_type)

def get_bot_type(message):
    bot_type = message.text
    bot.send_message(message.chat.id, "Коротко опишіть ідею:")
    bot.register_next_step_handler(message, get_biz, bot_type)

def get_biz(message, bot_type):
    desc = message.text
    bot.send_message(message.chat.id, "Як до вас звертатися?")
    bot.register_next_step_handler(message, send_report, bot_type, desc)

def send_report(message, bot_type, desc):
    contact = message.text
    bot.send_message(message.chat.id, "✅ Дякую! Заявку прийнято.", reply_markup=main_menu())
    report = f"🔥 ЗАЯВКА!\nТип: {bot_type}\nОпис: {desc}\nКлієнт: {contact}"
    bot.send_message(ADMIN_ID, report)

# --- ЗАПУСК ---
if __name__ == "__main__":
    Thread(target=run_server).start()
    print("Бот запущен успешно!")
    bot.infinity_polling(skip_pending=True)
    
