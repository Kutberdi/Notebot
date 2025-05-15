import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.markdown import hbold
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import Router
from aiogram.client.default import DefaultBotProperties
from aiogram import BaseMiddleware
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)
user_notes = {}

@router.message(F.text.startswith("/save"))
async def save_note(message: Message):
    text = message.text[5:].strip()
    if text:
        user_notes.setdefault(message.from_user.id, []).append(text)
        await message.answer("✅ Заметка сохранена.")
    else:
        await message.answer("⚠️ Пожалуйста, укажи текст после команды /save")

@router.message(F.text == "/show")
async def show_notes(message: Message):
    notes = user_notes.get(message.from_user.id, [])
    if notes:
        reply = "\n\n".join(f"{i+1}. {note}" for i, note in enumerate(notes))
        await message.answer(f"<b>📝 Твои заметки:</b>\n\n{reply}")
    else:
        await message.answer("❌ У тебя нет сохранённых заметок.")

@router.message(F.text == "/clear")
async def clear_notes(message: Message):
    user_notes[message.from_user.id] = []
    await message.answer("🗑 Все заметки удалены.")

@router.message(F.text == "/start")
async def start_cmd(message: Message):
    await message.answer("Привет! Я бот для заметок.\nИспользуй /save, /show и /clear.")

# Запуск
if __name__ == "__main__":
    import asyncio

    async def main():
        await dp.start_polling(bot)

    asyncio.run(main())
