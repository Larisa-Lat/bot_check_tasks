from aiogram.exceptions import TelegramBadRequest

from aiogram.types import Message
from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from bot.utils.states import AddAdmin
from bot.admins_info.subloader_admins import add_admin

from bot.handlers.admin_commands.get_admins_cases_info import get_admins_info

router = Router()


@router.message(Command("add_admin"))
async def get_admins_info(message: Message, state: FSMContext) -> None:
    """Добавление админа"""
    await message.answer(text="Новый админ должен иметь приватный чат с ботом! \n"
                              "Введи username админа c @\n\n"
                              "Для отмены пришли 0")
    await state.set_state(AddAdmin.GET_ADMIN_NAME)


@router.message(AddAdmin.GET_ADMIN_NAME)
async def get_admin_name(message: Message, state: FSMContext) -> None:
    if message.text != "0":
        await state.update_data(admin_name=message.text)
        await message.answer(text="Введи user id админа\n"
                                  "Дай новуму админу право на редактирования в папке\n"
                                  "https://drive.google.com/drive/folders/19u0KGC1TXr6eQ2c5XKNJsgbhj-WKQb1S \n"
                                  "После добавления админа перезагрузить фоновый процесс на сервере\n"
                                  "Для отмены пришли 0")
        await state.set_state(AddAdmin.GET_ADMIN_ID)
    else:
        await state.clear()
        await message.answer(text="Отменено")


@router.message(AddAdmin.GET_ADMIN_ID)
async def get_admin_id(message: Message, state: FSMContext, bot: Bot) -> None:
    if message.text != "0" and message.text.isdigit():
        await state.update_data(admin_id=int(message.text))
        new_admin = await state.get_data()
        try:
            await bot.send_message(new_admin["admin_id"],
                                   text="Поздравляю ты новый админ бота - Pet_projects_case_bot")
        except TelegramBadRequest:
            await message.answer(text="Нет приватного чата нового админа с ботом ((")
        else:
            add_admin(new_admin)
            await message.answer(text="Готово")
            await get_admins_info(message)
    else:
        await message.answer(text="Отменено")
    await state.clear()
