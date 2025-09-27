from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.keyboards.inline import random_fact_keyboard, start_keyboard
from bot.services.chatgpt_client import ask_chatgpt
from bot.core.logger import setup_logger
import os

router = Router()
logger = setup_logger()

FACT_PROMPT_PATH = "bot/assets/prompts/random.txt"

def load_prompt() -> str:
    if not os.path.exists(FACT_PROMPT_PATH):
        logger.warning("Файл промпта не найден, используется fallback.")
        return "Расскажи интересный факт."
    try:
        with open(FACT_PROMPT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Ошибка загрузки промпта: {e}")
        return "Расскажи интересный факт."


@router.message(Command("random"))
async def handle_random(message: Message, state: FSMContext):
    await state.clear()
    prompt = load_prompt()
    await message.answer("🎲 Генерирую интересный факт...")
    fact = await ask_chatgpt(prompt)
    await message.answer(f"<b>Факт:</b>\n{fact}", reply_markup=random_fact_keyboard())


@router.callback_query(F.data == "random_again")
async def handle_random_again(callback: CallbackQuery, state: FSMContext):
    prompt = load_prompt()
    fact = await ask_chatgpt(prompt)
    await callback.message.edit_text(f"<b>Факт:</b>\n{fact}", reply_markup=random_fact_keyboard())
    await callback.answer()


@router.callback_query(F.data == "random_end")
async def handle_random_end(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("🏁 Возврат в главное меню", reply_markup=start_keyboard())
    await callback.answer()


def register(dp):
    dp.include_router(router)