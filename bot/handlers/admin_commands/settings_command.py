from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters import Command

from bot.admins_info.subloader_admins import get_admins_id

from bot.handlers.admin_commands import add_admin_command, \
    add_case_command, delete_admin_command, \
    delete_case_command, get_admins_cases_info

router = Router()
router.message.filter(
    F.from_user.id.in_(get_admins_id())
)
router.include_routers(
    add_admin_command.router,
    add_case_command.router,
    delete_admin_command.router,
    delete_case_command.router,
    get_admins_cases_info.router
)


@router.message(Command("settings"))
async def show_commands_for_admin(message: Message) -> None:
    """Вывод всех комманд для админов"""
    ans = f"/cases_info - инфа о кейсах \n" \
          f"/add_case - добавить новый кейс\n" \
          f"/delete_case - удалить кейс\n" \
          f"\n\n" \
          f"/admins_info - инфа об админах\n" \
          f"/add_admin - добавить админа\n" \
          f"/delete_admin - удалить админа\n"
    await message.answer(ans)


