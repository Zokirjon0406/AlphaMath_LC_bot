from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Admin ID (faqat sizga xabar yuboriladi)
ADMIN_ID = 7226387171

# Kanal username (azolik tekshiruvi uchun)
CHANNEL_USERNAME = "@AlphaMath_LC"  # Kanal usernameni shu tarzda yozing

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Foydalanuvchi kanalga azo bo‘lganini tekshirish
    chat_member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user.id)
    if chat_member.status in ["member", "administrator", "creator"]:
        await update.message.reply_text("Assalomu alaykum! Xush kelibsiz 😊. Endi yozishingiz mumkin.")
    else:
        await update.message.reply_text(
            f"Botdan foydalanish uchun iltimos, kanalimizga a'zo bo‘ling: {CHANNEL_USERNAME}"
        )

# Oddiy xabarlar handleri
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Tekshiruv: kanalga azo bo‘lganmi
    chat_member = await context.bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user.id)
    if chat_member.status in ["member", "administrator", "creator"]:
        text = update.message.text
        # Adminga forward qilish
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"Yangi xabar: {text} \nKimdan: {user.full_name}")
        await update.message.reply_text("Xabaringiz qabul qilindi! Tez orada javob olasiz.")
    else:
        await update.message.reply_text(f"Iltimos, avval kanalga a'zo bo‘ling: {CHANNEL_USERNAME}")

# Botni ishga tushurish
def main():
    app = ApplicationBuilder().token("7226387171:AAHtQ8bGpS7T5kr9PmQU4x8XSBG2mCeRO40").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
