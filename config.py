import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

# Чтение токена из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
OPEN_WEATHER_API = os.getenv("OPEN_WEATHER_API")


if not TOKEN:
    raise ValueError("Переменная окружения BOT_TOKEN не установлена!")