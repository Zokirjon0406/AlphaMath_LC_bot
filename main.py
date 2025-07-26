import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

# Token va kanal username
TOKEN = '7617741780:AAHRnPEOJV5rRP21D7c_ycyXqsaxLG0hS6A'
CHANNEL_USERNAME = '@AlphaMath_LC'

# Logging
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# A'zolikni tekshirish funksiyasi
async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"A'zolikni tekshirishda xatolik: {e}")
        return False

# /start komandasi
@dp.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id
    is_subscribed = await check_subscription(user_id)

    if is_subscribed:
        await message.answer("✅ <b>AlphaMath botga xush kelibsiz!</b>\nAdmin: @thezakirovv")
    else:
        await message.answer(
            f"❗ <b>Siz {CHANNEL_USERNAME} kanaliga a’zo emassiz!</b>\n\n"
            f"Iltimos, <a href='https://t.me/{CHANNEL_USERNAME[1:]}'>kanalga a’zo bo‘ling</a> va /start buyrug‘ini qayta yuboring."
        )

# Asosiy ishga tushirish funksiyasi
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
