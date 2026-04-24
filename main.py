import telebot
from telebot import types
from flask import Flask
from threading import Thread

# СЕРВЕР ДЛЯ RENDER
app = Flask('')
@app.route('/')
def home(): return "Shop Alive"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    Thread(target=run).start()

# ТВОЙ ПРАВИЛЬНЫЙ ТОКЕН
TOKEN = '8643102833:AAFT3-4fcuu5l5OOEeGloVBx83loSIKrVb0'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📱 Смартфони", "💻 Ноутбуки")
    bot.send_message(message.chat.id, "🛒 Привіт! Це демо-магазин:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "📱 Смартфони":
        bot.send_message(message.chat.id, "📱 Тут будуть iPhone!")
    elif message.text == "💻 Ноутбуки":
        bot.send_message(message.chat.id, "💻 Тут будуть MacBook!")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
    


