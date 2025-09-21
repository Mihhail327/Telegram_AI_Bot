from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🏁 Главное меню
def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Рандомный факт", callback_data="open_random")],
        [InlineKeyboardButton(text="💬 ChatGPT", callback_data="open_gpt")],
        [InlineKeyboardButton(text="💡 Генератор идей", callback_data="open_idea")],
    ])

# 🎲 Кнопки после факта
def random_fact_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Хочу ещё факт", callback_data="random_again")],
        [InlineKeyboardButton(text="🏁 Закончить", callback_data="random_end")]
    ])

# 💬 Выбор стиля GPT
def gpt_style_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🤓 Кратко", callback_data="style_short")],
        [InlineKeyboardButton(text="📖 Подробно", callback_data="style_deep")],
        [InlineKeyboardButton(text="🎭 С юмором", callback_data="style_funny")],
        [InlineKeyboardButton(text="🧘 Философски", callback_data="style_think")]
    ])