from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from bot.states.states import AlgoState
from bot.services.chatgpt_client import ask_chatgpt
from bot.keyboards.inline import algo_keyboard, start_keyboard

router = Router()


@router.callback_query(F.data == "open_algo")
async def start_algo_mode(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AlgoState.waiting_for_name)
    await callback.message.answer("🧩 Напиши название алгоритма, и я объясню его простыми словами.")
    await callback.answer()


@router.message(AlgoState.waiting_for_name)
async def handle_algo(message: Message, state: FSMContext):
    algo_name = message.text.strip()
    prompt = (
        f"Объясни алгоритм '{algo_name}' простыми словами. "
        "Добавь пример, аналогию из жизни, и короткий псевдокод. "
        "Если алгоритм сложный — разбей объяснение на шаги."
    )
    response = await ask_chatgpt(prompt)
    await message.answer(f"<b>Объяснение:</b>\n{response}", reply_markup=algo_keyboard())
    await state.clear()


@router.callback_query(F.data == "algo_again")
async def handle_algo_repeat(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AlgoState.waiting_for_name)
    await callback.message.answer("🧩 Напиши новый алгоритм, и я снова объясню его.")
    await callback.answer()


@router.callback_query(F.data == "algo_end")
async def handle_algo_end(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("🏁 Возврат в главное меню", reply_markup=start_keyboard())
    await callback.answer()


def register(dp):
    dp.include_router(router)
