import asyncio
from aiogram import Bot, Dispatcher, F
from bot.handlers import user_commands
from bot.utils import alert_admins
from bot.handlers.admin_commands import settings_command
from bot.handlers.user_commands import user_commands
from bot.handlers.user_commands import case_command, default_react_text

from os import getenv
from dotenv import load_dotenv

import logging


dp = Dispatcher()
dp.message.filter(
    F.chat.func(lambda chat: chat.type == "private")
)

load_dotenv()
TOKEN = getenv("BOT_TOKEN4")
bot = Bot(TOKEN)


async def start():
    dp.startup.register(alert_admins.start_bot)
    dp.shutdown.register(alert_admins.stop_bot)

    # Создаем логгер
    logger = logging.getLogger("main_logger")
    logger.setLevel(logging.DEBUG)
    FORMAT = '%(asctime)s / %(name)s:%(lineno)s / %(levelname)s / %(message)s\n\n'

    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(logging.Formatter(FORMAT))

    fh = logging.FileHandler(filename="logs/log.txt")
    fh.setFormatter(logging.Formatter(FORMAT))
    fh.setLevel(logging.INFO)

    logger.addHandler(sh)
    logger.addHandler(fh)


    try:
        dp.include_routers(
            case_command.router,
            user_commands.router,
            settings_command.router,
            default_react_text.router
        )

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print("Exit")

