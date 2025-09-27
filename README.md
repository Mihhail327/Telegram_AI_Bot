# 🤖 Telegram AI Bot

Интеллектуальный Telegram-бот на базе ChatGPT, с поддержкой генерации идей, фактов, алгоритмов и квизов. Построен на `aiogram 3`, с чистой архитектурой, FSM и модульной структурой.

---

## 🚀 Возможности

- `/start` — главное меню с inline-кнопками
- `/random` — генерация интересного факта
- `/gpt` — выбор стиля ответа и вопрос к ChatGPT
- `/idea` — генератор идей по описанию
- 📷 Распознавание изображений через GPT-4o (Vision)
- 🧩 Объяснение алгоритмов с примерами и аналогиями
- ❓ Квиз в стиле «Кто хочет стать миллионером»
- FSM-состояния для диалогов
- Асинхронные запросы к OpenAI
- Чистая архитектура, готовая к масштабированию
- Inline-кнопки: «Хочу ещё», «Закончить», «Вернуться»

---

## 🧱 Структура проекта

bot/ ├── core/ # Конфигурация, логгер, бот ├── handlers/ # Хендлеры по разделам ├── keyboards/ # Inline-клавиатуры ├──
services/ # ChatGPT API, генерация вопросов ├── states/ # FSM-состояния ├── assets/ # Промпты └── main.py # Точка входа


---

## ⚙️ Установка

```bash
git clone https://github.com/yourname/telegram-ai-bot.git
cd telegram-ai-bot
python3 -m venv .venv
source .venv/bin/activate
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
openai==1.3.5