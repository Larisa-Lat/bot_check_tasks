from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.utils.states import DeleteCase
from model.cases_info.subloader_cases_info import delete_case

from bot.handlers.admin_commands.get_admins_cases_info import get_cases_info

router = Router()


@router.message(Command("delete_case"))
async def deleting_case(message: Message, state: FSMContext) -> None:
    """Удаление кейса"""
    await message.answer(text="Введи id удаляемого кейса\nДля отмены пришли 0.")
    await state.set_state(DeleteCase.DELETE_CASE)


@router.message(DeleteCase.DELETE_CASE)
async def add_metric(message: Message, state: FSMContext) -> None:
    if message.text.isdigit() and message.text != "0":
        delete_case(int(message.text))
        await get_cases_info(message)
        await message.answer(text="Готово")
    else:
        await message.answer(text="Отменено")
    await state.clear()