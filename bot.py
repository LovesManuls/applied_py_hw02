import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
# from handlers import setup_handlers
# from middlewares import LoggingMiddleware
# from handlers import questions, different_types
from set_profile import router as set_profile_router

# Создаем экземпляры бота и диспетчера
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Настраиваем middleware и обработчики
# dp.message.middleware(LoggingMiddleware())
# setup_handlers(dp)

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)


dp.include_routers(set_profile_router)

if __name__ == "__main__":
    asyncio.run(main())


