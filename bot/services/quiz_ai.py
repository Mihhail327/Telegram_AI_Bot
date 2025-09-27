import json
from typing import Dict, List, Optional, Set
from bot.services.chatgpt_client import ask_chatgpt

FALLBACK_QUESTIONS: List[Dict] = [
    {
        "q": "Какой элемент обозначается символом 'O'?",
        "options": ["Олово", "Кислород", "Золото", "Осмий"],
        "answer": 1,
        "explain": "O — это кислород, от латинского Oxygenium."
    },
    {
        "q": "Кто написал роман 'Война и мир'?",
        "options": ["Фёдор Достоевский", "Иван Тургенев", "Лев Толстой", "Александр Пушкин"],
        "answer": 2,
        "explain": "Автор — Лев Николаевич Толстой."
    },
    {
        "q": "Сколько будет 12 × 12?",
        "options": ["124", "144", "132", "122"],
        "answer": 1,
        "explain": "12 × 12 = 144."
    },
    {
        "q": "Столица Австралии?",
        "options": ["Сидней", "Канберра", "Мельбурн", "Перт"],
        "answer": 1,
        "explain": "Столица — Канберра, а не Сидней."
    },
    {
        "q": "Какая планета ближе всего к Солнцу?",
        "options": ["Венера", "Меркурий", "Марс", "Земля"],
        "answer": 1,
        "explain": "Меркурий — самая близкая к Солнцу."
    },
]

def validate_question(q: Dict) -> Optional[Dict]:
    if not isinstance(q, dict):
        return None
    if "q" not in q or "options" not in q or "answer" not in q or "explain" not in q:
        return None
    if not isinstance(q["options"], list) or len(q["options"]) != 4:
        return None
    if not isinstance(q["answer"], int) or q["answer"] not in range(4):
        return None
    if not isinstance(q["explain"], str):
        return None
    return q

async def generate_quiz_question(level: int, used: Set[str]) -> Dict:
    prompt = (
        "Сгенерируй один вопрос для квиза в стиле «Кто хочет стать миллионером».\n"
        "Формат строго JSON без пояснений:\n"
        "{"
        "\"q\": \"текст вопроса\", "
        "\"options\": [\"вариант A\", \"вариант B\", \"вариант C\", \"вариант D\"], "
        "\"answer\": индекс_правильного_варианта_от_0_до_3, "
        "\"explain\": \"краткое объяснение правильного ответа\""
        "}\n"
        f"Сложность: уровень {level} из 15."
    )

    for _ in range(5):
        try:
            raw = await ask_chatgpt(prompt)
            data = json.loads(raw)
            valid = validate_question(data)
            if valid and valid["q"] not in used:
                return valid
        except Exception:
            continue

    for fallback in FALLBACK_QUESTIONS:
        if fallback["q"] not in used:
            return fallback

    return FALLBACK_QUESTIONS[level % len(FALLBACK_QUESTIONS)]