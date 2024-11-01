from aiogram.types import Message, FSInputFile
from aiogram import Router
from aiogram.filters import Command


router = Router()


@router.message(Command("cases_info"))
async def get_cases_info(message: Message) -> None:
    document = FSInputFile(path="model/cases_info/cases_info.json")
    await message.answer_document(document=document)


@router.message(Command("admins_info"))
async def get_admins_info(message: Message) -> None:
    document = FSInputFile(path="bot/admins_info/admins.json")
    await message.answer_document(document=document)