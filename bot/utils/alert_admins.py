from aiogram import Bot
from bot.admins_info.subloader_admins import get_admins_id
from aiogram.exceptions import TelegramBadRequest
import logging
from bot.utils.show_commands import show_commands
logger = logging.getLogger("main_logger.start_end_bot")


async def start_bot(bot: Bot) -> None:
    """ Уведомление о начале работы бота админам и автоматический запуск меню команд"""
    await show_commands(bot)
    try:
        for send_to in get_admins_id():
            await bot.send_message(send_to, text='Бот запущен!')
    except TelegramBadRequest as err:
        logger.exception("inaccessible_admin")


async def stop_bot(bot: Bot) -> None:
    """ Уведомление об окончании работы бота админам"""
    try:
        for send_to in get_admins_id():
            await bot.send_message(send_to, text='Бот остановлен!')
    except TelegramBadRequest as err:
        logger.exception("inaccessible_admin")


async def alert_admins(bot: Bot, exception: str):
    try:
        for send_to in get_admins_id():
            await bot.send_message(send_to, text=exception)
    except TelegramBadRequest as err:
        logger.exception("inaccessible_admin")