# Botni ishga tushurish
def main():
    app = ApplicationBuilder().token("7226387171:AAHtQ8bGpS7T5kr9PmQU4x8XSBG2mCeRO40").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
