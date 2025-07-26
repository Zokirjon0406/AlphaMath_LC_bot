import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatMemberUpdated, ChatJoinRequest
from aiogram.filters import CommandStart, ChatMemberUpdatedFilter
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.utils.keyboard import InlineKeyboardBuilder
import asyncio
import os

# Token va konfiguratsiya
BOT_TOKEN = "7617741780:AAHRnPEOJV5rRP21D7c_ycyXqsaxLG0hS6A"
GROUP_ID = -1002135132927  # @AlphaMath_LCgroup ni IDsi
CHANNEL_ID = "@AlphaMath_LC"  # Ko‘rsatadigan kanal username
ADMIN_USERNAME = "@thezakirovv"  # Admin username

# Bot va disp
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# Inline tugma yasovchi
def join_button():
    builder = InlineKeyboardBuilder()
    builder.button(text="➕ Guruhga azo bo‘lish", url=f"https://t.me/{CHANNEL_ID.strip('@')}")
    return builder.as_markup()

# 1. /start komandasi — guruhga azo bo‘lmaganlarni tekshiradi
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    try:
        user = await bot.get_chat_member(GROUP_ID, message.from_user.id)
        if user.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
            await message.answer("❗ Iltimos, botdan foydalanish uchun guruhga azo bo‘ling:", reply_markup=join_button())
        else:
            await message.answer("✅ Xush kelibsiz! Siz guruhga azosiz!")
    except Exception as e:
        await message.answer("❗ Xatolik yuz berdi yoki siz hali guruhda emassiz.")
        print(e)

# 2. Yangi a’zo kirganda kutib olish
@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=True))
async def greet_new_user(event: ChatMemberUpdated):
    if event.new_chat_member.status == ChatMemberStatus.MEMBER:
        user_mention = event.from_user.mention_html()
        await bot.send_message(
            event.chat.id,
            f"👋 Xush kelibsiz, {user_mention}!\n\nAgar sizga yordam kerak bo‘lsa, admin: {ADMIN_USERNAME}",
            parse_mode="HTML"
        )

# Ishga tushurish
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
