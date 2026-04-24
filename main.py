import telebot
from telebot import types
from flask import Flask
from threading import Thread
import time

# --- СЕРВЕР ДЛЯ RENDER ---
app = Flask('')
@app.route('/')
def home(): return "I am alive"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

# ТОКЕН ТВОЄЇ ВІЗИТКИ (ПЕРШИЙ БОТ)
TOKEN = '8682627312:AAHcQ2-cY-wuyxPHEMr0jT4kATwMqwfxZco'
bot = telebot.TeleBot(TOKEN)

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton("💰 Прайс та послуги")
    btn2 = types.KeyboardButton("📝 Замовити розробку")
    btn3 = types.KeyboardButton("👨‍💻 Написати майстру")
    markup.add(btn1, btn2, btn3)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привіт, {message.from_user.first_name}! 👋\nОберіть потрібний розділ меню:", reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "💰 Прайс та послуги":
        prices = "📊 **Наші послуги:**\n\n1️⃣ Бот-візитка — 800 грн\n2️⃣ Бот-анкета — 1 500 грн"
        bot.send_message(message.chat.id, prices, parse_mode='Markdown')
    elif message.text == "👨‍💻 Написати майстру":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Написати особисто 💬", url="https://t.me"))
        bot.send_message(message.chat.id, "Тисніть на кнопку нижче:", reply_markup=markup)
    elif message.text == "📝 Замовити розробку":
        bot.send_message(message.chat.id, "Який тип бота вас цікавить? (Візитка/Анкета/Магазин)")

if __name__ == "__main__":
    keep_alive()
    print("Візитка запущена...")
    bot.infinity_polling()
    
