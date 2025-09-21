from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.keyboards.inline import start_keyboard

router = Router()

@router.message(Command("start"))
async def handle_start(message: Message):
    await message.answer(
        "👋 Привет! Я бот с ИИ. Выбери, что хочешь сделать:",
        reply_markup=start_keyboard()
    )

def register(dp):
    dp.include_router(router)