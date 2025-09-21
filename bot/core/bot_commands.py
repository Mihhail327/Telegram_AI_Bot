from aiogram.types import BotCommand

def get_bot_command() -> list[BotCommand]:
    return [
        BotCommand(command="start", description="Главное меню"),
        BotCommand(command="random", description="Интересный факт"),
        BotCommand(command="gpt", description="Задать вопрос ChatGPT"),
        BotCommand(command="idea", description="Генератор идей"),
        BotCommand(command="algo", description="Объяснение алгоритма")
    ]