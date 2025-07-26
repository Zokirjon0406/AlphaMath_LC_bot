import telebot

TOKEN = '7617741780:AAHRnPEOJV5rRP21D7c_ycyXqsaxLG0hS6A'
bot = telebot.TeleBot(TOKEN)

# Guruhga xush kelibsiz
@bot.message_handler(content_types=['new_chat_members'])
def greet_new_member(message):
    for user in message.new_chat_members:
        bot.send_message(
            message.chat.id,
            f"👋 Xush kelibsiz, {user.first_name}!\n\nSizni guruhda ko‘rib turganimizdan xursandmiz!\nBot admin: @thezakirovv"
        )

# Start komandasi
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(
        message.chat.id,
        "Assalomu alaykum, AlphaMath_LC_bot ga xush kelibsiz!\nIltimos, kanalga a'zo bo‘ling: @AlphaMath_LC"
    )

bot.infinity_polling()
