from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.states.states import GPTState
from bot.services.chatgpt_client import ask_chatgpt
from bot.keyboards.inline import gpt_style_keyboard

router = Router()

STYLE_PROMPTS = {
    "short": "Отвечай кратко и по делу.",
    "deep": "Объясни подробно, с примерами.",
    "funny": "Отвечай с юмором и игриво.",
    "think": "Отвечай философски, с размышлениями."
}

@router.message(Command("gpt"))
async def handle_gpt_command(message: Message, state: FSMContext):
    await state.set_state(GPTState.choosing_style)
    await message.answer("💬 Выберите стиль ответа:", reply_markup=gpt_style_keyboard())

@router.callback_query(F.data.startswith("style_"))
async def handle_style_choice(callback: CallbackQuery, state: FSMContext):
    style = callback.data.split("_")[1]
    await state.update_data(style=style)
    await state.set_state(GPTState.waiting_for_input)
    await callback.message.answer("✍️ Напиши вопрос, и я отвечу в выбранном стиле.")
    await callback.answer()

@router.message(GPTState.waiting_for_input)
async def handle_gpt_query(message: Message, state: FSMContext):
    data = await state.get_data()
    style = data.get("style", "short")
    prompt = f"{STYLE_PROMPTS[style]}\nВопрос: {message.text}"
    response = await ask_chatgpt(prompt)
    await message.answer(f"<b>Ответ ({style}):</b>\n{response}")
    await state.clear()

def register(dp):
    dp.include_router(router)