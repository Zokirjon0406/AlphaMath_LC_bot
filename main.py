import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
import asyncio

TOKEN = '7617741780:AAHRnPEOJV5rRP21D7c_ycyXqsaxLG0hS6A'
CHANNEL_USERNAME = '@AlphaMath_LC'  # Kanal username (Guruh emas!)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# A'zolikni tekshirish
async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# /start komandasi
@dp.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id
    is_subscribed = await check_subscription(user_id)

    if is_subscribed:
        await message.answer("✅ <b>AlphaMath botga xush kelibsiz!</b>\nAdmin: @thezakirovv")
    else:
        await message.answer(f"❗ <b>Siz {CHANNEL_USERNAME} kanaliga a’zo emassiz!</b>\n\nIltimos, avval kanalga a’zo bo‘ling va /start ni qayta yuboring.")

# Ishga tushirish
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
