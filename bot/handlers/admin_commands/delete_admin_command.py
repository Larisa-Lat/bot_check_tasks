from aiogram.types import Message
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from bot.utils.states import DeleteAdmin
from bot.admins_info.subloader_admins import delete_admin

from bot.handlers.admin_commands.get_admins_cases_info import get_admins_info

router = Router()


@router.message(Command("delete_admin"))
async def deleting_admin(message: Message, state: FSMContext) -> None:
    """Удаление админа"""
    await message.answer(text="Введи username удаляемого админа c @\n"
                              "После добавления админа перезагрузить фоновый процесс на сервере.\n"
                              "Для отмены пришли 0.")
    await state.set_state(DeleteAdmin.DELETE_ADMIN)


@router.message(DeleteAdmin.DELETE_ADMIN)
async def delete_admin_name(message: Message, state: FSMContext) -> None:
    if message.text != "0":
        delete_admin(message.text)
        await message.answer(text="Готово")
        await get_admins_info(message)
    else:
        await message.answer(text="Отменено")
    await state.clear()