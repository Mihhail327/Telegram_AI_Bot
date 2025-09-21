import asyncio
from aiogram import Dispatcher
from bot.core.bot import bot, storage
from bot.core.logger import setup_logger
from bot.handlers import start, random, gpt, idea, callbacks, image, algo
from bot.core.bot_commands import get_bot_command

logger = setup_logger()


async def main():
    dp = Dispatcher(storage=storage)

    start.register(dp)
    random.register(dp)
    gpt.register(dp)
    idea.register(dp)
    callbacks.register(dp)
    image.register(dp)
    algo.register(dp)

    logger.info("Бот запущен")
    await dp.start_polling(bot, allowed_updates=["message", "callback_query"])
    await bot.set_my_commands(get_bot_command())


if __name__ == "__main__":
    asyncio.run(main())
