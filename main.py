import telebot

TOKEN = '7617741780:AAHRnPEOJV5rRP21D7c_ycyXqsaxLG0hS6A'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Assalomu alaykum, AlphaMath botga xush kelibsiz!")

bot.infinity_polling()
