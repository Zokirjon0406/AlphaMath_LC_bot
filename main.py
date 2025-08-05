# main.py
import logging
import random
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command

API_TOKEN = "7226387171:AAHtQ8bGpS7T5kr9PmQU4x8XSBG2mCeRO40"
ADMIN_ID = 5825805663  # Sizning Telegram ID'ingiz

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

full_test = []
correct_answers = {}
user_progress = {}

@dp.message(Command("newtest"))
async def load_test(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ Siz test yuklay olmaysiz.")
    
    global full_test, correct_answers
    text = message.text.split('\n')[1:]
    full_test = []
    correct_answers = {}

    question = {}
    q_number = 0

    for line in text:
        if line.strip() == "":
            continue
        if line[0].isdigit() and '.' in line:
            if question:
                full_test.append(question)
            q_number += 1
            question = {
                "q": line,
                "options": [],
                "correct": ""
            }
        elif line[0] in ['a', 'b', 'c', 'd'] and ')' in line:
            option_text = line[3:].strip()
            if '*' in option_text:
                question["correct"] = line[0]
                option_text = option_text.replace('*', '').strip()
            question["options"].append((line[0], option_text))
    
    if question:
        full_test.append(question)

    for idx, q in enumerate(full_test):
        correct_answers[idx] = q["correct"]

    await message.answer(f"✅ {len(full_test)} ta savol yuklandi.")

@dp.message(CommandStart())
async def start_test(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧪 Testni boshlash", callback_data="start_test")]
    ])
    await message.answer("Assalomu alaykum!\n🧮 Matematika test botiga xush kelibsiz.", reply_markup=keyboard)

@dp.callback_query(F.data == "start_test")
async def begin_test(callback: CallbackQuery):
    user_id = callback.from_user.id
    if not full_test:
        return await callback.message.answer("🚫 Hozircha test mavjud emas.")

    shuffled = list(enumerate(full_test))
    random.shuffle(shuffled)

    user_progress[user_id] = {
        "current": 0,
        "score": 0,
        "wrong": 0,
        "questions": shuffled,
        "answers": {}
    }

    await send_question(callback.message, user_id)

async def send_question(message: Message, user_id: int):
    progress = user_progress[user_id]
    idx, question = progress["questions"][progress["current"]]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{opt[0]}) {opt[1]}", callback_data=f"answer:{idx}:{opt[0]}")]
        for opt in question["options"]
    ])
    await message.answer(f"<b>{question['q']}</b>", reply_markup=keyboard)

@dp.callback_query(F.data.startswith("answer:"))
async def handle_answer(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in user_progress:
        return await callback.message.answer("⛔ Siz hali testni boshlamadingiz.")

    _, qidx, selected = callback.data.split(":")
    qidx = int(qidx)

    correct = correct_answers[qidx]
    progress = user_progress[user_id]
    progress["answers"][qidx] = selected

    if selected == correct:
        progress["score"] += 1
    else:
        progress["wrong"] += 1

    progress["current"] += 1

    if progress["current"] < len(progress["questions"]):
        await send_question(callback.message, user_id)
    else:
        total = len(progress["questions"])
        correct = progress["score"]
        wrong = progress["wrong"]
        await callback.message.answer(f"✅ Test yakunlandi!\n\n"
                                      f"To'g'ri javoblar soni: <b>{correct}</b>\n"
                                      f"Xato javoblar soni: <b>{wrong}</b>\n"
                                      f"Umumiy savollar: <b>{total}</b>")
        del user_progress[user_id]

logging.basicConfig(level=logging.INFO)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
