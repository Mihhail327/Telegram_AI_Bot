import json
from typing import Dict, List, Optional, Set
from bot.services.chatgpt_client import ask_chatgpt

class QuizQuestion:
    def __init__(self, q: str, options: List[str], answer: int, explain: str, points: int = 100):
        self.q = q
        self.options = options
        self.answer = answer
        self.explain = explain
        self.points = points

    def to_dict(self) -> Dict:
        return {
            "q": self.q,
            "options": self.options,
            "answer": self.answer,
            "explain": self.explain,
            "points": self.points
        }

    @staticmethod
    def from_dict(data: Dict) -> Optional["QuizQuestion"]:
        if not isinstance(data, dict):
            return None
        if "q" not in data or "options" not in data or "answer" not in data or "explain" not in data:
            return None
        if not isinstance(data["options"], list) or len(data["options"]) != 4:
            return None
        if not isinstance(data["answer"], int) or data["answer"] not in range(4):
            return None
        if not isinstance(data["explain"], str):
            return None
        return QuizQuestion(
            q=data["q"],
            options=data["options"],
            answer=data["answer"],
            explain=data["explain"],
            points=data.get("points", 100)
        )

FALLBACK_QUESTIONS: List[QuizQuestion] = [
    QuizQuestion("Какой элемент обозначается символом 'O'?", ["Олово", "Кислород", "Золото", "Осмий"], 1, "O — это кислород, от латинского Oxygenium."),
    QuizQuestion("Кто написал роман 'Война и мир'?", ["Фёдор Достоевский", "Иван Тургенев", "Лев Толстой", "Александр Пушкин"], 2, "Автор — Лев Николаевич Толстой."),
    QuizQuestion("Сколько будет 12 × 12?", ["124", "144", "132", "122"], 1, "12 × 12 = 144."),
    QuizQuestion("Столица Австралии?", ["Сидней", "Канберра", "Мельбурн", "Перт"], 1, "Столица — Канберра, а не Сидней."),
    QuizQuestion("Какая планета ближе всего к Солнцу?", ["Венера", "Меркурий", "Марс", "Земля"], 1, "Меркурий — самая близкая к Солнцу.")
]

async def generate_quiz_question(level: int, used: Set[str]) -> QuizQuestion:
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
            question = QuizQuestion.from_dict(data)
            if question and question.q not in used:
                return question
        except Exception:
            continue

    for fallback in FALLBACK_QUESTIONS:
        if fallback.q not in used:
            return fallback

    return FALLBACK_QUESTIONS[level % len(FALLBACK_QUESTIONS)]

def check_answer(question: QuizQuestion, index: int) -> bool:
    return question.answer == index