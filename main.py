import asyncio
from aiogram import Dispatcher
from bot.core.bot import bot, storage
from bot.core.logger import setup_logger
from bot.handlers import start, random, gpt, idea, callbacks

logger = setup_logger()

async def main():
    dp = Dispatcher(storage=storage)

    start.register(dp)
    random.register(dp)
    gpt.register(dp)
    idea.register(dp)
    callbacks.register(dp)

    logger.info("Бот запущен")
    await dp.start_polling(bot, allowed_updates=["message", "callback_query"])

if __name__ == "__main__":
    asyncio.run(main())