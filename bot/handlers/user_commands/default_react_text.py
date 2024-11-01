from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def for_text_message(message: Message) -> None:
    await message.answer(
        f"Я знаю только следующие команды:\n"
        f"/info_cases - список кейсов\n"
        f"/send_case - отправить на оценку\n"
        f"/instruction - инструкция\n"
        f"/help - помощь здесь")
