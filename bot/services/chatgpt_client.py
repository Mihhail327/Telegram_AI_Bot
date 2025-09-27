import aiohttp
from bot.core.config import settings
from bot.core.logger import setup_logger

logger = setup_logger()

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def get_headers() -> dict:
    if not settings.openai_key:
        logger.error("❌ OpenAI ключ не задан.")
        return {}
    return {
        "Authorization": f"Bearer {settings.openai_key}",
        "Content-Type": "application/json"
    }

async def ask_chatgpt(prompt: str, model: str = "gpt-3.5-turbo", temperature: float = 0.7) -> str:
    headers = get_headers()
    if not headers:
        return "⚠️ Ключ OpenAI не найден."

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }

    logger.info(f"📤 Отправка запроса в ChatGPT:\n{prompt}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(OPENAI_API_URL, headers=headers, json=payload) as response:
                logger.info(f"📥 Статус ответа: {response.status}")
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"❌ Ошибка OpenAI: {error_text}")
                    return "⚠️ Ошибка при обращении к ChatGPT."

                data = await response.json()
                choices = data.get("choices")
                if not choices:
                    logger.error(f"❌ Пустой ответ от OpenAI: {data}")
                    return "⚠️ ChatGPT не вернул результат."

                reply = choices[0]["message"]["content"].strip()
                logger.info(f"✅ Ответ ChatGPT:\n{reply}")
                return reply

    except Exception as e:
        logger.exception(f"❌ Исключение при запросе к ChatGPT: {e}")
        return "⚠️ Не удалось получить ответ от ChatGPT."

async def ask_chatgpt_with_image(image_url: str, instruction: str = "Опиши изображение кратко и точно.") -> str:
    headers = get_headers()
    if not headers:
        return "⚠️ Ключ OpenAI не найден."

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
            async with session.post(OPENAI_API_URL, headers=headers, json=payload) as response:
                logger.info(f"📥 Статус ответа: {response.status}")
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"❌ Ошибка OpenAI: {error_text}")
                    return "⚠️ GPT-4o не смог обработать изображение."

                data = await response.json()
                choices = data.get("choices")
                if not choices:
                    logger.error(f"❌ Пустой ответ от GPT-4o: {data}")
                    return "⚠️ GPT-4o не вернул результат."

                reply = choices[0]["message"]["content"].strip()
                logger.info(f"✅ Ответ GPT-4o:\n{reply}")
                return reply

    except Exception as e:
        logger.exception(f"❌ Исключение при запросе к GPT-4o: {e}")
        return "⚠️ Не удалось получить ответ от GPT-4o."