from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.states.states import IdeaState
from bot.services.chatgpt_client import ask_chatgpt

router = Router()

@router.message(Command("idea"))
async def handle_idea_command(message: Message, state: FSMContext):
    await state.set_state(IdeaState.waiting_for_input)
    await message.answer("💡 Опиши свою идею, и я помогу её развить.")

@router.message(IdeaState.waiting_for_input)
async def handle_idea(message: Message, state: FSMContext):
    prompt = (
        "Ты — продуктовый дизайнер и креативный стратег. "
        f"Помоги развить идею: {message.text}. "
        "Предложи название, цель, первые шаги, возможные фичи и стиль общения."
    )
    response = await ask_chatgpt(prompt)
    await message.answer(f"<b>Развитие идеи:</b>\n{response}")
    await state.clear()

def register(dp):
    dp.include_router(router)