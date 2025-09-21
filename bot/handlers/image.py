from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.states.states import ImageState
from bot.core.bot import bot
from bot.services.chatgpt_client import ask_chatgpt_with_image
from bot.keyboards.inline import start_keyboard

router = Router()

@router.callback_query(F.data == "open_image")
async def start_image_mode(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ImageState.waiting_for_photo)
    await callback.message.answer("📷 Отправь изображение, и я постараюсь описать его.")
    await callback.answer()

@router.message(ImageState.waiting_for_photo)
async def handle_photo(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("⚠️ Пожалуйста, отправь изображение.")
        return

    photo = message.photo[-1]  # самое большое изображение
    file = await bot.get_file(photo.file_id)
    image_url = f"https://api.telegram.org/file/bot{bot.token}/{file.file_path}"

    await message.answer("🖼️ Отправляю изображение в GPT-4o...")
    response = await ask_chatgpt_with_image(image_url)
    await message.answer(f"<b>Описание:</b>\n{response}", reply_markup=start_keyboard())
    await state.clear()

def register(dp):
    dp.include_router(router)
