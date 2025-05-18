# бот
import asyncio
from aiogram import Dispatcher

from app.handlers import router
from create_bot import bot

dp = Dispatcher()


async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
