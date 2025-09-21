import aiohttp
from bot.core.config import settings
from bot.core.logger import setup_logger

logger = setup_logger()

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {settings.openai_key}",
    "Content-Type": "application/json"
}

async def ask_chatgpt(prompt: str) -> str:
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Ты дружелюбный Telegram-бот, отвечай ясно и полезно."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(OPENAI_API_URL, headers=HEADERS, json=payload) as response:
                if response.status != 200:
                    logger.error(f"OpenAI API error: {response.status}")
                    return "⚠️ Ошибка при обращении к ChatGPT."

                data = await response.json()
                return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        logger.exception(f"Ошибка запроса к OpenAI: {e}")
        return "⚠️ Не удалось получить ответ от ChatGPT."