import telebot
from telebot import types
from flask import Flask
from threading import Thread
import time

# --- СЕРВЕР ДЛЯ RENDER ---
app = Flask('')
@app.route('/')
def home(): return "Бот-візитка працює!"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

# ТОКЕН ТВОЕЙ ВИЗИТКИ
TOKEN = '8682627312:AAHcQ2-cY-wuyxPHEMr0jT4kATwMqwfxZco'
ADMIN_ID = 6863105636 
bot = telebot.TeleBot(TOKEN)

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add("💰 Прайс та послуги", "📝 Замовити розробку", "👨‍💻 Написати майстру")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привіт, {message.from_user.first_name}! 👋\nОберіть потрібний розділ меню:", reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "💰 Прайс та послуги":
        prices = (
            "📊 **Наші пропозиції:**\n\n"
            "1️⃣ **Бот-візитка** — 800 грн\n"
            "2️⃣ **Бот-анкета** — 1 500 грн\n"
            "3️⃣ **Бот-магазин** — від 4 000 грн\n\n"
            "🚀 **Не знайшли що шукали? Оберіть 'Інше' у замовленні!**"
        )
        bot.send_message(message.chat.id, prices, parse_mode='Markdown')
    
    elif message.text == "👨‍💻 Написати майстру":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Написати особисто 💬", url="https://t.me"))
        bot.send_message(message.chat.id, "Тисніть на кнопку нижче:", reply_markup=markup)

    elif message.text == "📝 Замовити розробку":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add("Візитка", "Анкета", "Магазин", "🚀 Інше")
        bot.send_message(message.chat.id, "Який тип бота вас цікавить?", reply_markup=markup)
        bot.register_next_step_handler(message, get_bot_type)

# Логика анкеты (как была раньше)
def get_bot_type(message):
    bot_type = message.text
    bot.send_message(message.chat.id, "Коротко опишіть вашу ідею чи бізнес:")
    bot.register_next_step_handler(message, get_biz, bot_type)

def get_biz(message, bot_type):
    biz_desc = message.text
    bot.send_message(message.chat.id, "Як до вас звертатися? (Ім'я або телефон)")
    bot.register_next_step_handler(message, get_contact, bot_type, biz_desc)

def get_contact(message, bot_type, biz_desc):
    contact = message.text
    user = f"@{message.from_user.username}" if message.from_user.username else "Приховано"
    bot.send_message(message.chat.id, "✅ Дякую! Заявку прийнято. Я скоро напишу вам.", reply_markup=main_menu())
    
    report = (f"🔥 **НОВА ЗАЯВКА!**\n\n"
              f"🕹 Тип: {bot_type}\n"
              f"📋 Опис: {biz_desc}\n"
              f"👤 Клієнт: {contact}\n"
              f"🔗 Юзер: {user}")
    bot.send_message(ADMIN_ID, report)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
    
