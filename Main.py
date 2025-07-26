import telebot
import os

TOKEN = os.getenv("7617741780:AAHRnPEOJV5rRP21D7c_ycyXqsaxLG0hS6A")
ADMIN_ID = os.getenv("5782061696")
CHANNEL_USERNAME = os.getenv("@AlphaMath_LC")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Bot ishlayapti! ✅")

bot.infinity_polling()
