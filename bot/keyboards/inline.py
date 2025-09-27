from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# 🏁 Главное меню
def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Факт", callback_data="open_random"),
         InlineKeyboardButton(text="💡 Идея", callback_data="open_idea")],
        [InlineKeyboardButton(text="💬 ChatGPT", callback_data="open_gpt"),
         InlineKeyboardButton(text="🧩 Алгоритм", callback_data="open_algo")],
        [InlineKeyboardButton(text="🖼️ Изображение", callback_data="open_image")],
        [InlineKeyboardButton(text="🎭 Поговорить с личностью", callback_data="open_personality")],
        [InlineKeyboardButton(text="💰 Квиз", callback_data="open_quiz")]
    ])


# 🎲 Факт
def random_fact_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Ещё факт", callback_data="random_again")],
        [InlineKeyboardButton(text="🏁 Назад в меню", callback_data="random_end")]
    ])


# 💬 GPT стиль
def gpt_style_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🤓 Кратко", callback_data="style_short"),
         InlineKeyboardButton(text="📖 Подробно", callback_data="style_deep")],
        [InlineKeyboardButton(text="🎭 С юмором", callback_data="style_funny"),
         InlineKeyboardButton(text="🧘 Философски", callback_data="style_think")]
    ])


# 💡 Идея
def idea_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Ещё идею", callback_data="idea_again")],
        [InlineKeyboardButton(text="🏁 Назад в меню", callback_data="idea_end")]
    ])


# 🧩 Алгоритм
def algo_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Ещё алгоритм", callback_data="algo_again")],
        [InlineKeyboardButton(text="🏁 Назад в меню", callback_data="algo_end")]
    ])


# 🖼️ Изображение
def image_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏁 Назад в меню", callback_data="image_end")]
    ])


# 👥 Общение с известной личностью
def personality_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧠 Эйнштейн", callback_data="person_einstein"),
         InlineKeyboardButton(text="🎬 Тарантино", callback_data="person_tarantino")],
        [InlineKeyboardButton(text="🎤 Канье Уэст", callback_data="person_kanye"),
         InlineKeyboardButton(text="📚 Толстой", callback_data="person_tolstoy")],
        [InlineKeyboardButton(text="🏁 Назад в меню", callback_data="person_end")]
    ])


def personality_reply_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Задать ещё вопрос", callback_data="person_again")],
        [InlineKeyboardButton(text="🏁 Назад в меню", callback_data="person_end")]
    ])

def quiz_keyboard(options: list[str]) -> InlineKeyboardMarkup:
    letters = ["A", "B", "C", "D"]
    rows = [[InlineKeyboardButton(text=f"{letters[i]}: {opt}", callback_data=f"quiz_answer_{i}")]
            for i, opt in enumerate(options)]
    rows.append([InlineKeyboardButton(text="🏁 Завершить игру", callback_data="quiz_end")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

def quiz_status_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➡️ Следующий вопрос", callback_data="quiz_next")],
        [InlineKeyboardButton(text="🏁 Завершить игру", callback_data="quiz_end")]
    ])

