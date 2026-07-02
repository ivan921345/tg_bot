import asyncio
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher

from keyboards import user, admin

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

dp.include_router(user.router)
dp.include_router(admin.router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())