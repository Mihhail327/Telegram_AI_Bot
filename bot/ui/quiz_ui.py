from aiogram import Bot
from aiogram.fsm.context import FSMContext

class QuizUIManager:
    async def cleanup_previous(self, chat_id: int, state: FSMContext):
        data = await state.get_data()
        msg_id = data.get("last_score_msg_id")
        if msg_id:
            try:
                bot: Bot = state.bot
                await bot.delete_message(chat_id, msg_id)
            except Exception:
                pass

    def render_progress_bar(self, current: int, total: int, length: int = 15) -> str:
        filled = int((current / total) * length)
        return "▮" * filled + "▯" * (length - filled)