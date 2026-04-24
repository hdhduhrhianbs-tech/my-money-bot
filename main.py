import telebot
from telebot import types
import time

TOKEN = '8682627312:AAHcQ2-cY-wuyxPHEMr0jT4kATwMqwfxZco'
ADMIN_ID = 6863105636 
MY_USERNAME = 'MuichiroHGP'

bot = telebot.TeleBot(TOKEN, threaded=False)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton("💰 Прайс та послуги")
    btn2 = types.KeyboardButton("📝 Замовити розробку")
    btn3 = types.KeyboardButton("👨‍💻 Написати майстру")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, f"Привіт! 👋 Я створюю ботів для бізнесу.\nОберіть пункт меню: 👇", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "💰 Прайс та послуги":
        prices = ("📊 **Наші пропозиції:**\n\n1️⃣ Візитка — 800 грн\n2️⃣ Анкета — 1500 грн\n3️⃣ Магазин — від 4000 грн")
        bot.send_message(message.chat.id, prices, parse_mode='Markdown')
    elif message.text == "👨‍💻 Написати майстру":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("Написати особисто 💬", url=f"tg://resolve?domain={MY_USERNAME}")
        markup.add(btn)
        bot.send_message(message.chat.id, "Тисніть кнопку:", reply_markup=markup)
    elif message.text == "📝 Замовити розробку":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add("Візитка", "Анкета", "Магазин", "🚀 Інше")
        bot.send_message(message.chat.id, "Що саме вас цікавить?", reply_markup=markup)
        bot.register_next_step_handler(message, get_bot_type)

def get_bot_type(message):
    bot_type = message.text
    bot.send_message(message.chat.id, "Опишіть вашу ідею:")
    bot.register_next_step_handler(message, get_biz, bot_type)

def get_biz(message, bot_type):
    biz = message.text
    bot.send_message(message.chat.id, "Ваше ім'я або телефон?")
    bot.register_next_step_handler(message, get_contact, bot_type, biz)

def get_contact(message, bot_type, biz):
    user = f"@{message.from_user.username}" if message.from_user.username else "Приховано"
    bot.send_message(message.chat.id, "✅ Заявку прийнято!")
    report = (f"🔥 ЗАМОВЛЕННЯ!\n🕹 Тип: {bot_type}\n📋 Опис: {biz}\n👤 Клієнт: {message.text}\n🔗 Юзер: {user}")
    bot.send_message(ADMIN_ID, report)

while True:
    try:
        bot.polling(none_stop=True, timeout=90)
    except Exception:
        time.sleep(5)
      
