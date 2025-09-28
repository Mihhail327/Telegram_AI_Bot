from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.assets.prompts.personalities_prompt import PERSONALITIES

# 🎭 Эмодзи для персонажей
EMOJI = {
    "einstein": "🧠",
    "tarantino": "🎬",
    "kanye": "🎤",
    "tolstoy": "📚"
}

# 🧱 Утилита: создание кнопки
def btn(text: str, callback: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, callback_data=callback)

# 🏁 Главное меню
def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [btn("🎲 Факт", "open_random"), btn("💡 Идея", "open_idea")],
        [btn("💬 ChatGPT", "open_gpt"), btn("🧩 Алгоритм", "open_algo")],
        [btn("🖼️ Изображение", "open_image")],
        [btn("🎭 Поговорить с личностью", "open_personality")],
        [btn("💰 Квиз", "open_quiz")]
    ])

# 🔁 Общая кнопка "Назад"
def back_keyboard(callback_end: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[btn("🏁 Назад в меню", callback_end)]])

# 🎲 Факт
def random_fact_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [btn("🔁 Ещё факт", "random_again")],
        [btn("🏁 Назад в меню", "random_end")]
    ])

# 💡 Идея
def idea_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [btn("🔁 Ещё идею", "idea_again")],
        [btn("🏁 Назад в меню", "idea_end")]
    ])

# 💬 GPT стиль
def gpt_style_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [btn("🤓 Кратко", "style_short"), btn("📖 Подробно", "style_deep")],
        [btn("🎭 С юмором", "style_funny"), btn("🧘 Философски", "style_think")]
    ])

# 🧩 Алгоритм
def algo_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [btn("🔁 Ещё алгоритм", "algo_again")],
        [btn("🏁 Назад в меню", "algo_end")]
    ])

# 🖼️ Изображение
def image_keyboard() -> InlineKeyboardMarkup:
    return back_keyboard("image_end")

# 🎭 Персонажи (динамически из PERSONALITIES)
def personality_keyboard() -> InlineKeyboardMarkup:
    rows, row = [], []
    for i, (key, data) in enumerate(PERSONALITIES.items(), start=1):
        emoji = EMOJI.get(key, "👤")
        row.append(btn(f"{emoji} {data['name']}", f"persona_{key}"))
        if i % 2 == 0:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([btn("🏁 Назад в меню", "person_end")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

# 🔁 Повторный вопрос к персонажу
def personality_reply_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [btn("🔁 Задать ещё вопрос", "person_again")],
        [btn("🏁 Назад в меню", "person_end")]
    ])

# 💰 Квиз: варианты ответа
def quiz_keyboard(options: list[str]) -> InlineKeyboardMarkup:
    letters = [chr(65 + i) for i in range(len(options))]  # A, B, C, ...
    rows = [[btn(f"{letters[i]}: {opt}", f"quiz_answer_{i}")] for i, opt in enumerate(options)]
    rows.append([btn("🏁 Завершить игру", "quiz_end")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

# 💰 Квиз: статус
def quiz_status_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [btn("➡️ Следующий вопрос", "quiz_next")],
        [btn("🏁 Завершить игру", "quiz_end")]
    ])