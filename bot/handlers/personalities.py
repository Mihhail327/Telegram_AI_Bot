from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from bot.states.states import PersonalityState
from bot.keyboards.inline import (
    personality_keyboard,
    personality_reply_keyboard,
    start_keyboard
)
from bot.services.chatgpt_client import ask_chatgpt

router = Router()

# 🎭 Старт фичи: выбор личности
@router.callback_query(F.data == "open_personality")
async def start_personality(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PersonalityState.waiting_for_choice)
    await callback.message.edit_text(
        "🎭 С кем хочешь поговорить?",
        reply_markup=personality_keyboard()
    )
    await callback.answer()

# ✅ Выбор персонажа
@router.callback_query(F.data.startswith("person_"))
async def handle_person_choice(callback: CallbackQuery, state: FSMContext):
    character = callback.data.split("_")[1]

    if character == "end":
        await state.clear()
        await callback.message.edit_text("🏁 Главное меню:", reply_markup=start_keyboard())
        await callback.answer()
        return

    await state.set_state(PersonalityState.waiting_for_question)
    await state.update_data({"character": character})
    await callback.message.edit_text(
        f"🗣️ Ты выбрал: {character.title()}. Задай вопрос.",
        reply_markup=None
    )
    await callback.answer()

# 💬 Вопрос к выбранной личности
@router.message(PersonalityState.waiting_for_question)
async def handle_person_question(msg: Message, state: FSMContext):
    data = await state.get_data()
    character = data.get("character", "неизвестный персонаж")

    prompt = (
        f"Представь, что ты {character.title()}. Ответь на вопрос пользователя в стиле этой личности.\n"
        f"Вопрос: {msg.text}"
    )

    response = await ask_chatgpt(prompt)
    sent = await msg.answer(
        f"<b>{character.title()} отвечает:</b>\n{response}",
        reply_markup=personality_reply_keyboard()
    )

    await state.update_data({"last_message_id": sent.message_id})
    await state.set_state(PersonalityState.waiting_for_question)

# 🔁 Задать ещё вопрос
@router.callback_query(F.data == "person_again")
async def repeat_person_dialogue(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    character = data.get("character", "неизвестный персонаж")

    await callback.message.edit_text(
        f"🗣️ Ты снова общаешься с {character.title()}. Задай вопрос.",
        reply_markup=None
    )
    await callback.answer()

# 🏁 Назад в меню
@router.callback_query(F.data == "person_end")
async def end_personality(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    try:
        await callback.message.delete()  # удаляем сообщение с диалогом
    except Exception:
        pass

    await callback.message.answer("🏁 Главное меню:", reply_markup=start_keyboard())
    await callback.answer()

def register(dp):
    dp.include_router(router)