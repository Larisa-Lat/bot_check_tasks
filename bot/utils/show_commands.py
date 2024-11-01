from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def show_commands(bot: Bot):
    """ Меню команд бота для пользователей """
    commands = [
        BotCommand(
            command="info_cases",
            description="описание заданий кейсов и их айдишки"
        ),
        BotCommand(
            command="send_case",
            description="отправка кейса"
        ),
        BotCommand(
            command="instruction",
            description="инструкция"
        ),
        BotCommand(
            command="help",
            description="помощь здесь"
        ),
        BotCommand(
            command="settings",
            description="для админов"
        )
    ]
    await bot.set_my_commands(commands)
