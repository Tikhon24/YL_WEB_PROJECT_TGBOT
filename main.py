# бот
import requests
import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router

TOKEN_API = "8045924051:AAH0OKdt2dqkjQvRXII_CyhmfbxC_wbMaiI"

bot = Bot(TOKEN_API)
dp = Dispatcher()


async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
