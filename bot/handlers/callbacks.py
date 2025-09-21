from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.handlers.random import handle_random
from bot.handlers.gpt import handle_gpt_command
from bot.handlers.idea import handle_idea_command

router = Router()

@router.callback_query(F.data == "open_random")
async def open_random(callback: CallbackQuery, state: FSMContext):
    await handle_random(callback.message, state)
    await callback.answer()

@router.callback_query(F.data == "open_gpt")
async def open_gpt(callback: CallbackQuery, state: FSMContext):
    await handle_gpt_command(callback.message, state)
    await callback.answer()

@router.callback_query(F.data == "open_idea")
async def open_idea(callback: CallbackQuery, state: FSMContext):
    await handle_idea_command(callback.message, state)
    await callback.answer()

def register(dp):
    dp.include_router(router)