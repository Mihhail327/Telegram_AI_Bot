import asyncio
from aiogram import Dispatcher
from bot.core.bot import bot, storage
from bot.core.logger import setup_logger
from bot.core.bot_commands import get_bot_command
from bot.handlers import all_handlers_router

logger = setup_logger()

async def main():
    dp = Dispatcher(storage=storage)
    dp.include_router(all_handlers_router)
    await bot.set_my_commands(get_bot_command())
    logger.info("Бот запущен")
    await dp.start_polling(bot, allowed_updates=["message", "callback_query"])

if __name__ == "__main__":
    asyncio.run(main())