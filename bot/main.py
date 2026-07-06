import asyncio
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault, MenuButtonCommands

from keyboards import user, admin

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

dp.include_router(user.router)
dp.include_router(admin.router)


async def set_bot_commands():
    commands = [
        BotCommand(command="start", description="Запустити бота"),
        BotCommand(command="admin", description="Панель адміністратора"),
        BotCommand(command="help", description="Допомога"),
    ]

    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeDefault(),
    )

    await bot.set_chat_menu_button(
        menu_button=MenuButtonCommands()
    )


async def main():
    await set_bot_commands()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())