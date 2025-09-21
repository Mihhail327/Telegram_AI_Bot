# 🤖 Telegram AI Bot

Интеллектуальный Telegram-бот на базе ChatGPT, с поддержкой стилей ответа, генерации идей и интересных фактов. Построен на `aiogram 3`, с чистой архитектурой и FSM.

---

## 🚀 Возможности

- `/start` — главное меню с кнопками
- `/random` — генерация интересного факта
- `/gpt` — выбор стиля ответа и вопрос к ChatGPT
- `/idea` — генератор идей по описанию
- 📷 Распознавание изображений через GPT-4o
- 🧩 Объяснение алгоритмов с примерами и аналогиями
- FSM-состояния для диалогов
- Inline-кнопки: «Хочу ещё», «Закончить», «Вернуться»
- Чистая архитектура, готовая к масштабированию
- FSM-состояния для диалогов
- Асинхронные запросы к OpenAI
- Чистая архитектура, готовая к масштабированию

---

## 🧱 Структура проекта
bot/ 
    ├── core/          # Конфигурация, логгер, бот 
    ├── handlers/      # Хендлеры по разделам 
    ├── keyboards/     # Inline-клавиатуры 
    ├── services/      # ChatGPT API   
    ├── states/        # FSM-состояния 
    ├── assets/        # Промпты 
└── main.py        # Точка входа

---

## ⚙️ Установка

```bash
git clone https://github.com/yourname/telegram-ai-bot.git
cd telegram-ai-bot
pip install -r requirements.txt

🔐 Настройка .env
Создай файл .env в корне проекта:
BOT_TOKEN=your-telegram-token
OPENAI_KEY=your-openai-api-key

▶️ Запуск
python main.py



📦 Зависимости
aiogram==3.4.1
aiohttp==3.9.5
pydantic==2.5.3
pydantic-settings==2.2.1
python-dotenv==1.0.1
