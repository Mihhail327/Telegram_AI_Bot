from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.states.states import IdeaState
from bot.services.chatgpt_client import ask_chatgpt
from bot.keyboards.inline import idea_keyboard, start_keyboard

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
    await message.answer(f"<b>Развитие идеи:</b>\n{response}", reply_markup=idea_keyboard())
    await state.clear()


@router.callback_query(F.data == "idea_again")
async def handle_idea_repeat(callback: CallbackQuery, state: FSMContext):
    await state.set_state(IdeaState.waiting_for_input)
    await callback.message.answer("💡 Напиши новую идею, и я снова помогу её развить.")
    await callback.answer()


@router.callback_query(F.data == "idea_end")
async def handle_idea_end(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("🏁 Возврат в главное меню", reply_markup=start_keyboard())
    await callback.answer()


def register(dp):
    dp.include_router(router)
