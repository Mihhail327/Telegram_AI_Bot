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
from bot.assets.prompts.personalities_prompt import PERSONALITIES

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
@router.callback_query(F.data.startswith("persona_"))
async def handle_person_choice(callback: CallbackQuery, state: FSMContext):
    character_key = callback.data.removeprefix("persona_")
    character_data = PERSONALITIES.get(character_key)

    if not character_data:
        await callback.message.answer("❌ Неизвестный персонаж.")
        await callback.answer()
        return

    await state.set_state(PersonalityState.waiting_for_question)
    await state.update_data({
        "character_key": character_key,
        "dialog_history": []  # начинаем с пустой истории
    })

    await callback.message.edit_text(
        f"🗣️ Ты выбрал: {character_data['name']}. Задай вопрос.",
        reply_markup=None
    )
    await callback.answer()

# 💬 Вопрос к выбранной личности
@router.message(PersonalityState.waiting_for_question)
async def handle_person_question(msg: Message, state: FSMContext):
    data = await state.get_data()
    character_key = data.get("character_key")
    history = data.get("dialog_history", [])

    character_data = PERSONALITIES.get(character_key)
    if not character_data:
        await msg.answer("⚠️ Персонаж не найден. Пожалуйста, выбери его заново.", reply_markup=personality_keyboard())
        await state.set_state(PersonalityState.waiting_for_choice)
        return

    # Формируем prompt с историей
    history.append(f"Пользователь: {msg.text}")
    prompt = f"{character_data['prompt']}\nИстория:\n" + "\n".join(history)

    response = await ask_chatgpt(prompt) or "🤖 Не удалось получить ответ."
    history.append(f"{character_data['name']}: {response}")

    await msg.answer(
        f"<b>{character_data['name']} отвечает:</b>\n{response}",
        reply_markup=personality_reply_keyboard()
    )

    await state.update_data({"dialog_history": history})

# 🔁 Задать ещё вопрос
@router.callback_query(F.data == "person_again")
async def repeat_person_dialogue(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    character_key = data.get("character_key")
    character_data = PERSONALITIES.get(character_key)

    if not character_data:
        await callback.message.answer(
            "⚠️ Персонаж не найден. Пожалуйста, выбери его заново.",
            reply_markup=personality_keyboard()
        )
        await state.set_state(PersonalityState.waiting_for_choice)
        await callback.answer()
        return

    await callback.message.edit_text(
        f"🗣️ Ты снова общаешься с {character_data['name']}. Задай вопрос.",
        reply_markup=None
    )
    await callback.answer()

# 🏁 Назад в меню
@router.callback_query(F.data == "person_end")
async def end_personality(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await callback.message.delete()
    except Exception:
        pass
    await callback.message.answer("🏁 Главное меню:", reply_markup=start_keyboard())
    await callback.answer()

def register(dp):
    dp.include_router(router)