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
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(OPENAI_API_URL, headers=HEADERS, json=payload) as response:
                if response.status != 200:
                    return "⚠️ Ошибка при обращении к ChatGPT."
                data = await response.json()
                return data["choices"][0]["message"]["content"].strip()
    except Exception:
        return "⚠️ Не удалось получить ответ от ChatGPT."

async def ask_chatgpt_with_image(image_url: str, instruction: str = "Опиши изображение кратко и точно.") -> str:
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": instruction},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    logger.info(f"📤 Отправка изображения в GPT-4o:\n{image_url}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(OPENAI_API_URL, headers=HEADERS, json=payload) as response:
                logger.info(f"📥 Статус ответа: {response.status}")
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"❌ Ошибка OpenAI: {error_text}")
                    return "⚠️ GPT-4o не смог обработать изображение."

                data = await response.json()
                reply = data["choices"][0]["message"]["content"].strip()
                logger.info(f"✅ Ответ GPT-4o:\n{reply}")
                return reply

    except Exception as e:
        logger.exception(f"❌ Исключение при запросе к GPT-4o: {e}")
        return "⚠️ Не удалось получить ответ от GPT-4o."